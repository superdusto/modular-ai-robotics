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
      "scope": "Official NeoForge 26.1 modding documentation; not a tested Modular AI Robotics build.",
      "sources": [
        "https://docs.neoforged.net/docs/inventories/capabilities/"
      ]
    },
    {
      "id": "C2",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "NeoForge 26.1 resource transactions commit or revert participating handler operations when those handlers implement snapshot behavior.",
      "scope": "Official 26.1 transaction APIs and participating handlers; no claim of multi-tick distributed atomicity or save-crash durability.",
      "sources": [
        "https://docs.neoforged.net/docs/inventories/transactions/"
      ]
    },
    {
      "id": "C3",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "NeoForge mod metadata optional dependencies do not require the other mod to be installed but still enforce a compatible version when present.",
      "scope": "NeoForge 26.1 neoforge.mods.toml dependency metadata; exact packaging behavior must be tested with an executable mod.",
      "sources": [
        "https://docs.neoforged.net/docs/gettingstarted/modfiles/"
      ]
    },
    {
      "id": "C4",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "Applied Energistics 2 release v26.1.13-beta explicitly targets Minecraft 26.1.2.",
      "scope": "AE2 GitHub release v26.1.13-beta dated 2026-09-30; no tested interoperation with our mod.",
      "sources": [
        "https://github.com/AppliedEnergistics/Applied-Energistics-2/releases/tag/v26.1.13-beta"
      ]
    },
    {
      "id": "C5",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "AE2 tagged crafting service exposes an asynchronous crafting-plan calculation and job submission, with explicit crafting-link persistence requirements for machine requesters.",
      "scope": "AE2 v26.1.13-beta ICraftingService Java source; implementation and lifecycle behavior in our runtime remain untested.",
      "sources": [
        "https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingService.java"
      ]
    },
    {
      "id": "C6",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "AE2 tagged action source represents a player or machine and documents precedence of player identity for source checks.",
      "scope": "AE2 v26.1.13-beta IActionSource interface; does not establish authorization for any of our future robots.",
      "sources": [
        "https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/security/IActionSource.java"
      ]
    },
    {
      "id": "C7",
      "kind": "requirement",
      "status": "ESTABLISHED",
      "statement": "The project requires standalone robotics gameplay using Minecraft and NeoForge without mandatory third-party content mods.",
      "scope": "Owner-approved Modular AI Robotics ADR-0002 project requirement; not demonstrated implementation.",
      "sources": [
        "https://github.com/superdusto/modular-ai-robotics/blob/main/docs/decisions/0002-standalone-core-optional-integrations.md"
      ]
    },
    {
      "id": "C8",
      "kind": "runtime_observation",
      "status": "UNVERIFIED",
      "statement": "Runtime adapter isolation, inventory conservation, protected-area authorization, and AE2 crafting recovery have not been demonstrated for this project.",
      "scope": "Future Modular AI Robotics Minecraft 26.1.2 NeoForge client and dedicated-server builds, absent or installed AE2 and other content mods.",
      "sources": []
    }
  ]
}
-->

**Status:** Proposed for owner review; decision is not accepted until explicitly approved. **Implementation and integration tests:** Not run.

**Scope:** Offline-first Modular AI Robotics core on Minecraft Java 26.1.2 and NeoForge (ADRs [0001](0001-initial-platform.md) and [0002](0002-standalone-core-optional-integrations.md)); no claims about other Minecraft versions.

## Context

ADR-0002 establishes our standalone robotics core. Issue #2 still needs a precise way for the controller to use authorized vanilla containers and optionally coordinate existing third-party machines and networks. Public capability interfaces do not imply blanket authorization, and availability of a mod's API does not prove gameplay interoperability. The distinction between player intent, server authority, robot hardware, target-mod security, runtime compatibility and persistence must be mechanical at implementation time, not a prompt instruction or optimistic API assumption.

## Decision

**Propose one stable, vendor-neutral operation contract in the core, with server-side validation and isolated, optional integrations.** The controller owns goals, robot identity, job scheduling, checkpoints, admission policy and results; a robot chassis/modules constrain physical capabilities; adapters translate narrowly supported operations and never make security decisions on behalf of the core. The target mod owns its machinery, network state, crafting behavior, and its own permission mechanisms.

**First execution tier:** implement mod-owned courier pickup/deposit using verified vanilla/NeoForge 26.1 item access and a charging dock. A generic external inventory exposing the same supported item capability is the first cross-mod smoke test, not a specialized GUI driver. **First specialized adapter candidate:** AE2 v26.1.13-beta for Minecraft 26.1.2, initially inventory observation/authorized access, then a bounded crafting request with persistent requester-link tracking. AE2's release/API are documented; our integration is unimplemented.

**Packaging choice for the first candidate:** a single core mod artifact with separately isolated integration packages/initializers, activated only when a compatible, supported installed mod is detected. The core and common port must not import or eagerly initialize third-party classes. Verify this via clean startup and classloader failure tests; if reliable isolation cannot be demonstrated, switch specialized adapters to separately packaged bridge artifacts through a superseding decision. Do not declare a version-restricting optional dependency in the core metadata if that would cause incompatible installed versions to prevent core loading: NeoForge documents that even optional dependencies validate versions when present.

