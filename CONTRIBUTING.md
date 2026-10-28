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

The owner selected MIT for original code, documentation, schemas and examples, and [reserved original asset rights with explicit permitted uses](ASSET_LICENSE.md). See the [license map](docs/licensing.md) and [proposed ADR-0004](docs/decisions/0004-code-and-asset-licensing.md).

**Do not submit significant implementation code or assets until the maintainer adopts the detailed licensing/contribution package and explicitly authorizes those submissions.** This proposal records the direction; it does not lift the hold. Research, architecture discussion and test proposals may continue under the existing guidance.

## Contribution rights (proposed)

Contributors retain copyright in material they own. Submit original code and other MIT-covered material under [MIT](LICENSE), and original reserved assets under [the asset notice](ASSET_LICENSE.md), unless a separately reviewed applicable license is recorded. No copyright assignment or exclusive relicensing permission is requested. Independent packs not being incorporated into MAR retain their creators' chosen licenses.

For substantive contributions, an identified human or authorized organizational representative must review the actual diff and expressly confirm authority to contribute it under the applicable terms. Record the covered full commit IDs or PR head alongside the declaration. A suitable statement for a human to make is:

> I reviewed the contribution at [full commit SHA]. I have authority to submit the material under its stated terms, including any necessary employer or third-party permissions. I have disclosed known third-party material and material generation-tool restrictions relevant to this contribution.

This is a template, not a certification already made by the maintainer. A bot may record a declaration only when the human has actually made or expressly authorized it for that contribution. Bot authorship, a merged PR, an AI review or a copyright line cannot substitute for assent. Substantive later edits require renewed confirmation covering the accepted revision.

Disclose copied/adapted material, its source and license, required attribution/notices, and uncertain provenance. Check applicable generation-tool/output terms separately from third-party material found in generated output. Record relevant terms references/dates and resolve material restrictions or identified matches before acceptance. Private employer evidence may be handled privately; do not publish prompts, credentials, unrelated private material, or sensitive provenance evidence.

A formal DCO sign-off workflow is not adopted by this proposal. Do not automatically add a human Signed-off-by trailer. Hold affected material when no truthful authority declaration can be supplied or a material rights conflict remains unresolved.

New reserved assets require exact file paths, rights-holder credits, provenance and terms in the [asset inventory](docs/licensing.md#reserved-asset-inventory). Third-party material retains its own terms; the project does not claim it as original MAR work.
