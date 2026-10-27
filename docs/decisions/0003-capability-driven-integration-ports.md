# ADR-0003: Capability-Driven Ports and Optional Integration Isolation

<!-- decision-gate
{
  "schema_version": 1,
  "id": "ADR-0003",
  "title": "Capability driven integration ports with isolated optional mod adapters",
  "status": "proposed",
  "owner": "superdusto",
  "recorded_on": "2026-10-27",
  "issue": "https://github.com/superdusto/modular-ai-robotics/issues/2",
  "impact": "high",
  "verification_state": "not_run",
  "test_evidence": [],
  "claims": [
    {
      "id": "C1",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "NeoForge 26.1 documents ResourceHandler item and fluid capabilities and an EnergyHandler capability.",
      "scope": "Official NeoForge 26.1 documentation, not a tested Modular AI Robotics server build.",
      "sources": ["https://docs.neoforged.net/docs/inventories/capabilities/"]
    },
    {
      "id": "C2",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "NeoForge 26.1 transaction rollback requires participating handlers to implement appropriate snapshot behavior.",
      "scope": "NeoForge 26.1 handler transaction and snapshot contracts; not a guarantee of persisted multi-tick, cross-inventory crash atomicity.",
      "sources": ["https://docs.neoforged.net/docs/inventories/transactions/"]
    },
    {
      "id": "C3",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "NeoForge mod metadata optional dependencies allow absence but still check compatible versions when the dependency is installed.",
      "scope": "NeoForge 26.1 mod metadata; startup fallback for any particular packaged adapter remains untested.",
      "sources": ["https://docs.neoforged.net/docs/gettingstarted/modfiles/"]
    },
    {
      "id": "C4",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "AE2 tagged release v26.1.13-beta explicitly targets Minecraft 26.1.2.",
      "scope": "Specific AE2 release v26.1.13-beta, not a working integration or current-version compatibility guarantee.",
      "sources": ["https://github.com/AppliedEnergistics/Applied-Energistics-2/releases/tag/v26.1.13-beta"]
    },
    {
      "id": "C5",
      "kind": "source_observation",
      "status": "ESTABLISHED",
      "statement": "AE2 tagged ICraftingService declares asynchronous crafting-plan calculation, job submission and requester-linked craft tracking.",
      "scope": "AE2 v26.1.13-beta Java API declarations; scheduling, safe retry and in-world execution remain unverified.",
      "sources": ["https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingService.java"]
    },
    {
      "id": "C6",
      "kind": "source_observation",
      "status": "ESTABLISHED",
      "statement": "AE2 tagged IActionSource exposes empty, player and machine provenance without itself granting owner permission for proposed Modular AI Robotics network actions.",
      "scope": "AE2 v26.1.13-beta IActionSource declaration; no blanket claim that every unrelated target-mod authorization mechanism is absent.",
      "sources": ["https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/security/IActionSource.java"]
    },
    {
      "id": "C7",
      "kind": "requirement",
      "status": "ESTABLISHED",
      "statement": "Accepted project ADR-0002 requires an offline-first standalone core with no mandatory third-party content mod.",
      "scope": "Owner-selected project requirement at main base af57dd10793d4e78751d582605c733614f9d0369; not implemented Minecraft behavior.",
      "sources": ["https://github.com/superdusto/modular-ai-robotics/blob/af57dd10793d4e78751d582605c733614f9d0369/docs/decisions/0002-standalone-core-optional-integrations.md"]
    },
    {
      "id": "C8",
      "kind": "runtime_observation",
      "status": "UNVERIFIED",
      "statement": "Runtime adapter isolation, authorized endpoint and callback access, item custody, replay integrity and abrupt-crash recovery have not been demonstrated in this project.",
      "scope": "Future Modular AI Robotics Minecraft 26.1.2 NeoForge builds, vanilla courier and optional AE2 v26.1.13-beta worlds.",
      "sources": []
    },
    {
      "id": "C9",
      "kind": "source_observation",
      "status": "ESTABLISHED",
      "statement": "AE2 tagged ICraftingRequester has insertCraftedItems for in-progress output delivery, jobStateChange for terminal link state and getRequestedJobs for requester links.",
      "scope": "AE2 v26.1.13-beta tagged Java interface only; server thread, crash atomicity and duplicate callback semantics are not established.",
      "sources": ["https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingRequester.java"]
    },
    {
      "id": "C10",
      "kind": "source_observation",
      "status": "ESTABLISHED",
      "statement": "AE2 tagged Actionable differentiates MODULATE action from SIMULATE pretend action; its ICraftingLink exposes crafting ID, status and serialization.",
      "scope": "AE2 v26.1.13-beta Java enums/interfaces; no proof of cross-record persistence or item conservation.",
      "sources": [
        "https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/config/Actionable.java",
        "https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingLink.java"
      ]
    },
    {
      "id": "C11",
      "kind": "risk",
      "status": "UNVERIFIED",
      "statement": "No independent project-level proof yet establishes AE2 network ownership enforcement, callback thread safety, durable custody coordination or crash-safe single-courier replay.",
      "scope": "Implementation decisions and future tests INT-04A, INT-04B, INT-09A through INT-11A; proposed controls only.",
      "sources": []
    }
  ]
}
-->

