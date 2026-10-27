# Development Roadmap (Proposed)

No implementation has begun. Stages are gated on evidence and verified behavior rather than dates.

## Stage 0 — Technical choices
- **Accepted:** Minecraft Java 26.1.2, NeoForge and JDK 25 ([ADR-0001](decisions/0001-initial-platform.md)). Verify and pin the exact NeoForge/Gradle setup when scaffolding.
- Compare standalone robots with supported integration into OpenComputers: Modernized, PneumaticCraft, and CC: Tweaked.
- Select a license after checking intended dependencies and asset distribution.
- Document security and action-permission model.

**Exit:** Initial target accepted. Remaining: implementation/toolchain pins, standalone-vs-addon decision, license, and action-permission design.

## Stage 1 — Persistent robot foundation
One ground robot, owner, home/dock, inventory, energy, safe navigation, and save/load identity.

**Exit:** Repeated reloads preserve identity and cargo without duplication.

## Stage 2 — Courier end-to-end
Two assigned containers, item transfer, navigation, charge/return, bounded retries and interruption recovery.

**Exit:** Auditable no-loss/no-duplication completion and safe failure on full/unloaded/protected targets.

## Stage 3 — Hardware gates and mining
One mining module, one approved exposed ore target, validated break/collect/deliver.

**Exit:** Mining succeeds with module, fails safely without it, and respects permissions.

## Stage 4 — Reusable jobs and chassis
Add farming/courier/miner composites and one aerial chassis to prove capability-driven autonomy.

**Exit:** A shared work order functions across supported platforms without duplicating the planner.

## Stage 5 — Mod integrations and coordination
Optional adapters for selected storage/technology mods; work reservations, inter-robot jobs, resource requests.

**Exit:** Individual adapter regression tests; compatibility failures do not break the core.

## Stage 6 — Advanced systems
Construction, heavy mechs, complex excavation, defense, personality, knowledge-pack tools and optional user-provided external assistance.

**Exit:** No regression in safety, offline operation, persistence, or performance.

## Baseline constraints
No paid AI API is required. Never assume support for all Minecraft versions, third-party machines, or arbitrary documents.
