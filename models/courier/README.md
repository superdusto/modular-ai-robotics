# Standalone courier model (candidate)

This is `mar-courier-kernel-candidate@0.2.0`, an in-memory Java design model with 27 scenarios and 210 assertions. It exercises quantities, control fences, retained-cargo recovery and bounded retry timing. It is not a Minecraft mod or a production courier implementation.

The design references are the [owner-selected first courier scope](../../docs/courier/README.md) and [proposed engine contract](../../docs/courier/contract.md). Importing this candidate does not adopt every detailed contract rule or ADR-0003. Complete [RCN-01–RCN-10 cases](../../docs/courier/verification.md) remain not_run.

## Authorization and contribution review

On 2026-10-28, superdusto authorized bringing the existing standalone model and checks into the repository, making the instructions portable, rerunning checks and opening a draft PR. The [authorization record in issue #9](https://github.com/superdusto/modular-ai-robotics/issues/9) tracks that model-only scope. NeoForge scaffolding, client/server startup and real Minecraft integration remain separate steps requiring authorization.

This is an agent-authored record of the owner's project-chat approval, not a GitHub approving review or a human contribution-rights declaration. The [contribution policy](../../CONTRIBUTING.md#human-authority-and-express-assent) still requires an actual human declaration covering the final contribution revision before acceptance. Reserved asset paths in this submission: **NONE**.

## Run the checks

With Python 3 and an installed JDK 25, run from the repository root:

```sh
python3 -B models/courier/run-model.py
```

The runner selects `MAR_JAVA_HOME`, then `JAVA_HOME`, then `javac` on PATH, and uses that compiler's sibling JVM. An explicitly selected home is authoritative: an invalid or different-major JDK fails without falling back. Both compiler and runtime must be major 25; compilation uses `--release 25`. No dependency manager, Minecraft installation or network access is needed to run the model with those tools already installed.

Compiled classes live in a temporary directory cleaned on success or failure. Each run replaces the ignored `build/courier-model/model-results.json` report, including failed runs. Report schema 2 records execution time, compiler/runtime versions, SHA-256 hashes of the three Java sources, runner and scenario manifest, stable scenario IDs, assertion counts, baseline coverage and evidence limits. Known-gap observations are separate from the 27-scenario result and explicitly marked `observed_unfixed`. Reports are run observations, not committed fixtures. Use `--report PATH` for a different output path; a relative override is relative to the caller's working directory.

The [reviewed baseline manifest](scenario-baseline.json) requires M01–M27, their original names, each scenario's reviewed assertion minimum and at least 210 total assertions. IDs are explicit in the harness and remain stable if cases are reordered or extended. Counts must agree with the per-ID results. Removing cases, reusing IDs or replacing a substantial scenario with one trivial assertion fails the runner even when the harness reports its reduced list as passed. This is a retention guard, not proof that an assertion is meaningful or that the contract is correct; manifest/oracle edits still require review.

Run the coverage-guard regressions without a JDK:

```sh
python3 -B models/courier/test_runner.py
```

The [Courier Model workflow](../../.github/workflows/courier-model.yml) runs the coverage-guard regressions and the same model command with Temurin JDK 25 on Ubuntu, writing the JSON report into its log. Both actions are pinned to full commits; the Java setup pin is [setup-java v6.1.0](https://github.com/actions/setup-java/releases/tag/v6.1.0). Its reported JDK patch/build is an observation of that run, not a NeoForge project toolchain pin. The existing Decision Gate remains separate.

## Import provenance

`CourierKernel.java` preserves the earlier local v0.2.0 source byte-for-byte after the added MIT copyright/SPDX header. At the initial import, [5f765847](https://github.com/superdusto/modular-ai-robotics/commit/5f765847cde9f4ca5556dd89334c98391ff80e5e), the scenario harness also matched its original bytes. The review revision adds stable IDs and per-scenario assertion reporting to that harness; its original scenario bodies and 210 assertion executions are retained. A separate known-gap harness reproduces lifecycle defects. The original source hashes, before headers and those harness-reporting changes, are:

| Source | SHA-256 |
| --- | --- |
| CourierKernel.java | `ab1b6132ed1aa00b2d3ad46f684434189d6d422581f55844df13cb587c0917fe` |
| CourierKernelChecks.java | `38d52022571a0d2a83877ca2ea1255fc7005ff6822808c50fd264ae46f9ae5c0` |

The runner is adapted for JDK discovery, caller-independent source paths, ignored reports, failure reporting and independent baseline enforcement. Kernel behavior is unchanged. Original MAR material is covered by [MIT](../../LICENSE), with public credit superdusto. No artwork, sounds, upstream implementation or third-party source is included.

## Recovery behavior

A simulated restoration copies consumed budgets, attempt history, logical clock and item receipts, then fences physical dispatch and invalidates destination-context freshness. Even numerically consistent cargo cannot resume automatically.

The current owner must submit a new command at the expected control revision with a distinct continuation attempt and attributable, independently readable cargo evidence. The evidence must identify the same job/request and agree with its existing extraction, delivery and actual cargo. Validation consumes the original finite recovery pass/read/work reserve. Denied reads consume their allowance; unauthorized controllers cannot spend it. Missing attribution or a wrong lineage remains blocked.

After successful validation, the job retains its original completed extraction and current cargo. Fresh destination context is still required before inserting only the remainder. Replaying an old navigation result does not establish current arrival; replaying an old successful continuation cannot clear a newer stop. Cancellation, unresolved effects, failed record writes, spent delivery/recovery limits and partial pickups lacking a completed-load certificate remain blocked.

CargoEvidence and Context emulate trusted fixture evidence. They are not client authentication, provider hooks or proof that aggregate counts can resolve an unknown effect. This model never clears uncertainty or repairs physical stores from matching totals.

## Retry and time behavior

The default synthetic fixture allows three total insertion attempts, with declared waits of two and four logical active ticks, an overall active limit of 100 ticks, and a no-material-progress limit of 20 ticks. These are model inputs, not proposed production defaults or measured Minecraft performance. The larger receipt-pressure fixture explicitly uses a separate finite retry policy.

An early eligibility query returns RETRY_WAIT without invoking an effect, consuming an insertion attempt or reserving that operation ID. At its due tick, the queued identity may invoke one bounded attempt. A zero or partial result consumes an attempt; positive material transfer alone advances the no-material-progress boundary. Owner continuation, new IDs and restoration reset neither spent attempts nor deadlines. Attempt limits are cumulative across batches of the original job; a new pickup is blocked when no insertion allowance remains.

advanceActiveTicks advances only the harness's explicit logical active clock. It performs no sleeping, wall-clock inference or unloaded entity work. Snapshot copies retain the current clock and next retry time. The overall active deadline blocks normal delivery/service; finite record controls and authorized evidence work retain their separate gates. Separately authorized safety service remains bounded by its own allocation and relevant resolved context.

## Executed scenarios

M01–M27 identify the retained baseline in this model version. They are not executions of complete RCN/CV/PK cases. The harness reports explicit IDs, names and executed assertion counts; the runner checks them against the reviewed manifest.

| ID | Scenario |
|---|---|
| M01 | Full delivery also requires normal dock/charge completion |
| M02 | Source shortfall needs owner continuation and fresh batch certificates |
| M03 | Capacity-limited batch stays distinct from source shortage |
| M04 | Nonterminal partial pickup retains cargo and blocks downstream/top-up |
| M05 | Partial unload blocks normal return; safety service grants no normal DAG credit |
| M06 | Restored retained cargo needs owner validation before delivery |
| M07 | Cancellation during unknown effects remains fenced and unresolved |
| M08 | Stop remains available after work exhaustion; failed writes fence service |
| M09 | A newer stop rejects stale resume |
| M10 | Denied recovery reads consume protected reserve; restoration cannot renew it |
| M11 | Unknown physical prerequisites or missing budget history block effects |
| M12 | Continuation receipts cannot consume protected stop capacity |
| M13 | Control retention exhaustion refuses resume before losing future stop capacity |
| M14 | Operation/request collisions reject changed intent |
| M15 | Completed jobs and closed batches cannot restart normal work under new IDs |
| M16 | Retained-cargo continuation needs current owner rights and fresh destination context |
| M17 | Denied reads, matching unattributable totals and wrong lineage cannot clear recovery |
| M18 | Cancellation and unknown effects cannot be laundered through recovery evidence |
| M19 | Replayed recovery command cannot undo a newer stop |
| M20 | Increasing retry waits, attempts and due ticks survive restoration |
| M21 | Owner/restoration cannot renew exhausted insertion attempts |
| M22 | Zero effects and new IDs do not extend a no-progress deadline |
| M23 | Active deadline blocks delivery while bounded recovery and stop remain available |
| M24 | Actual material progress advances the progress boundary without renewing attempts |
| M25 | Partial-pickup cargo cannot become a completed load through recovery |
| M26 | Invalid retry policies and backwards clock changes reject |
| M27 | Owner continuation cannot start a pickup after cumulative insertion exhaustion |

## Remaining boundary

The model has fixed synthetic bindings and one exact item profile. It does not implement real enrollment/authentication, providers, components/codecs, route geometry, energy supply accounting, concurrent executors, disk serialization, crash consistency or a pack importer. Its constructor is not a server-wide admission/replay registry. Snapshot copying represents a fenced activation scenario, not actual durable recovery or a proof that only one physical embodiment exists.

Full RCN/CV/PK cases retain their original not_run/not_executed statuses. These observations cover selected model portions of RCN-01–RCN-05, with no inherited runtime result. Earlier local prototypes and research artifacts are not redistributed by this import.

## Model behavior requiring further review

This candidate implements selected rules rather than full contract conformance. In particular:

- `continueBatch` permits owner-authorized continuation after successful unload without requiring HOME/CHARGE certificates. The proposed contract describes continuation after batch service. The existing receipt-pressure and cumulative-attempt scenarios also use this simplified sequence; passing them does not prove the stricter service gate.
- **P2-01:** `snapshotCopy` requires recovery for zero-cargo jobs before their first pickup, after successful unload before HOME/CHARGE, and after service closes an incomplete batch. Retained-cargo recovery rejects zero cargo; ordinary resume and batch continuation cannot clear the recovery flag. Physical dispatch remains blocked by recovery or the closed-batch guard. The gap is broader than empty closed batches. Do not clear the fence merely because cargo is zero; current rights, attributable custody/receipts and the original budgets/timing still need a validated recovery path.
- **P2-02:** after delivery and service set SUCCEEDED, a new authorized `stop` can overwrite it with SUSPENDED (pause) or CANCELLED. Item quantities and spent physical work remain unchanged, but the final job verdict and control epoch change. The proposed correction is a terminal rejection/no-op response for a new post-completion control, preserving SUCCEEDED, cancellation state, epoch, receipts and accounting. This is a follow-up oracle for review, not behavior implemented or newly adopted by this import.
- **Additional Astra P2 (KG06):** `continueBatch` checks only that production work is nonzero. With a request of 16, capacity 8 and an initial production allowance of 4, the first eight items can be delivered and HOME/CHARGE completed with one production unit left. Continuation is recorded and the second pickup spends that last unit; destination navigation is EXHAUSTED and eight items remain aboard. This is independent of the missing HOME/CHARGE gate. A remainder of two units similarly permits pickup/navigation but exhausts at unload. Three units complete this fixed synthetic pickup/navigation/unload path, with separately sufficient service work. These are model-boundary observations, not production budget defaults or a guarantee of sufficient real-world work. The follow-up must validate or reserve sufficient declared work before admitting another pickup without renewing the original limits.

The separate [known-gap harness](CourierKernelKnownGapChecks.java) reproduces these lifecycle defects:

| ID | Observation of the unfixed candidate |
| --- | --- |
| KG01 | Empty restoration before first pickup stays fenced with no recovery path |
| KG02 | Empty restoration after unload before HOME/CHARGE stays fenced |
| KG03 | Empty restoration after service of an incomplete batch stays fenced |
| KG04 | A new pause overwrites a completed job's SUCCEEDED status |
| KG05 | A new cancellation overwrites a completed job's SUCCEEDED status |
| KG06 | Continuation admits cargo with insufficient work; remainders of one/two strand it, while three complete the fixed path |

These observations assert the current gaps and unchanged item accounting; they are not passing desired recovery/terminal-state/budget-admission scenarios. A green candidate run means the baseline was retained and the listed defects were reproduced. KG06 includes a sufficient-work boundary as a control, without treating assertion totals as a quality target. When fixing a gap, replace its observation with reviewed desired-behavior regressions and update the manifest deliberately. Behavioral corrections, including the earlier service gate, are tracked separately in [issue #23](https://github.com/superdusto/modular-ai-robotics/issues/23).

These are review findings in the preserved candidate, not demonstrated Minecraft defects or newly adopted product behavior. Reconcile them with the proposed contract and add appropriate regression scenarios before claiming those rules implemented. The initial review can distinguish preserving this model for reproducibility from accepting it as a production API.

The next environment milestone is a separately authorized, pinned Minecraft 26.1.2/NeoForge workspace on JDK 25, followed by a minimal build and isolated client/server startup. Real authority, resources and save ownership must be bound and tested before this model can become a live courier.