**Status:** Proposed for maintainer acceptance review; **not accepted**. **Implementation/runtime tests:** `NOT RUN`. **Scope:** Minecraft Java **26.1.2**, **NeoForge 26.1**, JDK **25** initial target, and optional AE2 tag **v26.1.13-beta**, constrained by accepted [ADR-0001](0001-initial-platform.md) and [ADR-0002](0002-standalone-core-optional-integrations.md).

## Context

Accepted ADR-0002 requires usable, offline-first robot/courier gameplay with vanilla Minecraft and NeoForge alone. Issue #2 needs a reviewable adapter boundary for authorized generic handlers and, later, specific third-party networks. A capability handle, `IActionSource` identity or consent to enroll a local bridge cannot independently establish access to another player's network. AE2 [issue #7116](https://github.com/AppliedEnergistics/Applied-Energistics-2/issues/7116) documents retirement of its old security system; the retired security-station/grid-ownership premise must not be used as the project's access controller. The issue is history, not proof every check in AE2 v26.1.13-beta is absent.

External crafting may deliver actual items asynchronously through AE2 `ICraftingRequester.insertCraftedItems`, independent of the controller's original submit call. The accepted cargo can outlive a canceled or dead crafting link. A graceful server restart is weaker than an abrupt crash between world mutation and actual durable checkpoint. A single courier can also replay a UUID without any multi-robot concurrency. These paths require explicit admission, custody and replay requirements before design acceptance; the necessary mechanisms do not yet exist in project code.

## Decision

**Propose** typed, bounded, versioned core operation ports, a **server-owned action and custody gateway** with all-path enforcement, and optional version-scoped adapters isolated from core class loading. This is a design selection awaiting maintainer approval, not a technical capability already enforced by Minecraft.

**Standalone-first execution:** Build a vanilla two-container courier, robot cargo and dock without AE2, internet, paid inference or other content mods. Use NeoForge 26.1 `ResourceHandler<ItemResource>` and participating resource transactions where supported. A generic external handler is a later smoke test; AE2 is a still later specialized candidate. Keep the first-courier gate inclusive of ordinary save/restart `INT-04`, abrupt crash `INT-04A` and *single-courier replay* `INT-04B`. Defer only two-or-more-robot coordination to `INT-14`.

**Packaging:** Initially propose one core mod with guarded, independently activated integration packages. Core initialization, shared DTOs, serialization and registries must not eagerly reference absent/incompatible AE2 APIs. Test loader behavior when an optional dependency is present but incompatible before relying on fallback: NeoForge metadata still evaluates version restrictions for installed optional mods. If one-JAR classloader isolation fails, revisit separate bridge artifacts in a new reviewed decision; accepted ADR-0002 prohibits turning a third-party content mod into a core prerequisite.

**Authorization and network identity (F1):** At enrollment, the proposed Modular AI Robotics **server-side policy registry and action gateway** must prove the acting principal's right to enroll the particular endpoint, attached network and work zone; store owner, endpoint, network identity/fingerprint and allowable operations. On *every* stock read, item extraction, craft submission, callback reception, network change/reload and right revocation, rebind the live network and recheck server owner/zone/operation/resource rules plus *separately verified* applicable claim/protection authorization. Verify genuinely supported target-mod checks when present; do not invent AE2 security station, FakePlayer equivalence, or player/network-owner rights. `IActionSource.empty()`, `ofPlayer` and `ofMachine` are provenance only. If independent network ownership or relevant provider authorization is absent, unknown, errored or cannot be established, **`BLOCKED` with no unauthorized effect**. A user enrolling another player's grid does not gain access by that enrollment. Tests `INT-05`, `INT-09`, `INT-09A`, `INT-09B`, `INT-09C`.

