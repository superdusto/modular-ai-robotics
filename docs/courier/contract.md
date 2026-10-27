# Proposed courier engine contract

**Status: Proposed, 2026-10-27.** The owner-selected [initial scope](README.md) uses one bounded-batch policy with owner-authorized continuation. The detailed contract below remains subject to the listed review decisions. It describes intended behavior, not implemented server enforcement or a durability guarantee.

The contract supports [requirements R-001–R-009](../requirements.md) and the accepted platform/standalone choices in [ADR-0001](../decisions/0001-initial-platform.md) and [ADR-0002](../decisions/0002-standalone-core-optional-integrations.md). It does not change [ADR-0003](../decisions/0003-capability-driven-integration-ports.md)'s proposed status or select a pack schema/registry version.

## Intent identity and custody

Bind server/world lineage, original request/job identity, canonical intent, robot UUID and unique embodiment, controller authority and original cargo beneficiary. Intent includes exact item/components, requested quantity, endpoint incarnations and interaction contexts, work area, route/dock, allowed operations, policy and original finite limits. Two endpoint references must not alias one backing inventory or robot cargo.

Keep command, continuation-attempt, DAG-node and physical-effect operation identities distinct. A duplicate operation returns its retained evidence without repeating the effect; changed intent under that identity collides. A proven zero or partial outcome may permit a new bounded attempt. Unknown outcome is never made retryable by changing an ID.

New ownership, enrollment or commands do not inherit rights to old cargo. Missing/duplicated embodiments, incompatible restore lineage and missing replay history block dependent effects. Do not spawn a replacement, reconstruct cargo or prune unresolved custody to recover space.

Receipts retain original intent, resource/key/instance, operation and attempt lineage, offered bound, actual paired result when known, uncertainty, proof scope, record revision and consumed limits. Saved inventory bytes and ledger counts are evidence, not additional physical stores or authority to populate one.

## Action specific guards

Use one server-owned dispatcher with guards selected by operation class. A blanket resolved-effects or live-hardware prerequisite must not prevent recording a stop or obtaining authorized recovery evidence.

| Class | Required conditions | Permitted result |
| --- | --- | --- |
| New admission | Authentic control/enrollment rights, valid immutable intent, empty proven cargo allocation, unique embodiment, relevant loaded/hardware/resource checks and reserved finite capacity | One admitted job; no item transfer |
| Record pause/cancel/revoke | Current scoped control or grant-issuer authority, canonical record, ordered revision and protected control capacity | Strengthen a dispatch fence even when effects, hardware or endpoints are unavailable |
| Retain custody / record uncertainty | Existing server-owned obligation and bounded attributable evidence | Preserve facts and explicit gaps without asserting a current quantity |
| Start recovery / read retained record | Scoped record access, quiescent dispatch and remaining finite recovery work | Inspect permitted historical evidence while effects remain unresolved |
| Read live evidence | Independent current right for each resource/field, valid identity/range/loaded context and read/work allowance | Bounded observation; unavailable or denied evidence stays unknown |
| Correct accounting | Server accounting authority, attributable evidence, expected record revision and bounded audit capacity | Correct justified facts or narrow uncertainty; no physical repair |
| Record resume/continuation/return intent | Current operation-specific control authority, original intent and ordered command | Record intent; resulting physical work still needs its own validation |
| Physical delivery | Current relevant rights, unique body, resolved dependent custody/quantity/position/energy, loaded context/hardware and remaining production limits | One bounded movement or paired transfer |
| Safety return/dock/charge | Separate current route/dock/supply/battery rights, resolved relevant physical state and finite service allocation | Service only; preserve cargo, delivery fence and normal dependency outcomes |

For normal delivery continuation, retain the conservative requirement that both enrolled endpoints and required route context are safely observable. Record-only controls need no endpoint access. Safety service checks its actual resources and cannot bypass relevant physical uncertainty. No path force-loads context or uses a different actor/face/provider to evade denial.

Preserve distinct provider states: ABSENT_CONFIRMED, PRESENT_ALLOW_VERIFIED, PRESENT_DENY_VERIFIED, PRESENT_NOT_APPLICABLE_VERIFIED, PRESENT_INDETERMINATE and PRESENCE_UNKNOWN. Evaluate all applicable supported checks. Trusted confirmed absence permits evaluating genuine built-in policy; absence alone grants no right. Required denial blocks the effect; unknown discovery/applicability/verdict defers it. Exact provider/version mappings remain a review and evidence requirement.

## Actual quantities and step outcomes

Let Q be fixed requested quantity, E cumulative unique proven source-to-cargo extraction, D cumulative unique proven cargo-to-destination delivery, and C actual attributable job cargo. In a resolved scope with no other cargo flows:

`0 <= D <= E <= Q; C = E - D; Q - D = C + (Q - E)`.

Bound pickup by Q−E, the declared maximum and actual cargo capacity. Bound insertion by actual C and Q−D. Preserve the exact component key. Requested amounts, simulations and aggregate endpoint totals do not establish attributable effects. After independent saves or external flows, retain historical proof scope and uncertainty rather than forcing current quantities to fit an equation.

