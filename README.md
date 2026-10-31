# Modular AI Robotics

**Offline-first autonomous robotics for Minecraft.**

Modular AI Robotics is a proposed Minecraft mod for useful, persistent robotic companions: ground robots, flying drones, humanoid machines, and eventually larger industrial mechs. Robots should be able to work alongside a player, manage resources, assist with construction and defense, and recover from interruptions—without a paid AI service or an internet connection.

> **Status: Research and architecture planning.** No playable mod or prototype is available yet. The initial development target is **Minecraft Java Edition 26.1.2 + NeoForge + JDK 25** ([ADR-0001](docs/decisions/0001-initial-platform.md)). The **standalone-core, optional-integration architecture** is accepted ([ADR-0002](docs/decisions/0002-standalone-core-optional-integrations.md)). The **MIT code / reserved-asset licensing and contribution policy** is accepted ([ADR-0004](docs/decisions/0004-code-and-asset-licensing.md)). Implementation details and explicit authorization for significant implementation submissions remain open.

## Vision

Build **one extensible autonomy foundation** rather than a separate intelligence implementation for each profession or chassis.

A robot combines:
- A **controller**: identity, task memory, priorities, scheduling, and recovery.
- A **chassis**: movement, dimensions, energy, cargo capacity, and equipment slots.
- **Modules**: mining tools, manipulators, sensors, weapons, batteries, and other capabilities.
- **Actions**: validated operations such as moving, mining, placing, transferring, crafting, and defending.
- **Knowledge**: data-driven jobs, operating policies, resource classifications, and optional importable knowledge packs.

Robots should select work from their goals and available capabilities, rather than requiring constant manual commands. Hardware determines what they *can* do; policy and game-side validation determine what they *may* do.

## Project principles

1. **Standalone and offline.** The core mod must run with Minecraft and NeoForge alone, including its own useful robots, charging, basic work and progression. No other content mod, ChatGPT API, hosted language model, subscription or internet connection is required.
2. **Useful before clever.** Reliable task execution, persistence, and recovery come before natural language, advanced personality, or speculative general AI.
3. **One brain architecture, multiple bodies.** Jobs should work with different robot platforms when their required capabilities are available.
4. **Optional interoperability, never mandatory dependencies.** Use vanilla/NeoForge interfaces where they apply; isolate adapters for specialized third-party mod mechanics. Missing or incompatible external mods must not break the standalone core.
5. **World-safe by design.** Respect ownership, permissions, protected locations, server authority, item accounting, and explicit work boundaries.
6. **Data-driven expansion.** Support validated declarative knowledge and job definitions; imported data must not execute arbitrary code or grant new permissions.
7. **Incremental development.** Prove a small working robot loop before expanding to multiple chassis, professions, or complex integrations.

## Example robots

| Platform | Possible roles |
| --- | --- |
| Ground utility robot | Courier, storage manager, farmer, miner, construction assistant |
| Flying drone | Scouting, light delivery, collection, base monitoring |
| Humanoid robot | General-purpose tool use, defense, adventuring companion |
| Heavy mech | Advanced mining, hauling, heavy construction (later-stage concept) |

These are **concepts**, not currently implemented features.

See the [robot visual references](docs/visual-design/README.md) for the selected compact utility robot appearance and two additional chassis concepts. The planned graphics offering includes Low, Medium and High, with optional Ultra detail; the [graphics pack plan](docs/visual-design/graphics-quality-tiers-v0.1.0.md) separates those owner-selected goals from proposed rendering details.

## Proposed architecture

```text
Player orders + world observations
                 |
          Autonomous controller
       goals / memory / scheduling
                 |
      Task planner + capability check
                 |
       Validated reusable actions
                 |
   Chassis + installed hardware modules
                 |
  Minecraft server + optional mod adapters
                 |
        Verify outcomes and persist
```

The controller, task planner, and job definitions are intended to be independent of robot appearance. World-changing actions must be validated by server-side code, including ownership, permitted areas, resource availability, and protection-system rules where supported.

More detail: [Architecture](docs/architecture.md), [Vision](docs/vision.md), and [Requirements](docs/requirements.md).

## Standalone core and optional technology integrations

Our mod owns its basic robots, docking/charging, autonomous controller, vanilla work actions and a route to building/upgrading its own units. Other mods can add access to player-built storage, processing, auto-crafting, power or third-party robots through explicitly supported adapters. An unsupported mod provides no implied machine control. See [ADR-0002](docs/decisions/0002-standalone-core-optional-integrations.md) and [Infrastructure Integration](docs/infrastructure-integration.md).

