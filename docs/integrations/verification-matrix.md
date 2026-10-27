# Issue #2 Verification Matrix — Unrun

**Scope:** executable-future acceptance cases for the proposed [ADR-0003](../decisions/0003-capability-driven-integration-ports.md), [integration contract](contract.md), [AE2 adapter plan](ae2-first-adapter.md), and [standalone verification plan](../verification-plan.md). **Every row and fault subcase is `NOT RUN`.** This document is neither test evidence nor proof that a Minecraft mod exists.

**Evidence protocol:** Execute in disposable worlds at recorded Minecraft/NeoForge/JDK, project commit/build and optional-mod versions. For each case capture principal, policy/provider status, endpoint/network identity, operation and `request_id`, injected fault/actual restart mode, source + robot cargo + staging + destination inventories per item key, external job state where applicable, persistent request/custody record, response/callback return, server logs and recovery outcome. An unknown or inaccessible physical delta remains `RECONCILE_REQUIRED`, never presumed zero. Runtime rows pass only with reproducible, linked evidence; no design, mock, CI governance run or clean shutdown substitutes for an actual world trial.

| ID | Environment and setup | Input, procedure or fault | Objective oracle and acceptance | Gate | Status |
| --- | --- | --- | --- | --- | --- |
| INT-01 | 26.1.2 + NeoForge + core only; client and dedicated server | Spawn courier/dock, use two enrolled vanilla containers | Both launch; basic courier works; physical inventory counts match request records | `first_courier` | NOT RUN |
| INT-02 | Same; network disconnected | Reboot offline, use and save courier | No hosted account/inference dependency; local state persists | `first_courier` | NOT RUN |
| INT-03 | Vanilla containers, bounded requests | Empty source; full/partial source; full/partial destination | Exact actual amounts and remainders; no loss, duplication or false `COMPLETED` | `first_courier` | NOT RUN |
| INT-04 | Vanilla courier, controlled orderly save | Stop *gracefully* after pickup and after deposit; reload | Saved cargo, source, sink and work-order record reconcile; no repeat effect | `first_courier` | NOT RUN |
| INT-04A | Disposable vanilla world; instrumented process termination and restart | Abrupt crashes at each `INT-04A-01`–`INT-04A-12` fault point below | Exact physical balances and durable result after unclean restart; uncertainty blocks replay; bounded recovery or documented manual reconciliation | `first_courier` | NOT RUN |
| INT-04B | Single vanilla courier; same persisted request namespace | Replay identical completed ID, changed-intent ID, pending ID, crash-uncertain ID | Stored proven result/no second effect; collision denied; uncertain blocked pending reconciliation; works with one robot and no AE2 | `first_courier` | NOT RUN |
| INT-05 | Vanilla with configured server policy and, where supported, optional claim provider | Denied, revoked, invalid-zone, absent/unknown/error provider; unload | No unauthorized mutation; `BLOCKED` with reason; no claim-provider outage becomes implied approval | `first_courier` | NOT RUN |
| INT-06 | External NeoForge 26.1 `ResourceHandler<ItemResource>` | Authorized sided, partial transfer, denial and changed target | Actual source/cargo/sink counts; no bypass of gateway/permissions | `generic_external_handler` | NOT RUN |
| INT-07 | No content mods | Inspect core class linkage and launch both sides with absent optional APIs | Standalone startup/progression without eager optional-class loading | `first_courier` | NOT RUN |
| INT-08 | Optional mod absent, compatible/disabled, present-incompatible | Probe metadata/loader/class loading and core fallback | Core remains usable in loader-supported configurations; incompatible cases documented, not presumed safe | `generic_external_handler` | NOT RUN |
| INT-09 | AE2 v26.1.13-beta; verified same-owner bridge/network, policy and protection evidence | Enroll then inspect approved stock, no craft | Enrollment and each observation independently authorized; no implied AE2 security-station check | `ae2_specialized` | NOT RUN |
| INT-09A | AE2 network of another player, enrolled or unenrolled | Attempt enroll, inspect, extract and craft | Each unsupported right fails closed; zero unauthorized reads/effects/submissions; attributable denial | `ae2_specialized` | NOT RUN |
| INT-09B | AE2 with no provider, then provider allow/deny/unknown/error | Repeat enrollment, inspection, extraction and craft with same policy/identity binding | No-provider/unknown/error does not confer external ownership; allow only when independent server policy and applicable provider jointly authorize | `ae2_specialized` | NOT RUN |
| INT-09C | AE2 endpoint/network changed or rights revoked after enrollment | Reconnect, inspect, extract and request crafting | Revalidate network binding and rights at use; zero unauthorized effects | `ae2_specialized` | NOT RUN |
| INT-10 | Authorized AE2 requester and known pattern | Asynchronous plan, bounded submit, lost/uncertain submission response | Exactly one confirmed submission or `RECONCILE_REQUIRED`; `ACCEPTED_PENDING` is not delivered cargo | `ae2_specialized` | NOT RUN |
| INT-10A | AE2 requester; controlled staging capacity | Call `insertCraftedItems` with `SIMULATE`, then full-buffer `MODULATE` | Simulation changes no durable/cargo/policy state; full buffer accepts/returns 0; returned quantity equals physically accepted amount | `ae2_specialized` | NOT RUN |
| INT-10B | AE2 requester with bounded buffer | Multiple partial `MODULATE` callbacks; wrong key/link; cancellation and `jobStateChange` | Only accepted physical cargo is credited; wrong key/link returns 0; terminal event never invents delivery or discards accepted custody | `ae2_specialized` | NOT RUN |
| INT-10C | AE2 job active, owner authorization changed or endpoint unloaded | Revoke owner policy after first delivery, invoke callback again; unload/reload | Prior custody retained/quarantined; new unauthorized/unloaded callback accepts 0; reason recorded | `ae2_specialized` | NOT RUN |
| INT-11 | AE2 requester link persisted through unload/restart | Reattach via `getRequestedJobs`; response lost, link cancelled/dead | No blind re-submission; persisted per-key accepted, remaining and uncertain quantities reconcile | `ae2_specialized` | NOT RUN |
| INT-11A | AE2 callback interrupted or repeated during process failure | Inject crash between callback inventory and durable record; repeat callback/recover | No false acceptance or duplicate delivery; if AE2 retry guarantee or atomicity unproved, block feature rather than mark pass | `ae2_specialized` | NOT RUN |
| INT-12 | AE2 unpowered, missing pattern/input, full/disconnected output | Request/observe denied or impossible work | Clear block/partial reason, zero false completion or quantity credit | `ae2_specialized` | NOT RUN |
| INT-13 | AE2 removed/changed with pending work | Reload a world that can otherwise load without AE2 | Core survives; external job and accepted cargo remain unresolved, not discarded | `ae2_specialized` | NOT RUN |
| INT-14 | Two+ robots; later coordination milestone | Concurrent requests, contention, reservations and budgets | No cross-robot duplicate effects or budget overruns; distinct from single-courier `INT-04B` | `multi_robot_later` | NOT RUN |

