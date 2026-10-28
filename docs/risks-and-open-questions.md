# Risks, Open Questions and Decision Boundaries

**Reviewed:** 2026-10-26. Risks are design hypotheses, not reported failures of an implementation.

| Risk / uncertainty | Potential impact | Planned response | Tracking |
| --- | --- | --- | --- |
| Desired external mod has no compatible 26.1.2 release/API | One optional integration is unavailable | Use mod-owned entities; disable incompatible adapter without affecting core | [#2](../../issues/2) |
| Optional mod is updated, removed or incompatible | Startup failure or stranded work if improperly coupled | Isolate optional APIs and test no-mod startup and recoverable jobs | [#2](../../issues/2) |
| World protections treat non-player actors differently | Unexpected block/container modification | Test server authority and supported protection hooks, deny unverified actions | [#7](../../issues/7) |
| Inventory transfer interrupted or partially accepted | Duplication, item loss, invalid work completion | Track actual moved quantities; staged checkpoints; restart reconciliation | [#6](../../issues/6), [#7](../../issues/7) |
| Chunk unload and entity lifecycle | Task stalls, stale targets, inconsistent memory | Persist resumable state; revalidate on activation; bound chunk-loading policy | [#6](../../issues/6) |
| Autonomy scans / pathfinding burden server | Tick lag, high CPU/memory usage | Budget navigation, scanning, retries and job scheduling; benchmark | [#3](../../issues/3) |
| Data pack imports contain unsafe or ambiguous instructions | Unauthorized actions or confusing behavior | Strict schemas; no embedded executable code; preview and rollback | [#5](../../issues/5) |
| Mod APIs vary by Minecraft version | Fragile compatibility, hard-to-maintain adapters | Compatibility tiers; version-locked optional tests and adapters | [#2](../../issues/2) |
| Flying navigation or large mechs have different physics/geometry | Chassis design leaks into planning, navigation bugs | Prove one courier on two chassis before expanding | [#4](../../issues/4) |
| Licensing direction selected; detailed terms and existing-material authority pending | Ambiguous rights if the proposal is treated as adoption | Review [ADR-0004](decisions/0004-code-and-asset-licensing.md), provenance and explicit contribution authorization | [#8](../../issues/8) |
| Complex UX or personality features expand scope | A working prototype is delayed | Require a minimal player control/status path first; defer flavor | Proposed |

## Decisions already accepted
- Minecraft Java **26.1.2**, **NeoForge**, **JDK 25** initial target — [ADR-0001](decisions/0001-initial-platform.md).
- Offline-first; no mandatory ChatGPT API, hosted LLM, subscription or external connection.
- The first proving task is a persistent courier and charging dock.
- Standalone core with optional integrations and no required third-party content mods — [ADR-0002](decisions/0002-standalone-core-optional-integrations.md).

## Still unresolved
1. Which optional adapters to prioritize, and whether adapters should be internal or separately packaged.
2. Exact MDK, NeoForge, Gradle and developer environment pinning, including tests.
3. Adoption of the selected MIT code / reserved-asset package, existing-material authority and explicit contribution authorization ([ADR-0004](decisions/0004-code-and-asset-licensing.md)).
4. Robot identity ownership and migration across physical chassis.
5. Exact permission/protection adapters and action semantics.
6. Knowledge pack format, validation versioning and import UX.
7. Work-order/player interfaces and initial progression/balance rules.
8. What (if any) mod compatibility ships with the first public version.
9. Performance budgets, multiplayer concurrency, and chunk lifecycle policy.

## Evidence discipline
Use official docs/source for present-tense compatibility claims, record dated release/build versions, and separate **documented API support** from **observed in-game results**. Unsupported and untested are not synonymous with impossible.
