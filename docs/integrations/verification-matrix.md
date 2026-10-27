# Issue #2 Verification Matrix — Unrun

**Scope:** proposed architecture and tests, not completed integration. Sources and rationale: [ADR-0003](../decisions/0003-capability-driven-integration-ports.md), [contract](contract.md), [AE2 plan](ae2-first-adapter.md), [existing verification plan](../verification-plan.md).

| ID | Test environment | Procedure / oracle | Acceptance | Status |
| --- | --- | --- | --- | --- |
| INT-01 | 26.1.2 + NeoForge + our mod; no content mods | Launch client and dedicated server, create robot/dock/courier | Startup, vanilla gameplay, item integrity | NOT RUN |
| INT-02 | Same, offline network | Reboot offline, repeat courier, save/reload | No account/inference dependency | NOT RUN |
| INT-03 | Clean vanilla containers | Full / partial / empty-source / full-sink transfers, observe counts | No loss or duplication; exact remainder | NOT RUN |
| INT-04 | Clean vanilla containers | Stop server after pickup and after deposit, rejoin and reconcile | No double move or phantom success | NOT RUN |
| INT-05 | Vanilla with protection or claim provider as applicable | Unauthorized, removed enrollment, unknown authorization | No forbidden effect; explicit denial | NOT RUN |
| INT-06 | Supported NeoForge handler from a different mod | Authorized, sided and partial transfer via same action gateway | Correct counts and permissions | NOT RUN |
| INT-07 | No optional mods | Verify all core class references, startup, recipes, registration and features | No linkage error or missing core progression | NOT RUN |
| INT-08 | Compatible, disabled, incompatible optional mods | Startup and adapter probe with disabled/version mismatch | Safe core fallback and clear reason; loader constraints verified | NOT RUN |
| INT-09 | AE2 supported build | Enroll a verified AE2 network, inspect only permitted capability | Security and scope correctly enforced | NOT RUN |
| INT-10 | AE2 supported build | Submit one bounded crafting request, verify pending state | No submission without authorized actor; no premature completion | NOT RUN |
| INT-11 | AE2 supported build | Unload/restart/lose response; reconcile requester link | No blind resubmission or duplicate materials | NOT RUN |
| INT-12 | AE2 supported build | Denial, unpowered network, no pattern, missing stock, full output | No incorrect completion, user-visible blocked reasons | NOT RUN |
| INT-13 | AE2 removed/changed with prior pending work | Reload compatible surviving world after adapter disappearance | Core loads; external job unresolved safely | NOT RUN |
| INT-14 | Dedicated server / multi-robot later milestone | Concurrent requests, replayed request UUIDs and work budgets | No unauthorized double submit or job accounting violation | NOT RUN |

**Test evidence rule:** A future row becomes PASSED only with a linked, immutable build/commit, test steps, installed versions, observed server state/results and relevant logs. Mark FAILED or BLOCKED with diagnostics. A unit test of a parser, ADR validator or mocked adapter does **not** demonstrate server-world integrity. Each runtime behavior must be observed in the target environment; owner approval of the design does not equal implemented functionality.

**Sequencing:** INT-01–08 before specialized AE2 crafting; INT-09–12 before claiming a usable AE2 adapter. INT-13–14 are release gates for affected features and are not requirements for the first standalone courier proof. Any unexpected duplicate, unaudited transfer or permission bypass blocks release until resolved.
