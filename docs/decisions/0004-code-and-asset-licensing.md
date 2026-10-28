# ADR-0004: MIT Code and Reserved Original Assets

<!-- decision-gate
{
  "schema_version": 1,
  "id": "ADR-0004",
  "title": "MIT code and reserved original assets",
  "status": "proposed",
  "owner": "superdusto",
  "recorded_on": "2026-10-27",
  "issue": "https://github.com/superdusto/modular-ai-robotics/issues/8",
  "impact": "high",
  "verification_state": "not_run",
  "test_evidence": [],
  "claims": [
    {
      "id": "C1",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "MIT permits reuse and modification subject to retention of its copyright and permission notice in copies or substantial portions of the covered software.",
      "scope": "The authentic MIT text; does not establish ownership of MAR files or grant rights in third-party material.",
      "sources": ["https://spdx.org/licenses/MIT.txt"]
    },
    {
      "id": "C2",
      "kind": "requirement",
      "status": "UNVERIFIED",
      "statement": "The maintainer has authority to apply the proposed terms to all pre-existing original material included in this package.",
      "scope": "Existing original MAR material; the owner expressly confirmed authority for reviewed package 2b5090b78495aae1da2aadf0e615843ec636efa6 and draft publication on 2026-10-27. This is owner-attested, not an independent legal or provenance audit.",
      "sources": []
    }
  ]
}
-->

- **Status:** Proposed detailed package for the owner's selected licensing direction.
- **Recorded:** 2026-10-27 (America/Chicago).
- **Public credit:** superdusto, as explicitly selected by the owner.
- **Implementation contribution hold:** Remains in effect pending adoption and explicit authorization.
- **Adoption gate:** Express maintainer acceptance of the final reviewed policy revision is pending. Published license grants already apply to their accompanying copies; proposed ADR status does not suspend them.

## Context

The owner wants credit for their work without controlling independently written scripts or behavior packs. After reviewing a Create-style separation, the owner selected MIT code and examples, reserved original visual/audio assets, and creator-chosen terms for independent community work. The previously researched MPL-first ranking depended on unconfirmed sharing priorities and is not the selected direction.

## Decision

