# Proposed courier verification plan

**Status: Proposed; complete cases not run, 2026-10-27.** These cases assess the [courier contract](contract.md) under the [selected first scope](README.md). They extend the repository's [acceptance plan](../verification-plan.md). No scenario is passed because its expected result is written here, and no local model observation is inherited as Minecraft evidence.

Case namespace: mar-courier-pack-verification@0.1.0, RCN-01–RCN-10. The general importer and automatic repeat-trip policy are deferred from the first prototype. Keep partial model executions separate from complete case results.

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

## RCN-09 Player-facing courier controls

- planning_status: planned; execution_status: not_run; readiness: blocked_pending_player_control_surface_and_integration.
- Requirements/environment: the player-facing controls and feedback in [prototype requirements](../requirements.md) and [player experience](../player-experience.md). Run separately on an integrated server and a dedicated server, with the standalone core and exact recorded builds. Use whichever player-facing command or interface surface is selected later; this case chooses no GUI or layout.
- Setup: an authenticated owner, an unauthorized second player, one enrolled robot/dock and two authorized containers. Use a bounded Q=16 order, then a known partial insertion with E=16, D=6 and retained C=10. Define record-status and live-inventory disclosure rights separately. Include destination-full, protected-target, unavailable-chunk, missing-equipment and exhausted-limit branches with attributable outcomes.
- Steps: through the player-facing surface, assign a valid bounded order, inspect its identity/progress/custody/service status, and observe blocked reasons. Request pause during retained cargo and inspect pending versus effective stop. Have the second player attempt assignment, inspection, pause and recovery/continuation. Revoke a relevant resource right, attempt owner recovery, then restore the right through the authorized fixture path and request continuation of the original retained cargo. Exercise incomplete-batch feedback under the selected first-prototype policy without automatically authorizing another pickup.
- Visible-status oracle: the owner sees accepted/rejected work, actual proven progress, retained cargo and an actionable blocked reason. Distinguish a pending stop from an effective fence and resolved effects; do not display a historical or uncertain quantity as current fact, or partial delivery as job success. Use player-meaningful status without requiring a particular UI presentation.
- Authorization/disclosure oracle: unauthorized commands cause no job/custody/permission change or physical effect, and inspection/denial feedback discloses no protected job or inventory data. Authorized retained-record status may remain available under its own ACL when endpoint access is revoked; do not read a denied live inventory to populate that status. Owner recovery still needs current resource rights and attributable same-job evidence, rather than trusting the displayed state.
- Recovery oracle: pause preserves delivered credit and cargo. Valid continuation delivers at most the retained ten under original limits, without empty-cargo admission or re-extraction, and refreshes required context. An incomplete goal requiring a later pickup shows that owner continuation is needed for this prototype. A click or command acknowledgment alone is not proof that a physical action completed.
- Evidence/limits/cleanup: capture the player command/interaction sequence, owner-visible and unauthorized-player responses, server-side authorization/dispatch evidence, quantities and consumed allocations. Use original finite limits; keep branches separate, retain evidence and reset only the disposable fixture. Internal helper calls alone cannot pass this player-facing case.

## RCN-10 Server chunk unload and reload

- planning_status: planned; execution_status: not_run; readiness: blocked_pending_chunk_lifecycle_and_server_integration.
- Requirements/environment: [persistent integrity and chunk-transition requirements](../requirements.md), executed separately on an integrated server and a dedicated server. Use exact recorded builds and an instrumented disposable fixture that can establish actual server chunk and entity-ticking state; client render distance, walking away or assumed unload is insufficient evidence.
- Setup: place the robot, source, destination and dock in separately controllable chunks within the approved work scope, without relying on spawn retention or force-load tickets. Start at a proven bounded boundary after pickup and, in another variant, after a partial insertion with E=16, D=6, C=10. Capture endpoint incarnations, item/component identity, custody/receipts, spent counters, next retry time and clock references. Control or explicitly account for external item flows. Declare the active-clock and any absolute-deadline semantics before execution.
- Variant matrix: unload and reload each row independently while recording which other contexts remain available. Include a permission-revocation or endpoint-replacement branch during inactivity, and repeat unload/reload to check that limits are not renewed.

