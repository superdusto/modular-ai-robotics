# Integrating Player-Built Infrastructure and Other Mods

**Status:** Standalone core + optional integrations accepted as a project requirement ([ADR-0002](decisions/0002-standalone-core-optional-integrations.md)). Specific adapters are still proposed and untested. A concrete design is proposed in [ADR-0003](decisions/0003-capability-driven-integration-ports.md), with a [core integration contract](integrations/contract.md), [AE2 adapter plan](integrations/ae2-first-adapter.md) and [verification matrix](integrations/verification-matrix.md). No runtime validation has occurred.

## Independence requirement

The mod must work with Minecraft + NeoForge alone, owning its robots, autonomy, docking, basic work and progression. Other technology mods are optional; failed or absent adapters must not stop core gameplay. See [ADR-0002](decisions/0002-standalone-core-optional-integrations.md).

## Goal

Our offline autonomous controller should be able to **use machines, networks and automation systems that the player has already built** to accomplish approved work orders. Over time, those systems could help manufacture upgrades, assemble additional robots, or extend the robot's own workshop.

**This is not synonymous with automatically controlling every other mod's robots or replicating every player's GUI interaction.** Integration depends on exposed operations, mod versions, permission semantics, and tests.

### Example: manufacture a second courier
1. The player registers an authorized storage network, processing equipment, and our mod's robot assembly/charging stations.
2. A work order requests one approved courier design.
3. The planner enumerates ingredients from verified recipes and checks existing stock and installed equipment.
4. For missing parts, the planner may request supported crafting/processing jobs from a compatible external system, or assign resources-gathering work to our own machines.
5. The controller tracks requested quantities, access policy, energy, job status, and machine responses, without assuming a cross-mod transaction is instantly complete.
6. Components are delivered to the designated assembler; the new robot receives a **new** identity, approved modules, and explicit ownership/work policy.
7. The robot charges and waits for a permitted job. If a recipe, machine, permission, required chunk, or input is missing, the plan stops and explains the blocker.

The recipe chain, assembly station, remote job interfaces, and task planner above are **design proposals**, not implemented APIs.

## Integration architecture (conceptual)

```text
Player-approved goals and registered infrastructure
                       |
             Offline autonomy controller
             (planning, memory, work queue)
                       |
           Capability and permission checks
                       |
               Action / integration ports
          /              |             \
 Vanilla + generic   Specialized       Robot-to-robot
 resource handlers   mod adapters      coordination adapters
          \              |             /
                 World-side results
                       |
              Verify / checkpoint
                       |
               Replan or report
```

Our controller owns the goal, work order, progress state, resource reservations, and user-visible reporting. **Other mods own their machines, networks, recipes, energy usage and crafting execution; a target-mod security station, grid-ownership check or other protection mechanism is not presumed to exist.** The Modular AI Robotics server policy must independently establish endpoint/network authority and any supported claim/protection decision at enrollment, on every action and for incoming AE2 requester output callbacks. Our adapter may request work but cannot claim completion until actual output and custody are reconciled. See [the proposed contract](integrations/contract.md) and [AE2 plan](integrations/ae2-first-adapter.md) (`F1`, `F2`; `INT-09A`, `INT-09B`, `INT-10A`, `INT-10B`).

Keep adapters optional and version-scoped; if an external mod is absent or its API changes, the core must remain usable.

## Capability tiers

| Tier | Intended operation | Feasibility / boundary |
| --- | --- | --- |
| A — Vanilla/common automation | Move items between authorized containers; observe or transfer fluids/energy where the interfaces allow | Common NeoForge APIs; requires world authorization and accounting |
| B — Network-aware | Observe stocks, interact with documented storage networks, place work requests | Specialized adapter; not equivalent to universal network access |
| C — Machine work orders | Request crafting, processing, charging, or assembly through a documented API | Needs implementation for each supported machine/network and exact version |
| D — Existing third-party robots | Ask supported turtles/drones/robots to perform constrained work | Requires a documented command surface or explicit cooperating program/bridge; direct AI ownership is not assumed |
| E — Autonomous infrastructure expansion | Craft, place, connect, configure and validate approved new machines | Requires verified recipes, blueprint/work-area controls, permissions, physical actions, resources and per-mod semantics |

## Verified upstream baseline (as of 2026-10-26)

