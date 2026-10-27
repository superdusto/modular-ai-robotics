# Verification and Acceptance Plan

**Status:** Proposed test plan. No executable mod, benchmark or integration test has been run.

## Prototype test environment
Use a disposable Minecraft Java Edition 26.1.2 + NeoForge development world. Validate in a dedicated server environment as well as an integrated single-player server, with only the necessary test dependencies. Record the exact loader/build and Java versions when testing begins.

## Minimum courier acceptance matrix

| Test | Expected result |
| --- | --- |
| Normal transfer between authorized containers | Exact requested/available item quantity moves and is accounted for |
| Empty source | Clear no-input result, no phantom items, bounded retry |
| Destination full | No discarded/unaccounted cargo, blocked state and recovery |
| Partial extract or insert | Actual amounts and remainders are preserved |
| Restart during navigate / extract / insert / return | Safe resume or explicit recovery, no duplicate or lost items |
| Chunk unload and reload | No assumed live entity ticks in inactive chunks; state revalidated |
| Dock unreachable or energy exhausted | Clear recoverable/failure state, no infinite spin |
| Invalid/unauthorized work area | Denial before the supported action path's side effect |
| Missing required module | Job is rejected or suspended with an equipment reason |
| Multiple robots request same job | No double credit or conflicting reservation when coordination is introduced |
| No internet | Core robot behavior and save/load still work |
| Dedicated server | Same authoritative inventory/action outcome as single-player |

## Action/permission boundary testing
Test direct entity actions and any optional FakePlayer-context actions separately. For each, identify ownership, permission APIs, claim behavior and whether events can cancel the mutation. A custom entity's success is **not** proof it was authorized by all protection mods. Record unsupported protections as compatibility gaps.

## Performance and reliability
- Bounded scans, navigation requests, action work and retry attempts per server tick; measure before selecting numeric budgets.
- No uncontrolled chunk loading to keep arbitrary jobs running.
- Diagnose stuck paths and unreachable goals with explicit failure categories.
- Verify inventory and energy serialization on repeated save/restart cycles.
- Validate behavior with a second robot before claiming scheduler correctness.

## Expansion gates
1. Courier succeeds reproducibly and passes integrity/security cases.
2. Mining module gates an exposed ore task and does not bypass protection.
3. The same courier work definition runs on a ground robot and a flying chassis.
4. Individual mod adapters pass repeatable tests for their precise Minecraft/loader versions.

## Documentation policy
For every result record: date, Minecraft version, loader version, JDK, enabled mods, test steps, observed result, commit/build ID, and remaining gaps. No tests are marked passed merely because a design document describes them.
