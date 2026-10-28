# Licensing and contribution scope

The owner selected MIT for original MAR code and examples, reserved rights for original artwork and sounds, and creator-chosen terms for independently authored community packs. The public copyright credit selected by the owner is **superdusto**.

The licensing and contribution policy is accepted in [ADR-0004](decisions/0004-code-and-asset-licensing.md). The owner [approved policy revision 67911cf](https://github.com/superdusto/modular-ai-robotics/pull/20#pullrequestreview-5677986426) and merged [PR #20](https://github.com/superdusto/modular-ai-robotics/pull/20) on 2026-10-28. The significant-implementation contribution hold remains pending separate explicit authorization in [CONTRIBUTING](../CONTRIBUTING.md). The earlier private authority/publication confirmation remains separately recorded and is not an independent rights audit.

Published license grants apply to the copies they accompany. Final policy adoption is established by the approving review and merge; this follow-up reconciles the stale proposed labels left in that merged tree. It does not change the approved license permissions or lift the separate significant-implementation hold.

## License scope and notices

The [canonical LICENSE](../LICENSE) contains only the authentic MIT text. Its project-specific scope is described here and in the README: original Modular AI Robotics source code, documentation, build tools, tests, schemas, functional data definitions, example scripts and behavior packs are MIT-covered.

Original artwork, robot models, textures, icons, sounds and logo artwork are excluded from that MIT scope and governed by [ASSET_LICENSE.md](../ASSET_LICENSE.md). Record their exact paths, credits and asset-specific notices in the inventory below. A file is not a reserved asset merely because it is inside a Minecraft assets directory. Third-party material remains subject to its own terms and notices. Contributors retain copyright in material they own; the project credit does not transfer their ownership to the maintainer.

## License map

| Material | Terms |
| --- | --- |
| Original engine, APIs, integrations, build tools and tests | [MIT](../LICENSE) |
| Original documentation, schemas, functional definitions, example scripts and behavior packs | MIT |
| Original artwork, robot models, textures, icons, sounds and logo artwork | [Reserved asset rights with explicit permitted uses](../ASSET_LICENSE.md) |
| Independently created community scripts, behavior packs and artwork | Their creators choose their own licenses |
| Third-party code, assets or other protected material | Its applicable license and notices, reviewed for the actual use |

Using MAR does not transfer ownership of a creator's independent work. Copying substantial MAR material into a pack still requires compliance with that material's terms. Licensing does not grant a pack server permissions or establish that a proposed pack format or importer exists.

## Credit and forks

MIT requires retaining its copyright and permission notice in copies or substantial portions of the covered software. It permits proprietary modifications and does not require changes to be submitted upstream. It does not require every script author, server operator or video creator to display a prominent credit merely for using MAR.

Code forks are permitted under MIT. A fork needs replacement artwork or a separate permission covering reuse of reserved MAR assets. The asset notice expressly allows normal gameplay, screenshots/videos and distribution of unmodified official releases in modpacks.

The [existing-release permission clause](../ASSET_LICENSE.md#permissions-for-existing-releases) preserves the notice attached to compliant copies of a lawfully distributed official release. Later changes to the README's channels or to asset terms do not retroactively withdraw those permissions; compliance requirements and applicable-law limits still apply.

## Reserved-asset inventory

No original robot artwork, models, textures, icons, sounds or logo files are present in the repository baseline for this package (`34bec980f4f909782aacf82da7c3c26cc2908b19`). No asset rights were audited or inferred from a bot account.

Before accepting a reserved asset, add its exact repository path, copyright holder/credit, provenance, applicable permission and express maintainer-grant record here. Record the full immutable revision(s) of `CONTRIBUTING.md` and `ASSET_LICENSE.md` and the affected paths in the declaration itself as well as this inventory. Each reserved asset must carry or clearly reference its asset-specific notice, using an appropriate file or precisely scoped directory notice. Maintain a separate entry or clearly bounded path group for every rights scope. Do not reserve an entire resource directory simply because Minecraft stores art and functional definitions together.

| Repository path | Rights holder / credit | Provenance, terms and express grant record |
| --- | --- | --- |
| No reserved files recorded yet | Not applicable | Asset inventory to be populated when actual files are proposed |

Third-party materials must carry their own notices and permissions; do not list them as original MAR-owned work. Package licenses and notices with any release containing covered material. Exact NeoForge metadata, download-channel setup and release auditing belong to the future build/release work.

## Contribution and adoption checks

The [contribution procedure](../CONTRIBUTING.md#contribution-rights) requires MIT inbound terms for covered material, a separate [nonexclusive maintainer grant for contributed reserved assets](../CONTRIBUTING.md#reserved-asset-contribution-grant), an express human rights declaration tied to the reviewed revision, and separate checks of generation-tool terms and third-party provenance. It does not adopt mandatory DCO, a separate CLA workflow or copyright assignment.

The asset grant permits maintainers to reproduce, adapt and incorporate the identified assets, publish them in MAR's current and future releases and development materials, and authorize the public uses in the asset notice at the agreed revision. Contributors retain ownership and copyright credit. Expanding those public permissions, relicensing the assets under MIT, or using them in unrelated projects requires separate permission; a statement of authority alone supplies no such grant.

The owner expressly confirmed authority to license the existing original material in reviewed commit `2b5090b78495aae1da2aadf0e615843ec636efa6` and authorized draft PR publication in private project chat on 2026-10-27. No third-party exception was identified in that reply. This is an owner attestation, not proof of every file's provenance; third-party terms and newly identified exceptions still require review.

The final-policy acceptance is now independently linked to its public approving-review record; it is not inferred from the earlier direction selection or draft-publication consent. Continue reviewing rights exceptions and actual contribution grants as new material arrives. No additional declaration, sign-off or consent may be invented for the maintainer. Record implementation authorization separately when lifting the hold; policy adoption does not establish that Minecraft behavior is implemented or verified.

## References

- [Authentic MIT text](https://spdx.org/licenses/MIT.txt)
- [GitHub guidance on keeping the canonical license simple and explaining mixed licensing elsewhere](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)
- [Create's code/assets split](https://github.com/Creators-of-Create/Create/blob/mc1.21.1/dev/LICENSE.md), inspected 2026-10-27; a reference pattern, not MAR's asset permission text
- [Linux Foundation guidance on generation-tool terms and third-party material](https://www.linuxfoundation.org/legal/generative-ai)