## Knowledge packs and adaptation

The project may support **importable, declarative knowledge packs** for jobs, priorities, recipes or resource metadata, permitted operating procedures, and robot profiles. The initial format has **not** been selected. Structured, validated data is a more reliable starting point than attempting to interpret arbitrary PDF or Word documents.

Persistent experience may help robots remember known storage locations, failed routes, blocked tasks, and useful observations. This is adaptive deterministic behavior—not neural-network training. A knowledge pack cannot add a new native game action without implementing that action.

Optional future tools could help people prepare knowledge files outside Minecraft. They will not be required for in-game operation.

See [Knowledge Packs](docs/knowledge-packs.md).

## First proposed prototype

**One small autonomous ground courier, one charging dock, and two containers.**

The robot should:
1. Receive a bounded item-transport assignment.
2. Check cargo capacity, target access, and work-area permissions.
3. Navigate to the source container and withdraw items using supported interfaces.
4. Carry them to the destination and deposit the actual amount retrieved.
5. Return to a dock for charging.
6. Resume correctly after save/reload, without losing or duplicating items.

Once reliable, add a mining module and verify that the same action framework can complete a small approved mining task. A flying drone can later test the separation of controller and chassis.

The [courier scope and proposed contract](docs/courier/README.md) records the owner-selected policy for the first prototype only: another pickup after an incomplete batch requires owner-authorized continuation. Detailed action/recovery rules remain proposed. The general pack importer is deferred, and automatic repeat trips remain a future design alternative.

See the [Development Roadmap](docs/development-roadmap.md), [Verification Plan](docs/verification-plan.md), and [Player Experience](docs/player-experience.md).

## Research before implementation

The **initial** Minecraft and loader target is selected: **Minecraft Java Edition 26.1.2 + NeoForge + JDK 25**. Exact loader/build-tool pinning and third-party integrations still require verification. This project is not restricted to ATM10.

**Standalone operation is a fixed requirement.** Research now concerns which *optional* adapters to implement for compatible external robots, networks and machines. No third-party content mod or implementation is a core prerequisite; APIs, versions and licenses must be individually verified.

See [ADR-0001](docs/decisions/0001-initial-platform.md), [ADR-0002](docs/decisions/0002-standalone-core-optional-integrations.md), [Compatibility Research](docs/minecraft-compatibility.md), [Risks and Open Questions](docs/risks-and-open-questions.md), and the [issue tracker](https://github.com/superdusto/modular-ai-robotics/issues).

## Mechanical Decision Gate

Architecture decisions use a [machine-checkable ADR format](docs/decision-gate.md), validated by the [Decision Gate workflow](.github/workflows/decision-gate.yml) with automated [negative and positive tests](tests/test_decision_gate.py). The gate checks required documentation structure, scoped claim classification, evidence references, verification bookkeeping and explicit alternatives. It **cannot** prove technical claims true or replace Minecraft runtime tests and accountable review. Merge blocking additionally requires an active GitHub branch ruleset; the workflow alone is not branch protection.

## Contributing and project status

Research findings, test proposals, architectural feedback, and documented compatibility evidence are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first. The licensing/contribution policy is adopted; the significant-implementation contribution hold remains until separate explicit maintainer authorization.

For sensitive security concerns, see [SECURITY.md](SECURITY.md).

## License

The owner selected **MIT for original code, documentation, schemas and examples**, and **reserved rights for original artwork and sounds** with explicit gameplay, screenshot/video and official-release modpack permissions. Independent community scripts and behavior packs remain under their creators' chosen terms.

See [LICENSE](LICENSE), [asset permissions](ASSET_LICENSE.md), the [license map and inventory](docs/licensing.md), and [accepted ADR-0004](docs/decisions/0004-code-and-asset-licensing.md). The selected public copyright credit is **superdusto**. MIT requires preservation of its copyright/license notices; it does not require prominent public credit or patches to be submitted upstream.

Published license grants apply to the copies they accompany. [ADR-0004](docs/decisions/0004-code-and-asset-licensing.md#evidence-and-uncertainty) records the accepted revision and adoption evidence. The separate contribution hold concerns acceptance of significant new submissions and remains in place. Original reserved assets carry the asset-specific notice rather than the root MIT terms; third-party material keeps its own terms.
