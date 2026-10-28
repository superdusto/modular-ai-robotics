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
      "scope": "Existing original MAR source, documentation and other material; requires express maintainer confirmation and resolution of any rights exceptions before publication.",
      "sources": []
    }
  ]
}
-->

- **Status:** Proposed detailed package for the owner's selected licensing direction.
- **Recorded:** 2026-10-27 (America/Chicago).
- **Public credit:** superdusto, as explicitly selected by the owner.
- **Implementation contribution hold:** Remains in effect pending adoption and explicit authorization.

## Context

The owner wants credit for their work without controlling independently written scripts or behavior packs. After reviewing a Create-style separation, the owner selected MIT code and examples, reserved original visual/audio assets, and creator-chosen terms for independent community work. The previously researched MPL-first ranking depended on unconfirmed sharing priorities and is not the selected direction.

## Decision

Publish the authentic [MIT grant](../../LICENSE) for original MAR code, documentation, build tools, tests, schemas, functional definitions and examples. Apply the [asset notice](../../ASSET_LICENSE.md) to original artwork, robot models, textures, icons, sounds and logo artwork, with explicit gameplay, screenshot/video and official-release modpack permissions. Maintain the [asset inventory](../licensing.md#reserved-asset-inventory); third-party material retains its own applicable terms.

Independent packs remain under their creators' chosen licenses. Code forks may retain MIT-covered material with its notices, but need replacement art or permission for reserved assets. No copyright assignment, exclusive relicensing right, mandatory DCO process or compatibility-intake program is adopted by this proposal.

The proposed contribution procedure uses inbound terms matching the affected material and an express human rights declaration for the accepted revision. The owner's agreement to the direction and choice of public credit do not themselves certify existing-file rights or authorize significant implementation submissions.

## Alternatives

- MIT for all original material would be simpler but would also permit broad reuse of original artwork; the owner selected a separate asset boundary.
- Apache-2.0 is a permissive alternative with express patent terms and additional notice provisions. The selected reference pattern uses the simpler MIT grant.
- MPL file-level reciprocity is not required for the stated attribution goal. Its distribution limits, secondary-license route and later-version permission would need explicit treatment if reconsidered.
- A blanket restriction on all files beneath a Minecraft assets directory would also capture functional definitions. Identify artwork precisely instead.

## Consequences

Reusers must preserve the MIT notices for covered material, but may keep their modifications proprietary. MIT does not require prominent public credit or upstream patch submission. Asset reuse has a separate permission boundary that can require replacement artwork in forks. Contributors retain their own copyright, and the project must maintain provenance and asset classifications.

## Evidence and uncertainty

C1 is supported by the [MIT text](https://spdx.org/licenses/MIT.txt). [Create's inspected license](https://github.com/Creators-of-Create/Create/blob/mc1.21.1/dev/LICENSE.md) illustrates separate code/asset treatment; MAR's explicit asset permissions are project-specific.

The owner selected the direction in private project chat on 2026-10-27, replying "This seems fair" to the scoped proposal, and selected "superdusto" for public credit. This is an agent-authored record of those selections, not a GitHub-recorded approving review or a rights attestation. C2 remains unverified; a repository role, bot account, AI review or copyright notice does not establish ownership. No copyright assignment or human sign-off is inferred.

## Verification plan

Compare the MIT body with the authoritative text, changing only the year and copyright holder. Inspect the complete proposed file scope, rights/provenance exceptions, asset permissions and contribution declaration. Obtain the maintainer's express existing-material authority confirmation and adoption decision before publication. Run documentation links, Decision Gate tests and current/history checks against the trusted base.

Keep verification_state at not_run until the declared review and evidence requirements are satisfied. Passing mechanical documentation checks alone does not complete the rights review, lift the contribution hold or verify Minecraft behavior.

## Revisit triggers

Revisit when introducing original artwork, incorporating outside material, changing commercial/relicensing goals, selecting a formal DCO/CLA process, or finding a dependency or asset permission conflict. An actual issue may require narrowing affected material; it does not justify silently replacing contributors' licenses or changing independent pack ownership.
