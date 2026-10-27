# Proposed courier verification plan

**Status: Proposed; complete cases not run, 2026-10-27.** These cases assess the [courier contract](contract.md) under the [selected first scope](README.md). They extend the repository's [acceptance plan](../verification-plan.md). No scenario is passed because its expected result is written here, and no local model observation is inherited as Minecraft evidence.

Case namespace: mar-courier-pack-verification@0.1.0, RCN-01–RCN-08. The general importer and automatic repeat-trip policy are deferred. Keep partial model executions separate from complete case results.

## Environments and results

The first implementation stage is a deterministic in-memory model with fixed bindings, trusted fixture observations and a logical active clock. Real integration requires disposable integrated and dedicated servers on Minecraft Java 26.1.2, JDK 25 and exact recorded NeoForge/project builds. Provider-specific support requires its own exact-version discovery/applicability/action evidence.

Use one robot, one dock and two distinct enrolled vanilla containers. Define real item/component identity and source/cargo/destination stores. Model capacity is an explicit fixture value; a real six-item destination must have demonstrably six usable spaces under actual slot/stack rules. An empty vanilla barrel is not that fixture. Track filler keys and external actor flows separately.

Report six independent verdicts:

| Verdict | Required observation |
| --- | --- |
| Safe stopping | Effective dispatch fence, bounded in-flight outcome and absence of prohibited new effects |
| Physical conservation | Consistent per-key observation of all real stores and known external flows |
| Delivery credit | Unique attributable insertions, separate from destination's later aggregate stock |
| Authorization/disclosure | Current actor/resource rights for every protected read/effect, including recovery |
| Durable controls and records | Survival of fences, replay history and nonrenewing budgets in the declared failure scope |
| Energy | Actual supply debit, battery gain, spending and defined losses independently accounted |

Use pass/fail/inconclusive/not_assessed for executed verdicts, alongside a separate execution status. Unknown stores are not zero. A definite conservation failure remains a failure even if safe stopping passes. A model can demonstrate modeled counts and eligibility, not real authentication, physical quantities, energy or disk durability.

Keep clean restart, abrupt process loss, synthetic old/new snapshot combinations, and OS/storage/power loss as separate scopes. Prove reachability before treating an injected file combination as an actual crash outcome. Require repeated recovery/second-failure observations where relevant.

Before each execution record source/build identity, exact environment, policy/variant, approved fixture bounds, grants/provider states, initial quantities/keys, external flows, command/receipt/counter history and fault point. Save observed outputs, all verdicts, date, evidence location and limits. Teardown resets only the isolated fixture after preserving evidence; it is not a product repair mechanism.

## RCN-01 Owner continuation after an incomplete batch

- execution_status: not_run; readiness: blocked_pending_implementation.
- Setup: Q=16, source10/cargo0/destination0, known bindings/rights and finite original limits. A second variant uses source64 and cargo capacity10.
- Steps: pick up actual10, deliver all10, complete permitted service, then advance eligible events and repeat the original request. In the shortfall variant, a fixture actor adds six source items with that inflow recorded. Try another pickup before authorization, then issue a fresh owner continuation and try the remaining six. Replay original and continuation identities.
- Oracle: E=D=10/C=0 remains suspended before continuation, with honest shortfall versus capacity-limited reason. No automatic second batch. Continuation preserves the same job/intent/beneficiary and spent limits; only Q−E=6 remains to pick up. Fresh batch certificates are required; old load/unload/home results cannot authorize a new effect. Changed intent collides and replays change no quantities.
- Limits/cleanup: original cumulative action/service/retry limits; retain observations then reset the isolated fixture. Automatic repeat-trip comparison is deferred.

## RCN-02 Capacity limited versus incomplete pickup

- execution_status: not_run; readiness: blocked_pending_implementation.
- Setup: Q=16, source64. Variant A has proven cargo capacity10; B targets16 but actual paired pickup is7 without proven source shortage; C yields zero or unknown effect.
- Steps: bind the pickup target before the effect, capture actual paired quantities and evaluate load/dependent eligibility. Try a caller-supplied shortfall flag and a new operation ID.
- Oracle: A may load/deliver/service10, then needs owner continuation. B retains C=7, load is partial and destination/new pickup stay blocked pending reviewed disposition. Do not invent shortage, top up or promote partial success. C never fakes load completion; unknown effects enter recovery.
- Limits/cleanup: one initial pickup and only separately eligible original retries; capture actual capacity and preserve counts before resetting the fixture.

## RCN-03 Reachable controls and truthful acknowledgments

- execution_status: not_run; readiness: blocked_pending_implementation.
- Setup: retained cargo with variants for unknown effect, missing/unloaded body, missing hardware, denied endpoint, exhausted production and failed record storage. Include stale/unauthorized commands and receipt pressure.
- Steps: request stop/cancel/revoke, order newer stops against older resumes and replay commands. Inspect request recording, effective fence and effect resolution separately. Try subsequent delivery and separately authorized service.
- Oracle: valid record-only controls use their own protected path. Unknown effects remain unresolved with cancellation requested; terminal cancellation requires resolution. Newer fences survive replay. Failed storage cannot claim durable acknowledgment and fences physical service as well as delivery. Deduplication/retention remains bounded without starving a required future stop.
- Limits/cleanup: finite command/rate/storage/scheduling bounds; no world read merely to record a stop; preserve failed-write evidence before fixture reset.

