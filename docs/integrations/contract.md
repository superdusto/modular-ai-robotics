# Integration Contract v0.1 — Design Proposal

**Status:** Proposed, unimplemented. Supports [ADR-0003](../decisions/0003-capability-driven-integration-ports.md) and Issue #2. These interfaces and state names are **project design**, not actual Minecraft/NeoForge/AE2 declarations or working enforcement. The accepted [ADR-0002](../decisions/0002-standalone-core-optional-integrations.md) standalone, offline-first courier must work without AE2, hosted inference or internet.

## Roles, paths and non-model enforcement

- **Player/principal and owner:** explicitly authorize goals, enrollment, work zones and resource limits, with revocation. A consent click or claimed owner UUID alone does not prove the player may use an external grid owned by someone else.
- **Controller:** proposes bounded actions, retains offline work orders and statuses; it is not the permission oracle and cannot directly alter authoritative inventory.
- **Capability catalog:** reports registered operations for installed hardware and validated adapters; capability discovery is not permission.
- **Server policy and endpoint registry (to implement):** server-controlled enrollment and authority state tying principal, owner, operation, work zone, stable endpoint/network identity, quantity and revocation epoch. Check both at enrollment and on every use. Independent verified claim/protection providers supply additional decisions where required; absence, `unknown` or error cannot substitute for a network-owner right. AE2 `IActionSource` is provenance, not permission.
- **Server action gateway (to implement):** the exclusive intended server-side admission and accounting entry point for *both* controller-initiated requests **and incoming AE2 requester callbacks**. It independently rechecks actor, enrolled endpoint/network, live rights, protection provider, module, chunk, quantity, current resource state and durable identity before every scoped read/mutation. No adapter, callback or other executor may bypass this boundary.
- **Core executor:** performs vanilla courier, docking and cargo operations with actual Minecraft/NeoForge APIs; output is a measured physical effect, not a proposed amount.
- **Optional integration adapter:** performs version-scoped translations, including a server-owned AE2 requester/receiver; it cannot confer rights, fake player permission, unconditionally load optional APIs or create a second unaudited world mutation path.
- **Target mod:** owns its machine and grid state. Use *verified* target-mod authorization only when established for the selected version/action; do not presume an obsolete AE2 security station/grid-owner check or universal target-mod protection.

**Current enforcement strength:** design text only; no `P2` runtime gate exists yet. To meet the security invariant, code review and runtime tests must enumerate *all* authoritative reads and world/inventory mutation paths (including callbacks, recovery, cancellation and reconciliation), make the server admission boundary exclusive, and demonstrate denial even if the controller requests a forbidden action. Actual third-party claim-provider behavior remains version-scoped and unverified.

## Proposed stable interfaces (illustrative signatures only)

```text
OperationRequest {
  request_id: UUID; work_order_id: UUID; actor_id: UUID; owner_id: UUID;
  operation_id: namespaced_id; endpoint_id: persisted_locator;
  parameters: canonical_validated_bounded_data; expected_state_version?: long
}
OperationContext {
  authoritative_server_world; work_zone; enrolled_endpoint_network_binding;
  authorized_principal_and_owner; current_hardware; revocation_epoch;
  verified_protection_decisions; adapter_compatibility; remaining_budget
}
OperationResult =
  COMPLETED(proven_evidence, actual_delta) |
  ACCEPTED_PENDING(external_job_ref_if_confirmed, evidence) |
  BLOCKED(reason, retry_hint) |
  RECONCILE_REQUIRED(reason, durable_receipt_if_available) |
  FAILED(reason, proven_effect_and_custody_disposition)
CapabilityProvider.describe(endpoint, runtime) -> supported_operation_ids
ActionGateway.authorize_and_execute(request, live_context) -> OperationResult
ActionGateway.receive_external_callback(callback, live_context) -> actual_accepted_amount_or_zero
OptionalAdapter.probe(runtime) -> COMPATIBLE | ABSENT | INCOMPATIBLE | DISABLED
OptionalAdapter.execute(authorized_request) -> OperationResult
OptionalAdapter.receive_callback(authorized_callback_context) -> actual_accepted_amount_or_zero
```

The callback contracts are **conceptual**, not AE2 Java signatures. The actual AE2 requester callback is synchronous and returns a number; future implementation must verify server-thread handoff and that it can return only after a proven physical acceptance. The possible helper interface above must not be read as an available library method. Exact types, storage format, scheduling, concurrency and save semantics are implementation work under Issues #3, #6 and #7.

## Operation catalog