| Inactive context | Required observation |
| --- | --- |
| Robot chunk / body | Prove server unload and lack of active entity ticking; no simulated movement, item transfer, recharge or delivery progress while the body is inactive |
| Source chunk | Block physical work and observations that require the inactive source; preserve carried custody and the first profile's conservative normal-continuation checks |
| Destination chunk | No insertion or dependent normal completion through an inactive destination; retain actual remainder and report unavailable context |
| Dock chunk | No docking/charging through an inactive dock; block any other action whose required energy/route context depends on it, without inventing service completion |

- Steps: establish the boundary and actual unload, attempt affected work and player status/control operations while inactive, change authority or incarnation in a declared branch, then reload. Revalidate loaded context, identity, current rights and relevant physical evidence before dispatch. Recover/resume already-carried cargo under its separate recovery/resume permissions and applicable action guards, following the [contract's distinction between recovery and another pickup](contract.md#continuation-and-recovery). Retry only the proven carried remainder at its eligible time under the original allocations; do not apply the new-pickup authorization rule to that retained-cargo path.
- Recovery versus new-pickup oracle: already-carried cargo with attributable completed-load evidence continues within its original job and extraction lineage after authorized reconciliation/resume. Do not require empty-cargo admission, a new extraction, or the first-prototype owner command for another pickup merely because chunks reloaded. Separate recovery/resume authority, current resource rights, controls, resolved relevant effects and remaining limits still apply; reload itself grants no permission. Only when a completed batch/service has C=0, D<Q and another pickup is proposed does the first-prototype policy require its fresh owner-authorized pickup continuation. Valid recovery of carried cargo does not authorize that later pickup.
- Physical-availability oracle: no physical action may execute if its required robot/entity, target, route or dock context is inactive or unavailable. Earlier permission does not waive availability. An action using other loaded contexts may proceed only if its existing action-specific authorization, physical prerequisites and limits permit it; unloading an unrelated context creates no emergency bypass or blanket ban on independently valid service.
- Control oracle: authorized record-only stop/revoke remains available through its separate server-record path even when the robot is unloaded. Reject unauthorized controls and independently protect status disclosure. Recording a fence does not simulate entity ticks or claim that prior effects or storage durability are resolved.
- Custody/quantity oracle: retain original job/robot/beneficiary, operation history and actual item identity/amounts without re-extraction, duplicate credit or invented cargo. With all stores observable at consistent before/after boundaries, check per-key conservation and attributable delivery with known external flows. An unloaded or unreadable store remains unknown, not zero; do not force-load it merely to manufacture an observation. Replacement, denied reads or contradictory evidence blocks dependent work and retains the gap.
- Budget/time oracle: preserve consumed counters without resetting them; charge only work actually performed to the correct allocation, including authorized record/control/recovery work during robot inactivity. No synthetic production attempts or inactive robot ticks accrue. Preserve retry counts and next-eligible-time meaning under the declared clock; reload cannot renew attempts/deadlines, invent elapsed work, or dispatch a burst of assumed overdue effects. If the declared policy has an absolute deadline, report any expiry on activation without treating elapsed inactive time as robot work.
- Evidence/limits/cleanup: capture actual load/ticking transitions, rejected/permitted action traces, controls, current authorization, quantities, receipts, clocks and budget deltas for every variant in both server environments. Use finite original limits, retain evidence and restore the disposable fixture after quiescence. Orderly chunk unload/reload does not replace RCN-07's process/storage-failure tests.

## Review and execution gates

Resolve the [open review decisions](README.md#decisions-still-requiring-review), including contribution terms, exact toolchain, authority/resource bindings, save owners/restore lineage, measured limits and fault reachability before the corresponding integration work. Model results must identify their exact implemented subset; they cannot change a complete case to passed without its declared environments and oracles.

The [Decision Gate](../decision-gate.md) checks ADR documentation/bookkeeping. Its success does not execute these cases or verify the courier's technical behavior.