## RCN-04 Protected recovery and nonrenewing limits

- execution_status: not_run; readiness: blocked_pending_implementation.
- Setup: explicit finite production/recovery/service partitions, separate recovery pass/read limits and protected control capacity. Choose synthetic model values separately from measured server defaults.
- Steps: exhaust production, then attempt authorized and denied/unavailable recovery reads. Exhaust the recovery reserve and repeat through new IDs, replan, continuation and activation. Attempt stop afterward and try missing saved budget history.
- Oracle: production cannot spend the reserve. Every attempted read consumes applicable read/work limits; each pass also needs work. Exhaustion becomes passive blocked custody without polling or renewed counters. Stop uses its protected bounded mechanism. Unknown consumption blocks rather than resetting to full.
- Limits/cleanup: original finite allocations and a fixed event sequence; retain exhausted snapshots and reset only the isolated fixture.

## RCN-05 Retained cargo dependency release and timing

- execution_status: not_run; readiness: blocked_pending_implementation.
- Setup: Q=16, proven load16, initial insertion6/C=10. Include revoked/restored rights, attributed and unattributed matching totals, zero/partial/success retries, no-load and unknown physical-state branches.
- Steps: inspect eligibility after each outcome; restore/activate and attempt delivery before owner validation. Supply current or invalid recovery evidence, replay a continuation after a newer stop, and refresh destination context. Exercise increasing backoff, exact due/deadline boundaries and cumulative retry exhaustion. Try normal return/charge and separate safety service.
- Oracle: partial unload blocks normal home/recharge. Retained-cargo recovery requires same-job attributable evidence/current authority and never reloads or demands empty cargo. Historical navigation cannot supply fresh context. Early eligibility queries invoke no effect; zero/partial attempts consume limits; restart/new IDs/owner commands renew neither attempts nor deadlines. Normal full unload releases home, and exact delivery plus actual service gates job success. Safety movement grants no delivery/DAG credit; relevant uncertainty blocks it. Another pickup cannot start after its needed insertion allowance is exhausted.
- Limits/cleanup: original insertion, active/no-progress, recovery and service limits; retain every branch's counts/results before fixture reset.

## RCN-06 Lifecycle with retained custody

- execution_status: not_run; readiness: deferred_pending_pack_lifecycle_implementation.
- Setup: pinned future artifact/job records with cargo or unknown effects, retained versions/receipts and consumed limits.
- Steps: try disable, replacement, rollback, migration and retirement with valid/invalid record mappings, changed intent, missing old bytes and stale revisions.
- Oracle: dependent work is fenced while scoped controls/evidence access remain available. Existing jobs retain pins; rollback changes selection only. Explicit mapping preserves intent/beneficiary/receipts/fences/budgets. Unsupported or uncertain migration quarantines; retirement cannot erase custody or replay history. No version change repairs world state.
- Limits/cleanup: bounded inert store operations, preserved original records and explicit fixture reset. This does not bring the importer into the first scope.

## RCN-07 Independent verdicts at save cuts

- execution_status: not_run; readiness: blocked_pending_save_owners_and_fault_instrumentation.
- Setup: identify independent source/cargo/destination, body/battery, dock supply/berth and job/control/budget saves; use isolated exact-key stores with external flows tracked.
- Steps: select finite cut combinations around pickup, insertion, movement, charging, controls and receipt updates. Distinguish synthetic snapshots from demonstrably reachable faults; restart/recover twice and observe all stores and verdicts.
- Oracle: a hold alone proves neither conservation nor durable control survival. Observed loss/duplication, false credit, reset limits and unexplained energy remain failures. Preserve unknown effects without balancing spawn/deletion/refund, teleport or energy reset. Synthetic combinations establish only that modeled scenario.
- Limits/cleanup: fixed fault schedule and declared failure scope; preserve evidence before restoring the disposable baseline.

## RCN-08 Exact strings canonical content and activation

- execution_status: not_run; readiness: deferred_pending_selected_schema_validator_and_importer.
- Setup: a separately reviewed schema/profile, complete field/reference corpus, independent canonical-byte vectors and version-collision records.
- Steps: probe whole decoded IDs/references/versions/digests with valid boundaries, prefix/suffix/control forms including U+2028/U+2029, lookalikes and normalization variants. Compare equivalent object ordering versus order-sensitive arrays/strings; try preview digests and changed content under one version.
- Oracle: independent whole-string semantic checks reject malformed values even if regex substring acceptance occurs. Preserve reviewed string/array semantics. A digest grants neither author identity nor world rights; incomplete preview cannot activate and version collisions reject. Schema/example/manifest/registry references agree on the separately selected versions.
- Limits/cleanup: fixed input/depth/token/corpus caps and inert temporary import store; preserve reports then remove fixture-owned candidates. No format or canonicalizer is selected by this case.

## Review and execution gates

Resolve the [open review decisions](README.md#decisions-still-requiring-review), including contribution terms, exact toolchain, authority/resource bindings, save owners/restore lineage, measured limits and fault reachability before the corresponding integration work. Model results must identify their exact implemented subset; they cannot change a complete case to passed without its declared environments and oracles.

The [Decision Gate](../decision-gate.md) checks ADR documentation/bookkeeping. Its success does not execute these cases or verify the courier's technical behavior.