| Operation ID | Minimum capability | Target | Successful interpretation |
| --- | --- | --- | --- |
| `modular_ai:inspect_inventory` | inspector + verified scoped right | Enrolled vanilla or supported handler | Authorized observation only; no ownership inference |
| `modular_ai:extract_items` | cargo + manipulator | Enrolled source | Physical source reduction and custody-increase evidence |
| `modular_ai:insert_items` | cargo + manipulator | Enrolled sink | Physical insertion evidence; remainder stays in custody |
| `modular_ai:dock_recharge` | docking + compatible battery | Mod-owned dock | Actual energy delta |
| `modular_ai:request_network_craft` | verified network authorization + adapter | Enrolled AE2 bridge/network | Confirmed submission gives `ACCEPTED_PENDING`, not delivered items |
| `modular_ai:inspect_craft_request` | scoped prior request right | Earlier authorized request | State read; may be uncertain |
| `modular_ai:receive_network_output` | **internal server-only callback route** | Persistable owned AE2 staging buffer | Actual physically accepted quantity per key; never a controller-issued public action |

All item identities and quantities, input/destination selectors, energy, scan radius and recursion are bounded; numeric limits must be measured rather than invented. No first-courier dependency on AE2 or generic third-party automation.

## Authorization and lifecycle (F1/F2)

1. **Enroll:** On the server, verify actor and owner privilege for the **specific** source/sink or attached network, zone, requested operations and any applicable separate claim-provider right. Store the verified binding and revocation scope; deny foreign network control that the server cannot independently establish. Physical possession of a bridge, claimed identity, exposure of a capability or provider absence alone is insufficient.
2. **Identify request:** Check a stable `request_id`, canonical intent, persisted outcome, owner and original authorization scope **before** any effect. Reject unknown action/schema; changed intent with the same ID is a collision (never a new operation). See replay state below and `INT-04B`.
3. **Resolve:** Read only a live, safely loaded validated target; do not force-load by default. Validate stable dimension/endpoint/network fingerprint and registration/version lifecycle after reconnect, relocation or replacement.
4. **Authorize at use:** Independently check current principal and owner, enrollment, zone, hardware, rate/cost limits, relevant server rules and verified applicable protection/target-mod rights, including rights revoked since submission. If required authorization is denied, unknown, errored or no longer provable, fail closed with a reason. A claim provider allowing a place does not independently authorize using a different owner's AE2 grid.
5. **Apply measured mutations:** For a compatible source/destination handler, use version-correct transaction APIs only with known participating handlers, bound to the authorized resource and actual capacity. Never assume a multi-tick courier movement is atomic; record actual extraction into robot cargo and actual later deposit separately. Partial result credits only the observed physical delta.
6. **Admit callbacks separately:** AE2 may call `insertCraftedItems` without a new controller action. Bind the received link/key/amount to the original authenticated request, endpoint/network and owner; recheck all live permissions and stage output only on the supported authoritative server execution path. Never bypass (2)–(5) because the entrypoint is a callback.
7. **Resolve results:** `COMPLETED` only on proven postcondition and item custody. `ACCEPTED_PENDING` only on confirmed accepted work lacking final output. `BLOCKED` denotes no new forbidden effect only when that absence is proven; if a mutation may have happened, return `RECONCILE_REQUIRED`, not optimistic `FAILED` or `COMPLETED`. `FAILED` must retain proven prior effects and cargo (if any). Release/transfer of quarantined output is itself newly authorized work.
8. **Recover:** Compare durable work record with *actual* source, robot, staging and sink inventories and external links. A read, simulation, speculative API response or terminal job state is not a success oracle. Never automatically replay uncertain effects; any safe retry must be bounded and idempotency-proven.

## First-courier idempotency contract (proposed; F4)

Use a **stable owner-scoped `request_id`** and durable canonical-intent hash of operation ID, owner/principal, item key including components, amount, source/destination endpoint and authorized work-scope/version at original admission. Persist request records before effects where the implementation supports it, but do **not** assert an atomic compare-and-write, lease, crash flush or exactly-once execution that has not been demonstrated.

| Durable logical state | Same ID + same canonical intent | Same ID + different canonical intent |
| --- | --- | --- |
| `not_seen` | Evaluate authorization and create the first request if it can be durably admitted | Not applicable without an existing record; avoid trusting caller's assertion |
| `accepted_or_in_progress` | Return existing pending result; **no second mutation** | Reject ID collision |
| `completed_with_proven_effects` | Return retained result and measured receipt; **no second mutation** | Reject ID collision |
| `blocked_no_effect` | Return recorded block without executing; a fresh authorized request requires a new ID | Reject ID collision |
| `uncertain_effect` | `RECONCILE_REQUIRED`; do not replay until authoritative reconciliation proves safe transition | Reject ID collision; preserve uncertainty |

`blocked_no_effect` is legal only with a verified zero-effect observation; crash after possible world mutation cannot default to it. If write ordering/atomicity fails to distinguish `not_seen` from an unrecorded effect after an abrupt crash, block automatic retries and use physical reconciliation. Retain completed IDs and tombstones long enough to cover configured retry horizon, unloaded world state and post-crash recovery; define and test bound, pruning, epoch and backup-restore behavior **before** enabling deletion/reuse. An unknown record after pruning is not a safe `not_seen`. Revocation stops future effects regardless of stored successful authorization; an already proven completion may still return its old receipt without new access. **`INT-04B` is mandatory for the first vanilla courier, independent of `INT-14` multi-robot coordination.**