### NeoForge Minecraft 26.1
- NeoForge documents capability access and transaction-backed resource transfers.
- Modern interfaces are **`ResourceHandler<ItemResource>`, `ResourceHandler<FluidResource>`, and `EnergyHandler`**. **Do not base new 26.1 code on 1.21.1-era `IItemHandler`, `IFluidHandler`, or `IEnergyStorage` as the preferred APIs.** NeoForge's major transfer rework replaced those APIs.
- A resource transaction can commit or roll back the operations **participating in that transaction**. It does not guarantee atomic completion of a multi-tick, cross-mod manufacturing process or crash recovery.
- Authoritative sources:
  - [NeoForge 26.1 Capabilities](https://docs.neoforged.net/docs/inventories/capabilities/)
  - [NeoForge 26.1 Transactions](https://docs.neoforged.net/docs/inventories/transactions/)
  - [NeoForge transfer rework announcement](https://neoforged.net/news/21.9-transfer-rework/)

### Concrete mod candidates

| Mod / ecosystem | Version-specific evidence | Integration hypothesis | Evidence status |
| --- | --- | --- | --- |
| [Applied Energistics 2](https://appliedenergistics.org/download) | `v26.1.13-beta` release for Minecraft **26.1.2** on 2026-09-30 | Optional AE2 grid/storage/crafting adapter | Release and API **established**; interoperability with our future mod **untested** |
| [CC: Tweaked](https://github.com/cc-tweaked/CC-Tweaked/releases/tag/v26.1.2-1.120.0) | `v26.1.2-1.120.0` prerelease on 2026-06-15 | Optional bridge for player-programmed turtles/computers, only if a secure command path is designed | Tagged release **established**; direct controller API/bridge **unverified** |
| [OpenComputers: Modernized](https://github.com/habzg/OpenComputers-Modernized) | Published version 1.10.7 targets **1.21.1**; 26.x port noted as in progress | Future component/robot addon adapter | **26.1.2 support unverified**, not presumed |
| [PneumaticCraft: Repressurized](https://github.com/TeamPneumatic/pnc-repressurized) | Inspected releases and public source primarily target **1.21.1** | Future drone/programming interface | **26.1.2 support unverified**, not presumed |
| Other industrial mods | Version- and API-dependent | Generic resource access first; specialized machine adapters second | Individual compatibility **unverified** |

AE2's inspected `v26.1.13-beta` source contains `ICraftingService` methods such as `beginCraftingCalculation` and `submitJob`, and `IActionSource` for player/machine attribution. Its `ICraftingService` documentation explicitly requires persisting the resulting `ICraftingLink` for a machine requester when tracking work across unload/reconnections.

- [AE2 tagged ICraftingService](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingService.java)
- [AE2 tagged IActionSource](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/security/IActionSource.java)
- [AE2 official add-on API overview](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/API.md)

**Important:** AE2 action sources and network access semantics need an appropriate authorized context. Neither generic capability availability nor a public API proves the controller has access to a player-owned network.

## Interaction and ownership contract (proposed)

**Explicit enrollment:** The player designates which containers, machines, networks, stations, areas or machine groups a controller is allowed to use. Discovering a machine is not permission to control it.

**Capability requests:** An adapter reports the narrowly defined operations it supports (e.g., `inspect_inventory`, `transfer_item`, `request_craft`, `read_craft_status`, `activate_approved_operation`, `issue_robot_command`); these are **conceptual action IDs**, not NeoForge method names.

**Separate authorization:** The Modular AI Robotics server must validate the requesting actor/owner, target, attached network identity, work zone, operation scope and current state at enrollment, every use and asynchronous callback. Use only independently verified claim/protection-provider and target-mod authorization checks applicable to the exact endpoint/action; do not presume a generic per-mod security system. No-provider, unknown, denied and errored rights must not be treated as grants; block any external-network operation whose ownership cannot be established. A custom entity, FakePlayer or AE2 `IActionSource` identity does not inherit another owner's authorization. Test `INT-05`, `INT-09A`, `INT-09B`, `INT-09C` and `INT-10C`.

**State integrity:** Use atomic transfer transactions where supported. For longer jobs, track unique request IDs, required materials, pending results, completion evidence, retries, and safe reconciliation after save/reload. Do not promise distributed atomicity.

**Bounded autonomy:** Limit crafting quantity, energy spending, construction footprint, recursion, scans, work queue size and robot population; optionally require confirmation for expensive or destructive construction.

**Degraded operation:** If an external mod is absent, unloaded, changed or unavailable, remain functional for vanilla-supported tasks; report blocked operations without consuming items or assuming work succeeded.

## Standalone versus addon framing

This is **not necessarily a binary decision**:
- Our mod could own the offline planner, controllers, robot chassis and core action interfaces.
- Player-built external technology can remain intact and be controlled through optional adapters.
- Some future third-party robots might be controlled as **external executors** via supported interfaces.
- An addon-only design is rejected; optional addons and adapters remain possible, but the core cannot depend on any third-party content mod.

**Standalone-first architecture is accepted** in [ADR-0002](decisions/0002-standalone-core-optional-integrations.md). ADR-0003 proposes the precise gateway and adapter design; [Issue #2](https://github.com/superdusto/modular-ai-robotics/issues/2) remains open for owner design approval and implementation/runtime evidence.

## Proposed tests

1. On **NeoForge 26.1.2**, register one player-approved vanilla chest and one our-mod robot. Test permission-aware transactional item transfer and reload.
2. Register an external block exposing a compatible `ResourceHandler<ItemResource>`. Transfer across the same path; test side and inventory restrictions.
3. With a matching AE2 version, connect an owned controller/bridge to an authorized network. Inspect available stock, request a known pattern, persist the crafting request link, and confirm the output after chunk unload/reload.
4. Test denied access, missing machine, unpowered network, unavailable pattern, full output, interrupted craft, duplicate requests and mod-uninstallation fallback.
5. Design (but do not yet implement) a **bounded self-expansion** experiment: make one permitted new component from a player-approved recipe/network and assemble one robot in an approved workshop.

## Follow-up decisions

- Does automatic access require manual enrollment of every machine, or may a player approve a named network/dock zone?
- Will the first integration include only storage, or a complete crafting request?
- Is a robot assembly station a base-game block owned by our mod?
- What approvals govern machine placement and spending of rare materials?
- Is future control of third-party robots worthwhile if users must first install a trusted bridge program?
- How are job IDs, reservations and attribution persisted between the core controller and external mod systems?

See [Requirements](requirements.md), [Architecture](architecture.md), [Risks](risks-and-open-questions.md), [Issue #2](https://github.com/superdusto/modular-ai-robotics/issues/2), and [Issue #7](https://github.com/superdusto/modular-ai-robotics/issues/7).