**All-path effects and asynchronous AE2 custody (F2):** The server gateway must encompass **incoming** AE2 requester callback mutations, not only controller calls. Provisional receiver is a single **server-owned persistable staging inventory at the enrolled bridge**, associated with original owner, request, network identity, AE2 crafting link and per-key expected/accepted counts. `SIMULATE` computes possible acceptance without changing inventory, ledger, permissions or work orders. A `MODULATE` callback requires live server-side authorization, matched link/key and capacity, returns the amount actually physically inserted, possibly partial/zero, and credits only that proven amount. On revoked rights, unloaded endpoint, wrong link/key or full buffer, refuse new acceptance, retain/quarantine existing staged cargo and report the reason. On `jobStateChange`, preserve a separate durable custody receipt even after the live link becomes dead; cancellation and job completion are not delivery evidence. Runtime callback threading/reentrancy, receipt persistence atomicity and AE2 retry behavior remain unverified; **block production AE2 output delivery** until resolved. Tests `INT-10A`, `INT-10B`, `INT-10C`, `INT-11`, `INT-11A`.

**Crash and replay integrity (F3/F4):** For each step measure actual source, robot cargo, staging buffer and sink inventory counts and compare with request/receipt state; record any legitimate external transformation explicitly. Unknown physical outcomes must remain `RECONCILE_REQUIRED`, not guessed conservation or `COMPLETED`. Maintain stable request UUID and canonical intent; distinguish `not_seen`, `accepted_or_in_progress`, `completed_with_proven_effects`, `blocked_no_effect`, `uncertain_effect`. Same ID and proven complete same intent returns stored receipt without new world effect; changed intent is rejected; in-progress ID does not execute again; uncertain prior mutation blocks and reconciles. Do not assume an atomic compare-and-write, save flush, bounded lease or exactly-once mutation that the implementation has not proved. Abruptly terminate disposable worlds before/after extraction, insertion, checkpoint creation and actual observable save/flush; validate partial/cancel/unload and repeated recovery. A clean save is **not** a crash test. Until fault injection establishes the supported windows, these release guarantees remain **unverified**, and a technically untestable critical window is a maintainer block, not an implied pass. Tests `INT-03`, `INT-04`, `INT-04A`, `INT-04B`.

**Results and limits:** `ACCEPTED_PENDING` means confirmed external admission, not physical delivery; `COMPLETED` requires proven postcondition; `BLOCKED` is a denied operation with no *new* side effects only where that is proved; `RECONCILE_REQUIRED` records any uncertain prior effects; `FAILED` must preserve attributable cargo and effects. No arbitrary GUI control, unknown commands, unbounded retries, force-loaded chunks or unverified impersonation. Full [contract](../integrations/contract.md), [AE2 plan](../integrations/ae2-first-adapter.md) and [unrun verification matrix](../integrations/verification-matrix.md) define precise proposed behaviors, not shipped APIs.

## Alternatives

1. **Addon-only robotics dependency — rejected under ADR-0002:** It cannot satisfy independent gameplay.
2. **Direct controller imports/calls to every optional mod — rejected:** It can bypass the proposed server gateway and break core startup on missing APIs.
3. **AE2 legacy security-station or action-source-as-permission model — rejected:** A retired station model and an actor-provenance object are not an independently verified network authorization path.
4. **Automatically permit access when no claim provider is present — rejected:** Absence of a provider is not proof of network ownership or approval; block unestablished rights.
5. **Deliver crafted callbacks directly to robot cargo — deferred:** More loading, route and identity ambiguity; propose persistable server-owned bridge staging first, contingent on testing.
6. **Treat transaction/journal writes or terminal crafting callbacks as exactly-once evidence — rejected:** Neither demonstrates cross-save disk durability or actual robot receipt.
7. **Defer all replay testing with multi-robot work — rejected:** One courier already faces duplicate UUIDs and crash replays.
8. **Separate add-on JARs immediately — deferred fallback:** Consider if one-JAR optional class-loading fails, without changing the accepted standalone requirement.

## Consequences

Proposed benefits: a single narrow server policy and accounting path for vanilla operations and external callbacks, testable negative permission cases, and a reviewable phased adapter. Costs: reliable ownership evidence for attached AE2 grids, potential claim-provider compatibility work, durable output staging, callback scheduling/reentrancy analysis, measured save/flush fault injection and request ID retention. A provider's mere presence, schema validation, AE2 link serialization or passing governance tests cannot satisfy these.

