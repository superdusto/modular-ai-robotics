# Development Roadmap (Proposed)

Standalone courier modeling has begun in the [candidate model](../models/courier/README.md); no Minecraft implementation has begun. Stages are gated on evidence and verified behavior rather than dates. The owner authorized only the standalone model submission; NeoForge scaffolding and real client/server work require separate authorization.

## Stage 0 — Technical choices
- **Accepted:** Minecraft Java 26.1.2, NeoForge and JDK 25 ([ADR-0001](decisions/0001-initial-platform.md)). Verify and pin the exact NeoForge/Gradle setup when scaffolding.
- **Accepted:** Standalone core with no required third-party content mods ([ADR-0002](decisions/0002-standalone-core-optional-integrations.md)); evaluate optional adapters to compatible external machines.
- **Accepted:** MIT code / reserved-asset licensing and contribution policy ([ADR-0004](decisions/0004-code-and-asset-licensing.md), 2026-10-28). The standalone model submission is authorized; review rights for the actual contribution and record separate authorization for subsequent implementation scopes.
- Document security and action-permission model.

**Exit:** Platform, standalone architecture and licensing/contribution policy accepted. Remaining: Minecraft project toolchain pins, authorization beyond the model submission, action-permission design and optional adapter priorities. Model checks do not satisfy the later Minecraft stage exits.

## Stage 1 — Persistent robot foundation
One **mod-owned** ground robot, owner, home/dock, inventory, energy, safe navigation, and save/load identity without any other content mod.

**Exit:** Repeated reloads preserve identity and cargo without duplication.

## Stage 2 — Courier end-to-end
Two assigned **vanilla** containers, item transfer, navigation, charge/return, bounded retries and interruption recovery.

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