Keep the canonical [LICENSE](../../LICENSE) as authentic MIT text only. Describe its scope for original MAR code, documentation, build tools, tests, schemas, functional definitions and examples in the README and [license map](../licensing.md). Apply the separate [asset notice](../../ASSET_LICENSE.md) to original artwork, robot models, textures, icons, sounds and logo artwork, with explicit gameplay, screenshot/video and official-release modpack permissions. Maintain precise asset notices and the [asset inventory](../licensing.md#reserved-asset-inventory); third-party material retains its own applicable terms.

Independent packs remain under their creators' chosen licenses. Code forks may retain MIT-covered material with its notices, but need replacement art or permission for reserved assets. No copyright assignment, exclusive relicensing right, mandatory DCO process, separate CLA workflow or compatibility-intake program is adopted by this proposal.

The proposed contribution procedure uses MIT inbound terms for covered material and a separate, express, nonexclusive maintainer grant for contributed reserved assets. The grant covers incorporation, reproduction, adaptation, publication in current/future MAR releases and development materials, and authorization of the public uses under the asset notice at the reviewed revision. Contributors retain copyright; broader asset permissions, unrelated-project use or MIT relicensing require separate permission. Record the express grant and applicable policy/notice revision with each asset; an authority statement alone is insufficient.

An express human rights declaration remains required for the accepted revision. The sample must identify the contribution commit, exact reserved-asset paths (or NONE), and full immutable revisions of the contribution policy and public asset notice. The owner separately confirmed authority over the existing original material and authorized publishing the prepared package as a draft PR. That existing-material confirmation is not assent on behalf of future asset contributors or acceptance of this final detailed policy. Significant implementation submissions still require explicit authorization after adoption.

Preserve the asset permissions attached to lawfully obtained/distributed official releases for compliant copies, including archived and modpack copies, when channels or later notices change. Applicable law and breach of the original notice remain limits. An official release's status is determined using the project's official channels when it was published, not a later README list.

Before merge, obtain and record express maintainer acceptance of the final reviewed policy commit, then update this ADR, the decision index and published policy status to reflect adoption. Keep them proposed until then. Adopting the licensing policy does not automatically lift the separate significant-implementation contribution hold.

## Alternatives

- MIT for all original material would be simpler but would also permit broad reuse of original artwork; the owner selected a separate asset boundary.
- Apache-2.0 is a permissive alternative with express patent terms and additional notice provisions. The selected reference pattern uses the simpler MIT grant.
- MPL file-level reciprocity is not required for the stated attribution goal. Its distribution limits, secondary-license route and later-version permission would need explicit treatment if reconsidered.
- A blanket restriction on all files beneath a Minecraft assets directory would also capture functional definitions. Identify artwork precisely instead.

## Consequences

Reusers must preserve the MIT notices for covered material, but may keep their modifications proprietary. MIT does not require prominent public credit or upstream patch submission. Asset reuse has a separate permission boundary that can require replacement artwork in forks. Contributors retain their own copyright, and the project must maintain provenance and asset classifications.

## Evidence and uncertainty

C1 is supported by the [MIT text](https://spdx.org/licenses/MIT.txt). [Create's inspected license](https://github.com/Creators-of-Create/Create/blob/mc1.21.1/dev/LICENSE.md) illustrates separate code/asset treatment; MAR's explicit asset permissions are project-specific. [GitHub's licensing guidance](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) recommends simplifying LICENSE and explaining mixed-license complexity elsewhere; actual GitHub display/detection is not claimed as tested. The [Copyright Office's description of reproduction, derivative-work, distribution, display and performance rights](https://www.copyright.gov/what-is-copyright/) informs the distinct maintainer grant; public-use permissions for an existing release do not replace contributor authorization to incorporate and adapt assets.

The owner selected the direction in private project chat on 2026-10-27, replying "This seems fair" to the scoped proposal, and selected "superdusto" for public credit. After being asked to confirm authority to license the existing original MAR material and authorize publication of reviewed commit `2b5090b78495aae1da2aadf0e615843ec636efa6` as a draft PR, the owner replied: "I am the one designing it so yes." No third-party exception was identified in that reply; this does not establish that no exception exists.

This is an agent-authored record of express private owner confirmation, not a GitHub-recorded approving review, DCO sign-off or copyright assignment. C2 remains independently unverified: the owner has attested authority, but no independent legal or provenance audit has been performed. Future substantive changes and contributions still require their own applicable rights review; the record does not extend assent to unrelated material.

## Verification plan

Compare the entire canonical LICENSE with the authoritative MIT text, changing only the year/copyright holder and whitespace. Inspect the separate scope/asset notices, release-permission stability, rights/provenance exceptions, maintainer grant and path/revision-specific contribution declaration. Before accepting a contributed asset, verify its grant record and agreed policy/notice revision; no assets are present yet. Retain the owner authority/publication confirmation recorded above and resolve identified rights exceptions. Record maintainer adoption of the final reviewed policy commit and reconcile ADR/index status before merge; keep implementation authorization as a separate decision. Run documentation links, Decision Gate tests and current/history checks against the trusted base.

Keep verification_state at not_run until the declared review and evidence requirements are satisfied. Passing mechanical documentation checks alone does not complete the rights review, lift the contribution hold or verify Minecraft behavior.

## Revisit triggers

Revisit when introducing original artwork, incorporating outside material, changing commercial/relicensing goals, selecting a formal DCO/CLA process, or finding a dependency or asset permission conflict. An actual issue may require narrowing affected material; it does not justify silently replacing contributors' licenses or changing independent pack ownership.
