# Integration Contract v0.1 — Design Proposal

**Status:** Proposed, unimplemented. Supports [ADR-0003](../decisions/0003-capability-driven-integration-ports.md) and Issue #2. This is a specification of *our* code boundaries, not a declaration of existing NeoForge/AE2 method signatures.

## Roles and trust boundaries

- **Player/owner:** chooses a goal, explicitly enrolls endpoints or networks, establishes allowed work zones and caps, may revoke access.
- **Controller:** maintains offline work orders, robot assignments and bounded planning; proposes operations but never directly mutates world state.
- **Capability catalog:** reports available operations based on the robot's installed modules and installed/validated adapters. Availability is not authorization.
- **Server action gateway:** the only intended entry point for game-state changes. Revalidates actor, target, module, enrollment, protection, loaded state, quantities and live security before effects.
- **Core executor:** implements vanilla courier, docking, cargo and later mod-owned work using Minecraft/NeoForge APIs.
- **Integration adapter:** version-scoped translator to a specific supported machine/network. It must never grant privileges, silently implement a substitute operation, or bypass the action gateway.
- **Target mod:** owns machine/grid state and its own security; its API result is not proof of successful physical delivery.

This architecture is a *requirement for later implementation*, not runtime-enforced today.

## Proposed stable interfaces (illustrative signatures only)

```text
OperationRequest {
  request_id: UUID; work_order_id: UUID; actor_id: UUID; owner_id: UUID;
  operation_id: namespaced_id; endpoint_id: persisted_locator;
  parameters: validated_bounded_data; expected_state_version?: long
}
OperationContext {
  server_world; work_zone; enrolled_endpoint; current_hardware;
  authorized_principal; adapter_compatibility; remaining_budget
}
OperationResult =
  COMPLETED(evidence, actual_delta) |
  ACCEPTED_PENDING(external_job_ref, evidence) |
  BLOCKED(reason, retry_hint) |
  RECONCILE_REQUIRED(reason, checkpoint) |
  FAILED(reason, no_unaccounted_effects_claim_if_proven)
CapabilityProvider.describe(endpoint, runtime) -> supported_operation_ids
ActionGateway.execute(request, context) -> OperationResult
OptionalAdapter.probe(runtime) -> COMPATIBLE | ABSENT | INCOMPATIBLE | DISABLED
OptionalAdapter.execute(request, authorized_context) -> OperationResult
```

These are conceptual Java-level ports; exact types, persistence format, thread confinement, and integration lifecycle are tasks for Issues #3 and #7. Generic item access and specialized AE2 crafting use different adapters behind the same gateway. Avoid overly generic arbitrary command dispatch; only allow registered, typed, bounded operations.

## Operation catalog (initially planned)

| Operation ID | Minimum capability | Target | Result interpretation |
| --- | --- | --- | --- |
| `modular_ai:inspect_inventory` | inspector / access to known endpoint | Vanilla or generic supported item handler | Observation; never permission |
| `modular_ai:extract_items` | cargo + manipulator | Enrolled source | Actual extracted amount and custody record |
| `modular_ai:insert_items` | cargo + manipulator | Enrolled sink | Actual inserted amount, remainder remains in custody |
| `modular_ai:dock_recharge` | docking + compatible battery | Mod-owned dock | Verified stored energy delta |
| `modular_ai:request_network_craft` | approved crafting-network integration | Enrolled AE2 endpoint | ACCEPTED_PENDING after confirmed submission, not completion |
| `modular_ai:inspect_craft_request` | approved crafting-network integration | Previously submitted request | Observed state, may be uncertain |

Use source/target allowlists, a bounded item predicate, quantity and time caps, and rate limits per work order. Network crafting and inspecting crafting requests are not first-prototype operations.

## Authorization and lifecycle

