# Modular AI Robotics

**Offline-first autonomous robotics for Minecraft.**

Modular AI Robotics is a proposed Minecraft mod for useful, persistent robotic companions: ground robots, flying drones, humanoid machines, and eventually larger industrial mechs. Robots should be able to work alongside a player, manage resources, assist with construction and defense, and recover from interruptions—without a paid AI service or an internet connection.

> **Status: Research and architecture planning.** No playable mod or prototype is available yet. The Minecraft version, mod loader, implementation plan, and software license have not been finalized.

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

1. **Offline and free to operate.** The core autonomy engine uses deterministic game-side logic. No ChatGPT API, hosted language model, or subscription is required.
2. **Useful before clever.** Reliable task execution, persistence, and recovery come before natural language, advanced personality, or speculative general AI.
3. **One brain architecture, multiple bodies.** Jobs should work with different robot platforms when their required capabilities are available.
4. **Modular, not universally compatible by assumption.** Prefer vanilla and common APIs, with optional adapters for specialized mod mechanics.
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

More detail: [Architecture](docs/architecture.md) and [Vision](docs/vision.md).

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

See the [Development Roadmap](docs/development-roadmap.md).

## Research before implementation

The starting Minecraft version and loader are **open decisions**. The choice should weigh API stability, Java/toolchain requirements, ecosystem maturity, and compatibility with technology and automation mods—not simply the newest Minecraft release.

We also need to evaluate **standalone machines vs. integration with existing robot mods**, including OpenComputers: Modernized, CC: Tweaked, and PneumaticCraft: Repressurized. No third-party implementation is assumed reusable without checking its API and license.

See [Compatibility Research](docs/minecraft-compatibility.md) and the [issue tracker](../../issues).

## Contributing and project status

Research findings, test proposals, architectural feedback, and documented compatibility evidence are welcome. Read [CONTRIBUTING.md](CONTRIBUTING.md) first. Code contributions should wait until the target platform, license, and minimal architecture are decided.

For sensitive security concerns, see [SECURITY.md](SECURITY.md).

## License

**A license has not been selected.** Public visibility does not grant permission to copy, redistribute, or incorporate the source or assets. Licensing is an explicit project decision to make before accepting or distributing implementation contributions.
