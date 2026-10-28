# Contributing

Thank you for your interest in Modular AI Robotics.

## Current phase
This project is in **research and architecture planning**. Please start with proposals, test plans, documented mod/API compatibility, and design reviews rather than large unrequested implementations.

## Good first contributions
- Version- and source-backed platform comparisons.
- Reproducible action/permission/inventory test cases.
- Small architecture alternatives with explicit tradeoffs.
- Knowledge-pack schema proposals and safety requirements.
- Corrections to research with authoritative references.

## Before proposing implementation
Open or discuss a focused issue describing purpose, constraints, relevant Minecraft and loader versions, source evidence, and acceptance criteria.

## Contribution hygiene
- Keep issues and pull requests narrow.
- Disclose the license of any borrowed code, assets, or reference data; do not copy incompatible third-party work.
- Do not commit personal game saves, credentials, API tokens, private logs, or proprietary documentation.
- Avoid introducing paid AI API requirements or mandatory cloud dependencies.
- Respect world protection, ownership, and server-side authority.

## Licensing and implementation hold

The owner adopted MIT for original code, documentation, schemas and examples, and [reserved original asset rights with explicit permitted uses](ASSET_LICENSE.md), through approval and merge of PR #20 on 2026-10-28. See the [license map](docs/licensing.md) and [accepted ADR-0004](docs/decisions/0004-code-and-asset-licensing.md).

**Do not submit significant implementation code or assets until the maintainer separately and explicitly authorizes those submissions.** Licensing/contribution-policy adoption is complete; the implementation contribution hold remains. Research, architecture discussion and test proposals may continue under the existing guidance.

Published license grants apply to their accompanying copies. This contribution hold controls acceptance of new submissions and does not revoke those published permissions. The accepted policy revision is `67911cff476f4f667e44356426de940ac67c80d1`, with [public approving-review evidence](https://github.com/superdusto/modular-ai-robotics/pull/20#pullrequestreview-5677986426); that acceptance does not itself authorize significant implementation submissions.

## Contribution rights

Contributors retain copyright in material they own. Submit original code and other MIT-covered material under [MIT](LICENSE). Original reserved-asset contributions require the express maintainer grant below and permission to offer the public uses in [the asset notice](ASSET_LICENSE.md), unless a separately reviewed applicable license is recorded. No copyright assignment or exclusive relicensing permission is requested. Independent packs not being incorporated into MAR retain their creators' chosen licenses.

### Reserved-asset contribution grant

Before a reserved asset is incorporated into MAR, its rights holder or authorized representative must expressly grant MAR's current and future project maintainers a **nonexclusive, worldwide, royalty-free copyright license** to:

1. Reproduce, modify, adapt and incorporate the contributed asset and its adaptations into Modular AI Robotics, including its project repositories and development/test materials.
2. Publish, distribute, publicly display and publicly perform those assets and adaptations, as applicable, as part of current and future official MAR releases and project development materials.
3. Authorize recipients to exercise the public permissions in `ASSET_LICENSE.md` at the reviewed revision identified in the contribution declaration, including permitted official-release modpack distribution.

The grant covers only the identified contribution, its authorized adaptations and rights the contributor is entitled to license, for the duration of the applicable copyright, subject to nonwaivable statutory rights. Contributors retain ownership and their copyright credits; maintainers must preserve applicable notices. This grant does not authorize licensing the assets under MIT, using them in unrelated projects, or expanding the public asset permissions beyond the identified notice without separate rights-holder permission.

### Human authority and express assent

For substantive contributions, an identified human or authorized organizational representative must review the actual diff and expressly confirm authority to contribute it under the applicable terms. Record the covered full commit IDs or PR head alongside the declaration. A suitable statement for a human to make is:

> Contribution reviewed: [CONTRIBUTION_FULL_SHA]. Reserved asset paths covered: [EXACT_REPOSITORY_PATHS, or NONE].
>
> I have authority to submit the identified material under its stated terms, including any necessary employer or third-party permissions. For the listed reserved assets, I expressly grant MAR's maintainers the permissions in `CONTRIBUTING.md` at [POLICY_FULL_SHA], with public uses governed by `ASSET_LICENSE.md` at [ASSET_NOTICE_FULL_SHA]. I have disclosed known third-party material and material generation-tool restrictions relevant to this contribution.

Replace every SHA placeholder with a full immutable commit ID, and list the exact asset paths in the declaration itself. If no reserved assets are included, use `NONE` and mark the asset-grant revision fields `NOT APPLICABLE`. If different asset groups use different terms, provide separate path-to-policy/notice-revision entries. Branch names, moving tags, or an unqualified reference to "the current notice" do not identify the grant terms.

This is a template, not a certification already made by the maintainer. A bot may record a declaration only when the human has actually made or expressly authorized it for that contribution. Bot authorship, a merged PR, an AI review or a copyright line cannot substitute for assent. Substantive later edits require renewed confirmation covering the accepted revision.

Disclose copied/adapted material, its source and license, required attribution/notices, and uncertain provenance. Check applicable generation-tool/output terms separately from third-party material found in generated output. Record relevant terms references/dates and resolve material restrictions or identified matches before acceptance. Private employer evidence may be handled privately; do not publish prompts, credentials, unrelated private material, or sensitive provenance evidence.

A formal DCO sign-off workflow is not part of this policy. Do not automatically add a human Signed-off-by trailer. Hold affected material when no truthful authority declaration can be supplied or a material rights conflict remains unresolved.

New reserved assets require exact file paths, rights-holder credits, provenance, applicable terms, and the express grant record with its reviewed policy/asset-notice revision in the [asset inventory](docs/licensing.md#reserved-asset-inventory). An authority declaration without the express asset grant is insufficient. Third-party material retains its own terms; the project does not claim it as original MAR work.