| Outcome | Step and next action |
| --- | --- |
| Full bounded pickup | Positive paired effect equals its preauthorized target; verified load success can release destination navigation |
| Proven source shortfall | A positive pickup of all proven safely available stock can complete that bounded load; deliver actual cargo, but never claim the requested goal complete |
| Capacity-limited batch | Pickup meets its bounded target; complete that batch/service, then suspend with reason capacity_limited if D<Q |
| Smaller nonterminal partial pickup | Retain cargo, mark load partial, block destination dispatch and suspend for reviewed disposition; no automatic top-up, refund or promotion to success |
| Zero/denied/unknown pickup | No load success; unknown effects enter recovery, and proven zero gets only its separately eligible bounded retry |
| Partial insertion | Retain the remainder; unload is incomplete and normal home/recharge edges stay blocked |
| Complete batch insertion | Entire carried batch is verifiably inserted, C=0 and no relevant uncertainty; unload can succeed even if D<Q |

Only a verified SUCCEEDED predecessor with attributable receipts satisfies a dependency. An invocation, partial effect or job lifecycle label cannot release a dependent. Current observations and permissions remain required at every effect boundary.

Job success requires D=Q, C=0, no unresolved effects, actual dock arrival and verified charge target. Full delivery with failed service is reported separately. A terminal result never erases retained custody or proves that an interrupted effect was zero.

## Continuation and recovery

After a completed batch/service leaves D<Q, another pickup requires a fresh owner command and continuation attempt within the same job. Preserve cumulative quantities, original intent/beneficiary, receipt lineage and spent limits. Require empty proven cargo, remaining Q−E, current rights and enough remaining applicable allowances; do not start another pickup after its required insertion allowance is exhausted.

New batches require their own current dependency certificates. Old unload/home/charge results cannot release a new batch. Completed physical mutations remain historical and are never replayed.

Restored carried cargo instead retains its original completed extraction. Fence dispatch during activation, validate same-job custody and attributable receipts through authorized evidence, then require fresh destination context before inserting the proven remainder. Do not apply empty-cargo admission or run load again. Matching totals without attribution, partial pickups lacking load success, cancellation and unresolved effects cannot enable delivery.

A replayed continuation returns its historical result without clearing a newer stop or renewing an allowance. Recovery accounting correction uses justified evidence and expected-version updates; it never spawns/deletes/refunds items, changes position or resets energy.

## Controls and cancellation

Track execution phase, delivery outcome, service outcome, custody, cancellation intent, effective dispatch fence, effect resolution and persistence status separately. A cancel request ends delivery intent monotonically. Unknown effects retain recovery/quarantine with cancellation requested; only resolved effects permit terminal CANCELLED. Custody remains open when cargo is retained.

Acknowledge three separate facts: request recorded with its persistence status; dispatch fenced at a named sequence; prior effects resolved or uncertain. Failed storage cannot acknowledge durability and must suppress further physical work, including service. A bounded in-flight quantum must finish consistently or stay explicitly uncertain; stopping creates no unlimited finish-safely privilege.

Resume cannot clear cancellation, a newer stop or resource revocation. A separately admitted and independently authorized return/service control may preserve the delivery fence while moving no cargo between inventories. Owner/admin disposition of held items requires its own reviewed scope; a role name is not proof of resource rights or past conservation.

## Finite limits and retry timing

At admission, partition finite automatic work/action capacity into production, recovery and separately authorized service allocations within a defined aggregate ceiling. Also bound reads, passes, observations, navigation/search, energy, active time, no-progress deadlines, attempts, record retention and per-tick work. Define units and counting rules before choosing measured production values.

Production cannot consume reserved recovery or control capacity. A recovery pass requires both its pass allowance and work/read capacity for each observation; denied/unavailable reads consume them. Reserve bounded control records, queue, storage and scheduling, with coalesced monotone stops, bounded deduplication and per-principal processing. Refuse new work or resume before protected stop capacity becomes unavailable.

Use a finite declared retry schedule. An early eligibility query does not dispatch an effect; a dispatched zero/partial/denied attempt consumes its applicable allocation. Permission denial or unknown authority does not permit an automatic mutation retry. Reconciliation, changed IDs, continuation and restart cannot renew spent attempts, deadlines or budgets. Preserve active-clock and next-retry state without inventing unloaded work.

Actual material progress may advance a defined no-progress boundary; zero effects and control requests cannot. Exhaustion leaves passive held custody without polling. Unknown stored consumption cannot default to a full balance. Separately authorized service has its own finite scope and cannot refill delivery or recovery quotas.

## Persistence and deferred pack lifecycle

Propose a logical server record owner for admission, controls, custody and operation history, reachable independently of entity ticking. Physical cargo/body/battery, vanilla inventories and dock supply/berth remain separately owned resources. Exact storage APIs, save units, execution/reentrancy, flush ordering and failure scope are unselected.

Keep admission/reservations, pre-effect intent, observed result and consumed budgets, stop boundary, activation/recovery evidence, and terminal/open-custody receipts as distinct logical checkpoints. Versioned record updates do not establish atomic world saves. A journal, dirty flag, clean restart or safe hold does not prove cross-store crash conservation. Unsupported effects remain disabled pending scoped evidence.

For a future importer, pin immutable reviewed pack bytes and compatible semantics to a job. Disable fences dependent work while preserving records; replacement preserves existing pins; rollback changes selection, not physical history. Migration needs an explicit reviewed mapping preserving intent, custody, quantities, controls, receipts and consumed limits. Unknown mappings/effects quarantine. Retirement cannot discard live custody or replay evidence. This proposal authorizes no automatic migration and chooses no file-format or registry version.

The [verification plan](verification.md) defines observations needed to assess these obligations. Unresolved [review decisions](README.md#decisions-still-requiring-review) remain visible until maintainer adoption and implementation evidence exist.
