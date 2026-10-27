# First Specialized Adapter Candidate — AE2 (Design Only)

**Status:** Candidate. No AE2 adapter has been compiled, loaded or tested. This proposal references AE2 **v26.1.13-beta** for Minecraft **26.1.2**, not every AE2 version.

## Why AE2 first

AE2's inspected `ICraftingService` includes `beginCraftingCalculation` (returns a `Future<ICraftingPlan>`) and `submitJob`, plus a requester/crafting-link contract. The `IActionSource` API distinguishes player and machine provenance. This makes AE2 a testable specialized *crafting request* candidate, unlike a hypothetical universal-machine adapter. Official source: [crafting service](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingService.java), [action source](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/security/IActionSource.java), [crafting link](https://github.com/AppliedEnergistics/Applied-Energistics-2/blob/v26.1.13-beta/src/main/java/appeng/api/networking/crafting/ICraftingLink.java), [release](https://github.com/AppliedEnergistics/Applied-Energistics-2/releases/tag/v26.1.13-beta).

## Phased acceptance

**Phase A — authorization and observation:** confirm a compatible installed AE2 binary, server-side enrolled bridge endpoint, network ownership/security, ability to observe approved stock/craftability, and denied-access behavior. Absence/incompatible-version startup must not break standalone. No crafting submission in this phase.

**Phase B — one bounded craft:** use the supported asynchronous crafting-calculation API without blocking the server tick; inspect any resulting plan, authorization and resource bounds. Submit only with an appropriate AE2 `IActionSource` backed by an approved player/machine context, and record request linkage if accepted. The project must define a real requester integration for any machine-initiated jobs, not merely invent a crafting ID.

**Phase C — durable recovery:** persist the resulting `ICraftingLink` through the supported AE2 serialization interface, expose it through the AE2 requester contract, recover status after unload/restart, and prove that a lost response or partial restart does not trigger duplicate requests. Inspect final resource output before counting a work order complete. A crafting-link state alone does not prove delivery to a robot.

## Permission and class-loading gates

Do not equate `IActionSource.empty()` with permission, fabricate a player-context identity, or treat mere AE2 grid presence as authorization. Verify how AE2's security station, grid ownership and machine bridge actually enforce permitted actions at the selected release; fail closed if it cannot be established. Keep AE2 classes in a guarded integration-only package and class loading out of core initialization, common DTOs and serializers.

NeoForge [mod metadata documentation](https://docs.neoforged.net/docs/gettingstarted/modfiles/) makes optional dependency version behavior material; version-range declarations need explicit missing/present/incompatible tests, and must not turn an incompatible optional mod into a required core startup failure.

## Test scenarios

- Clean vanilla+NeoForge+our mod startup without AE2, client and dedicated server.
- AE2 installed compatible build and enrolled network vs unenrolled/denied network.
- AE2 disabled or incompatible version; core remains functional if loader accepts the combination.
- Network with no power, no pattern, missing inputs, full or disconnected output.
- Request succeeds only for bounded item/quantity with known source; denial causes no extraction.
- Asynchronous plan pending, chunk unload, server restart, lost submission response, reattachment, link invalidation/cancel and duplicate request suppression.
- AE2 removes/changes the network or requester, or its mod is uninstalled between saves; core still loads if the world can load and reports unresolved integration jobs.

**Exit evidence:** actual client+dedicated-server test reports including Minecraft/NeoForge/AE2 versions, installed mod list, server permissions, build/commit, exact operations, observed inventory deltas, persisted crafting-link behavior and failure cases. Until then status is UNVERIFIED for runtime functionality.