## Conserving custody, asynchronous callbacks and abrupt crash (F2/F3)

For a conserved item key, use observed physical `source + robot_cargo + staging + destination` totals and account explicitly for proven external creation/consumption or authorized conversion; record in-flight/uncertain quantity separately and **never insert a guessed amount into the physical sum to hide a mismatch**. After extraction, source decrease must be explained by observed custody increase or a recorded `RECONCILE_REQUIRED` anomaly. After deposit, actual cargo decrease must equal measured sink increase or remain unresolved. A work order's `COMPLETED` credit may not exceed actual delivered quantity. Protect previously accepted custody even after a permission revocation, cancellation or terminated AE2 link.

**AE2 receiving default:** One server-owned persistable staging buffer per enrolled bridge/request mapping, not direct robot cargo. For `SIMULATE`, return calculated admissible amount without any inventory, ledger, reservation, work-order or permission-state mutation. For `MODULATE`, on a verified safe server execution path, revalidate original link/key/owner/current authorization, return only the amount physically inserted up to available capacity/outstanding request; return `0` when full, denied, mismatched, unloaded or callback-scheduling constraints are unresolved. Store per-key accepted, expected and outstanding quantities and a durable terminal receipt; a canceled/dead link must not erase prior staging cargo or create completion. Revocation blocks new deliveries while prior cargo remains quarantined/recorded. See [AE2 plan](ae2-first-adapter.md).

**Crash durability is unproved.** NeoForge 26.1 [transactions](https://docs.neoforged.net/docs/inventories/transactions/) handle participating snapshot-aware resource handlers; they do not supply durable atomic commit across world save, request record, robot cargo, destination and AE2 callback ledger. The future implementation must define and instrument before/after extraction, insertion, checkpoint creation and *actual persistence/flush* (if observable), including after-partial-transfer and after-cancel windows. Abruptly terminate process without orderly save, reload a disposable world, inspect physical stores, repeat recovery and block ambiguous replay. A local journal cannot alone guarantee disk durability or distributed rollback. Any unsupported window must be `BLOCKED` for the relevant claimed safety guarantee; manual/admin reconciliation may be required. `INT-04` (graceful) does not replace `INT-04A` (abrupt); `INT-04B` (single courier replay) is the same initial release gate.

## Pending external jobs

Before an AE2 craft is submitted, retain the request's canonical intent, original owner/principal, network binding, expected item keys/amounts, revocation context, actual confirmed external crafting ID/link (when available), receiver mapping and uncertainty state. If the submit response may have been lost, query a *verified authoritative* matching link before retry; otherwise `RECONCILE_REQUIRED` and no duplicate submission. `getRequestedJobs()` may reattach persisted live links, but `jobStateChange` ends use of a live link; an independent retained custody/reconciliation record remains. `ACCEPTED_PENDING` never implies finished delivery. Unknown AE2 callback retry, atomicity or server-thread guarantees block claims of safe automated output delivery until tested.

## Isolation and permission matrix

| Condition | Core behavior | Integration behavior |
| --- | --- | --- |
| No optional content mods / offline | Standalone courier remains usable | AE2 absent, specialized operations not offered |
| Optional adapter disabled or incompatible | Core fallback when loader permits this installation | No unsupported class load; clear reason, test `INT-08` |
| Endpoint/network removed, different, unloaded or unpowered | Other jobs continue | New operations `BLOCKED`; existing effects accounted; unknown prior effects `RECONCILE_REQUIRED` |
| Foreign network with no verifiable owner authorization | Core remains usable | No enrollment/read/extraction/craft; independent permission proof required |
| Claim provider missing, denying, unknown or errored | Server-owned policy still applies | No inferred access; block any operation whose external right cannot be established |
| Rights revoked while crafted cargo already staged | Core retains custody records | New callback acceptance zero; existing staged cargo quarantined, no deletion |
| Partial, canceled or dead external craft | Cargo remains tracked | No terminal-driven `COMPLETED` or lost accepted output |
| Uncertain transfer/submission/replay | Preserve durable request ID and observed physical facts | `RECONCILE_REQUIRED`, no blind duplicate attempt |

No third-party API in public core DTOs or unconditional registry signatures. Do not use FakePlayer impersonation, arbitrary GUI driving, script evaluation, silent fallback to another operation, unlimited retry or unbounded chunk loading. Quantitative budgets are established by future profiling.

## Open implementation work and gates

Implement core server gateway and owner/claim checks (Issues #3 and #7); vanilla custody, first-courier replay and fault-injection persistence harness (Issue #6); optional metadata/class-loading proof (Issue #9); and a separate version-scoped AE2 bridge/receiver. The required ordered [verification matrix](verification-matrix.md) gates are `first_courier` (`INT-04`, `INT-04A`, `INT-04B` included), then `generic_external_handler`, then `ae2_specialized`, with `INT-14` multi-robot coordination later. All remain `NOT RUN`; a passing Decision Gate is not gameplay evidence.