**Authorization:** a player must explicitly enroll an endpoint/network and an allowed work zone; every operation then rechecks the enrolled scope, live actor/robot identity, loaded region, hardware, resource bounds, server protection/claim rules where supported, and external target security. Neither enrollment nor a capability handle grants permission. If a reliable check is unavailable or inconclusive, block the action. No unverified FakePlayer impersonation or arbitrary GUI automation.

**Consistency:** separate synchronous handler transactions from long-running jobs. A transaction can cover participating resource handlers and must commit only verified permitted quantities; movement spanning robot pickup, travel and delivery is multiple independently durable steps, with exact custody tracking, checkpoints and reconciliation. Remote crafting submission returns **accepted/pending**, never completed until externally confirmed and output/custody is reconciled. On unknown completion state, do not blindly resubmit; block for reconciliation.

**Failure isolation:** missing, disabled, incompatible, unloaded, unpowered, denied or changed adapters become unavailable/blocked with a recorded reason. Vanilla robot functions remain usable without the optional content mod. No forced chunk loading, infinite retries or silent successful completion. All execution occurs on the authoritative game server; no network or hosted model is required.

See the [contract](../integrations/contract.md), [AE2 adapter plan](../integrations/ae2-first-adapter.md), and [test matrix](../integrations/verification-matrix.md). These names and operation IDs are **our proposed contract**, not names of implemented NeoForge or AE2 Java APIs.

## Alternatives

1. **Addon-only controller attached to a third-party robotics mod — rejected by ADR-0002.** Cannot satisfy standalone gameplay.
2. **Direct controller imports/calls to every supported mod — rejected.** Coupling exposes core startup and state to optional API removal/version churn.
3. **Treat all exposed automation handlers as automatically authorized — rejected.** A capability can be present while server or target-mod policy prohibits use.
4. **One generic GUI-driving/fake-player adapter — rejected.** No support exists for universal safe GUI operation or permission equivalence.
5. **Separate addon JAR for every integration immediately — deferred alternative.** Stronger dependency packaging isolation, but higher build, maintenance and distribution overhead before the first vanilla courier works. Revisit if internal isolation tests fail.
6. **Single mod, thin guarded adapters and server action gateway — selected proposal.** Lowest initial packaging complexity while retaining explicit tests and a fallback to separate artifacts.

## Consequences

Positive: fixed core contract accommodates different chassis and authorized player infrastructure, and vanilla-only play remains the primary deliverable. Risks: class loading, optional dependency metadata, endpoint security, crash consistency and network behavior require targeted tests; a one-JAR architecture has less static isolation than separately packaged adapters. AE2 support may lag release cadence. Exactly-once external requests and crash-proof cross-mod transfers cannot be promised from schema validation or a local journal alone. This ADR specifies design requirements, not demonstrated runtime guarantees.

## Evidence and uncertainty

C1 and C2 come from NeoForge's versioned 26.1 capability/transaction documentation; the transaction description is scoped to participating snapshot-aware handlers, not an arbitrary multi-tick workflow. C3 is the 26.1 mod-metadata rule that an optional dependency still validates a present version: the design therefore avoids treating an incompatible pinned optional dependency as a harmless fallback. C4 records AE2's specific 26.1.2 release, not a blanket current-version claim. C5/C6 are inspected Java API declarations at the named AE2 tag, not a demonstration of security or recovery integration. C7 is the accepted owner requirement; C8 remains explicitly unverified. An API contract and a passing ADR validator do not prove code isolation, endpoint permission, idempotency or item conservation.

Primary technical sources:
- [NeoForge 26.1 capabilities](https://docs.neoforged.net/docs/inventories/capabilities/), [transactions](https://docs.neoforged.net/docs/inventories/transactions/), and [mod dependency metadata](https://docs.neoforged.net/docs/gettingstarted/modfiles/).
- [AE2 v26.1.13-beta release](https://github.com/AppliedEnergistics/Applied-Energistics-2/releases/tag/v26.1.13-beta), [crafting service](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingService.java), and [action source](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/security/IActionSource.java).

## Verification plan

Use [integration verification matrix](../integrations/verification-matrix.md) as the acceptance plan. Require clean client and dedicated-server startup with no optional content mod; unmodified vanilla two-container courier and save/reload; authorized NeoForge item-handler transfer to an external inventory; missing/disabled/incompatible adapter startup; permission rejection; interrupted/partial transfers; bounded resources and chunk unloading. For the future AE2 adapter, record compatible mod versions, player/machine security identity, asynchronous-plan handling, persisted crafting links, duplicate-submission prevention and observed actual output after restart. The PR's ADR and CI tests can only prove documented structure, not Minecraft runtime behavior; keep `verification_state=not_run` until executable evidence exists.

## Revisit triggers

Reconsider packaging if absent or incompatible integration classes crash the core; if the loader forces incompatible optional dependencies to abort startup; if the target API cannot express authorized operations; if reconciliation tests reveal duplication/loss or unauthorized effects; if support for an external mod demands a separate permission authority; or if performance and maintenance measurements justify a bridge artifact. A breaking contract change needs a new version and a reviewed migration path, not silent reinterpretation.

**Boundary of Issue #2:** This ADR can settle the **design** once accepted. Requirements to demonstrate standalone boot, vanilla-only progression, actual external transfer and AE2 crafting remain open implementation/verification work until the corresponding tests are performed.
