# ADR-0002: Standalone Core with Optional Mod Integrations

- **Status:** Accepted (project-owner requirement)
- **Decision date:** 2026-10-26 (America/Chicago)
- **Scope:** The entire Modular AI Robotics project, including initial release and future optional integrations.
- **Implementation status:** Planning only; no implementation or compatibility testing has yet established this behavior.
- **Related:** [ADR-0001 — Initial Minecraft platform](0001-initial-platform.md), [Issue #2](https://github.com/superdusto/modular-ai-robotics/issues/2).

## Context

Minecraft players can have many different technology, storage, logistics and robotics mods. The goal is for our offline autonomous controller to coordinate player-built infrastructure where possible, without depending on the implementation, API stability, release cadence or continued development of any **specific third-party content mod**.

An addon-only mod that cannot operate without another robotics mod does not satisfy this requirement. A standalone mod that refuses to cooperate with other mods also fails the broader gameplay vision.

## Decision

**Modular AI Robotics is an independently playable Minecraft mod, with its own robots, controller, jobs and basic infrastructure. Other content mods are optional enhancements, never mandatory for its core.**

For the accepted initial platform, the mandatory runtime is **Minecraft Java 26.1.2 and NeoForge** ([ADR-0001](0001-initial-platform.md)). Minecraft and the chosen loader remain required platform dependencies; "standalone" is not "independent of Minecraft or NeoForge."

### Required independent core

The project must ultimately provide, without any additional content mod:

1. Own persistent ground-robot entity or equivalent physical unit, identity, ownership and inventory.
2. Offline task controller, job scheduler, memory/checkpoints and reusable action contracts.
3. Own usable energy/charging mechanic, docking/home infrastructure and starter hardware modules.
4. A way for the player to issue, pause and inspect bounded work orders and work permissions.
5. Useful interactions with **vanilla** world resources, inventories and appropriately authorized blocks/items.
6. A viable progression path for building, repairing and upgrading core robot units without obtaining resources or machine blocks supplied only by another content mod.
7. Save/reload recovery and safe error handling with **zero** optional content mods installed.

The first prototype remains a ground courier with a dock and two authorized vanilla containers. Other professions are future features, not promises of immediate completeness.

### Optional enhancement contract

- Integrate only through supported, version-verified, permission-aware interfaces.
- Prefer standard Minecraft/NeoForge capabilities when they genuinely express an operation; use per-mod adapters only for specialized network/crafting/machine/robot control.
- Keep third-party API references and initialization logic behind isolated optional integration boundaries. Do not make other mod classes mandatory during core startup.
- Do not list any third-party **content** mod as a required runtime dependency of the core.
- Optional integrations may be packaged within a single mod or as separately installed addon artifacts; **packaging remains undecided**. Either design must meet standalone installation and fallback tests.
- Use version-checked and conditional activation. Missing, incompatible or disabled integrations must not prevent core startup or core tasks.
- Adapters translate supported external capabilities into **our own stable task/action interfaces**. Our controller owns goals, permissions, task state and scheduling; the external mod owns its actual machines, networks, crafting effects and internal invariants.
- The player must explicitly authorize use of relevant machines/networks and work areas. Presence of an exposed capability does not by itself grant permission to use it.
- If an adapter is unavailable while a related job is pending, report a clear blocked/replan/recovery outcome. Reconcile actual resources and never assume an external request succeeded.
- Do not auto-drive unknown GUIs, bypass claims, or silently enable unsupported machine operations.

### Self-building and infrastructure growth

The core should eventually be capable of assembling **its own** robots/modules using its own recipes, base-game materials and its own assembly station/workshop. Optional integrations may accelerate manufacture by using the player's existing storage or processing, but cannot be the only possible route.

Full autonomous infrastructure expansion, blueprint placement, external network auto-crafting and direct control of third-party robots remain advanced, separately verified capabilities. The prototype does not need them.

### Independence test (design acceptance)

A supported core version must be able to:
- Start in a clean environment with **Minecraft + NeoForge + Modular AI Robotics only**.
- Create, command, recharge, save, load and use the basic courier robot with vanilla containers.
- Load an established world when previously supported optional mods have been removed, **to the extent the world itself still loads without those mods**, and gracefully handle unresolved optional jobs/references without claiming cargo was delivered.
- Stay usable when a compatible optional mod is installed but its adapter is disabled or encounters an expected API failure.
- Exercise each integration separately, while core tests run with zero optional content mods.
- Fail safely when a machine denies access or its network has no power, patterns, or required inputs.

A missing third-party mod can still make some externally supplied blocks/items unavailable in the wider world; our mod cannot guarantee another mod's world data remains intact after uninstallation.

## Alternatives considered

1. **Addon only for one robotics mod — Rejected.** Faster initial functionality could come at the cost of full dependency on another maintainer, ecosystem and compatible versions.
2. **Standalone with no integrations — Rejected.** Misses the player's goal of coordinating existing technical infrastructure.
3. **Standalone core + optional adapters — Accepted.** Core ownership and maintenance remain within this repository; optional adapters provide additional capabilities when supported.

## Consequences and tradeoffs

- We must implement our own minimum useful robot, dock, job control, persistence and vanilla-compatible action layer.
- This costs more initial effort than reusing another mod's mandatory robot implementation.
- External mod updates can still break **their corresponding adapters**, which we must maintain or disable, but should not stop base functionality.
- The codebase will need negative-dependency startup tests, optional-dependency isolation and version-specific adapter tests.
- Mod-specific compatibility may legitimately lag behind Minecraft/NeoForge releases.
- "Works on its own" is a project requirement until actual build/gameplay tests establish it.

## Follow-ups

- [Issue #2](https://github.com/superdusto/modular-ai-robotics/issues/2): design the optional adapter boundary, choose first integration and verify permissions.
- [Issue #3](https://github.com/superdusto/modular-ai-robotics/issues/3): define the independent controller/action contract.
- [Issue #6](https://github.com/superdusto/modular-ai-robotics/issues/6): verify the vanilla standalone courier.
- [Issue #9](https://github.com/superdusto/modular-ai-robotics/issues/9): establish a minimal 26.1.2 NeoForge build.
- [Infrastructure integration research](../infrastructure-integration.md) and [requirements](../requirements.md).

**Decision status is established as a project-owner choice. Implementation capability and version-specific interoperability remain unverified until tested.**