1. Enroll the source, destination, work zone and robot explicitly on the authoritative server. Store owner identity, endpoint locator (dimension, position or stable network identity), supported operation IDs, and configurable quantity/energy budgets. Revalidate the locator after load and after world changes.
2. Validate an idempotent request identifier and serialized intent. Deny unknown operation IDs or schemas; reject changed meaning when replaying a request ID.
3. Resolve the target only in a safely loaded, valid chunk. Do not force-load by default. Re-check that the enrollment is still valid; probe mod/version/adapter availability.
4. Check hardware, distance/path/range, scope and work budget. Query live server protection, actor and target-mod authorization through verified supported paths; **unknown authorization means deny**.
5. For inventory operations, validate stack identity, actual available counts, destination space and interface semantics. Use supported transactions on participating handlers. On partial success, persist actual custody and remainder; do not record requested quantity as accomplished.
6. Record effects and durable progress checkpoints before advancing a job. On reconnect/reload/unload, reconcile observations and current custody, not an optimistic cached success flag.
7. Report a stable result and user-readable reason. Retry only proven safe operations, with bounded backoff. Repeated uncertain effects must stay RECONCILE_REQUIRED until resolved by an authoritative observation or explicit recovery path.

## Conserving item custody

At each stable boundary: `source_reduction = robot_cargo_increase + other_proven_destination_increase` for successful extraction and `robot_cargo_reduction = destination_increase` for successful delivery, excluding any explicitly recorded, authorized transformation. Never count simulated transfers as effects. If two handlers cannot participate in one trustworthy atomic transaction, do not assume end-to-end atomicity: stage into owned robot cargo with per-step checks and test crash windows. A local log alone does not establish crash-safe atomicity; design write ordering after actual server/NeoForge persistence behavior is tested.

### Pending external jobs

For each external request persist a stable local request ID, submitted target, owner, input/output specification, network identity, adapter version, last confirmed external reference, and **uncertain-submission** state as necessary. Before retrying a request that may have been accepted, query the external system for a matching link/status; if no authoritative deduplication path exists, block rather than risk duplicate crafting. A successful response to submission is ACCEPTED_PENDING until confirmed output is reconciled. Never equate an asynchronous future or crafting link with delivered items.

## Isolation and permission matrix

| Condition | Expected core behavior | Adapter/job behavior |
| --- | --- | --- |
| No third-party content mods | Core starts and courier works | Adapter ABSENT; no specialized operations |
| Supported optional mod present, adapter disabled | Core works | DISABLED with explicit reason |
| Incompatible installed version | Core works if loader permits installation | INCOMPATIBLE; no class loading of unsupported API |
| Missing/destroyed machine or unloaded chunk | Other jobs continue | BLOCKED; no silent request submission |
| Permission denied or security check unavailable | Other jobs continue | BLOCKED, deny side effects |
| Network unpowered, no pattern or stock | Other jobs continue | BLOCKED with actionable reason |
| Partial or uncertain item transfer | Cargo tracked or recovery required | No success credit without proof |
| External request interrupted by restart | Core reloads | Reconcile using persistent external link; no blind retry |

A server owner may disable adapters. Integration discovery is a *capability probe*, not a bypass of enrollment. A player's enrollment does not establish external network authorization. Optional APIs stay out of shared DTOs, serialization, public core signatures and unconditional registries.

## Safety and performance limits

Disallow arbitrary commands, script evaluation, uncontrolled GUI clicking, unbounded searches and automatic factory expansion in the initial scope. Each world-modifying operation requires finite quantity, target, permitted zone and resource budget. Limit retry count and backoff, scanning/tick time, concurrent jobs, crafting quantity and robot count. Actual numeric defaults require profiling and balancing, not invented values.

## Open implementation work

Define Java records/interfaces and lifecycle hooks (Issue #3), owner and claims checks (Issue #7), concrete custody serialization/recovery tests (Issue #6), exact optional-mod classloader/metadata behavior (Issue #9), and AE2 provider bridge with an approved action source (separate scoped implementation after standalone prototype). Each must produce a testable code artifact; no Java implementation is claimed here.