## Abrupt-crash injection subcases for INT-04A

All subcase IDs are independently reportable; each has status `NOT RUN`. The harness must terminate the process **without an orderly world save**. After every restart, observe actual persisted counts and records, then attempt bounded reconciliation and a second restart. Do not use a clean stop as a substitute. For all cases, an unprovable effect is `RECONCILE_REQUIRED`; no automatic re-extraction/reinsertion or fictitious conservation via an in-flight counter.

| Subcase | Injected boundary | Additional oracle | Status |
| --- | --- | --- | --- |
| INT-04A-01 | Immediately before actual extraction mutation | No unauthorized decrement or success credit | NOT RUN |
| INT-04A-02 | Immediately after extraction, before next proven durable checkpoint | Observed source/cargo delta reconciled; no second extraction | NOT RUN |
| INT-04A-03 | Immediately before destination insertion mutation | Cargo remains accountable; no false delivery | NOT RUN |
| INT-04A-04 | Immediately after insertion, before next proven durable checkpoint | Observed destination increase; no second insertion | NOT RUN |
| INT-04A-05 | Immediately before checkpoint construction | No assumed durable progress | NOT RUN |
| INT-04A-06 | Immediately after checkpoint construction, before actual save/flush | In-memory checkpoint not counted as durable | NOT RUN |
| INT-04A-07 | Immediately before observable persistence/flush boundary | Record evidence of what actually reached durable storage | NOT RUN |
| INT-04A-08 | Immediately after observable persistence/flush boundary | Re-read persisted state; do not assume flush unless verified | NOT RUN |
| INT-04A-09 | Between steps of a partial transfer | Preserve proven remainder, actual cargo and blocked/uncertain state | NOT RUN |
| INT-04A-10 | During a cancelled operation with prior physical effect | Preserve custody, no completion from cancellation | NOT RUN |
| INT-04A-11 | During unload/reload around a mutation | No forced chunk load or silently continued action | NOT RUN |
| INT-04A-12 | After an uncertain restart, repeat recovery and replay original ID | No additional physical effect or guessed success; bounded/admin reconciliation | NOT RUN |

If a deterministic fault point, actual save/flush observation, safe world snapshot or reliable post-crash inventory observation is unavailable, report that precise subcase as `BLOCKED` in a future result with the missing harness/proof. Its planned status here remains `NOT RUN`.

## Gate sequencing

1. **First standalone courier (no AE2 or second robot):** `INT-01`, `INT-02`, `INT-03`, `INT-04`, `INT-04A` (all twelve subcases require evidence; any critical blocked subcase holds the crash-safety release gate), `INT-04B`, `INT-05`, `INT-07`. Release requires credible crash/replay integrity evidence; blocked critical fault windows block the corresponding crash-safety release claim, not silently waive it.
2. **Generic external-handler capability:** `INT-06`, `INT-08`, after the first-courier security/accounting boundary is implemented. External handler compatibility does not approve AE2 crafting.
3. **AE2 specialized capability:** `INT-09`, `INT-09A`, `INT-09B`, `INT-09C`, `INT-10`, `INT-10A`, `INT-10B`, `INT-10C`, `INT-11`, `INT-11A`, `INT-12`, `INT-13`. All must pass for the explicitly advertised supported scenario; missing independent network authorization, server-thread callback execution, callback persistence atomicity/reconciliation or duplicate-delivery safeguards blocks the affected AE2 feature.
4. **Multi-robot later:** `INT-14`. This deferral **does not defer `INT-04B`**.

The `first_courier` milestone must not claim exactly-once crash-safe world mutations based solely on a journal or NeoForge resource transaction. Required properties are no demonstrable item duplication/loss or unsupported success for claimed supported crash windows, no blind replay of uncertain effects, and bounded reconciliation. If technical constraints prevent a proven property, hold the feature/release gate and surface a maintainer decision; do not turn an unsupported case into a `PASS`.