The proposed policy is not a verified P2 runtime gate until non-model server components exist **and** all known mutation/callback/recovery paths demonstrably route through them. If an external API inherently bypasses the proposed admission boundary, the scope must narrow or the feature remain disabled. No distributed rollback, arbitrary disk durability or general exactly-once processing is promised. Where reconciliation cannot establish actual outcome, manual/admin intervention is an explicit bounded recovery outcome.

## Evidence and uncertainty

Claims C1–C3 are documented NeoForge 26.1 capabilities, participating transaction rules and optional dependency behavior; no independent saved-world guarantee is transferred from them. C4 is an AE2 **release-specific** compatibility target. C5–C6 and C9–C10 are **tagged Java API observations** (crafting planning, requester callbacks, `Actionable`, link status, action-source provenance), not our mod's runtime functionality. C7 is the accepted ADR-0002 project **requirement**, not a gameplay test. C8 and C11 explicitly keep the missing runtime enforcement and durability facts **UNVERIFIED**. None of C1–C10 upgrades a proposed callback/authorization mechanism into an existing implementation.

Primary versioned sources: [NeoForge 26.1 capabilities](https://docs.neoforged.net/docs/inventories/capabilities/), [transactions](https://docs.neoforged.net/docs/inventories/transactions/), [mod metadata](https://docs.neoforged.net/docs/gettingstarted/modfiles/); [AE2 v26.1.13-beta release](https://github.com/AppliedEnergistics/Applied-Energistics-2/releases/tag/v26.1.13-beta), [`ICraftingService`](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingService.java), [`IActionSource`](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/security/IActionSource.java), [`ICraftingRequester`](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingRequester.java), [`ICraftingLink`](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingLink.java), [`Actionable`](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/config/Actionable.java) and [security-system issue #7116](https://github.com/AppliedEnergistics/Applied-Energistics-2/issues/7116). The 2023 issue is change history, not a full negative API audit for the 2026 tag.

## Verification plan

Gate `first_courier` requires `INT-01`, `INT-02`, `INT-03`, **`INT-04` orderly restart, `INT-04A` abrupt crash including 12 enumerated mutation/persistence fault points, `INT-04B` single-courier replay**, `INT-05` denied policy and `INT-07` absent optional API startup. For `INT-04A`, compare precise physical inventories and durable request/uncertainty state after a crash **without orderly save**; report missing fault harnesses as `BLOCKED` if a future run cannot test them, rather than substitute graceful restart. The proposed release integrity requirement is no false completion, unauthorized duplication/loss or automatic replay of unresolved effects, with bounded accountable recovery; the mechanism remains unproved until implementation and trials.

Gate `generic_external_handler` separately requires `INT-06` and `INT-08`. Gate `ae2_specialized` requires `INT-09`, `INT-09A`, `INT-09B`, `INT-09C`, `INT-10`, `INT-10A`, `INT-10B`, `INT-10C`, `INT-11`, `INT-11A`, `INT-12`, `INT-13`: other-owner/no-provider/unknown-provider denial; same-network revalidation and revocation; bounded asynchronous submission; simulation with no mutation; partial callback acceptance and cancellation; wrong key/link and full buffer; unloaded/revoked callback denial; terminal receipt retention; interrupted/repeated callback and crash reconciliation. `INT-14` is only the **later multi-robot** gate. Every named case is currently **`NOT RUN`**. Future evidence must include exact versions/build, request/link IDs, policy decisions, physical deltas, server logs, process kill point, repeated recovery and a persistent immutable report.

Passing the [Decision Gate](../decision-gate.md), including its historical 39 governance tests, proves only constrained documentation mechanics, not Minecraft boot, permissions, inventory integrity, crash safety or AE2 operation. Keep metadata `verification_state: not_run` and `test_evidence: []` until independent observed runtime results support a justified update.

## Revisit triggers

Request renewed maintainer approval if a real AE2 version exposes a different documented authorization path; no enforceable binding can establish another owner's grid rights; callback server-thread confinement or atomic custody persistence cannot be implemented; crash tests reveal unauthorized duplicate/lost items; retention/pruning permits reused request IDs; optionally present incompatible mods break core startup; or one-JAR isolation fails. Do not weaken authorization, conservation or replay acceptance to force an ADR or runtime release to pass. If these remain unresolved, **request changes before accepting ADR-0003**; no accepted decision or deployed system is claimed here.

**Boundary of Issue #2:** The ADR can only settle a proposed design following owner review. Vanilla courier, generic transfers, AE2 crafting, permissions and persistence remain future implementation and runtime verification obligations.
