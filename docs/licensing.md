# Licensing and contribution scope

The owner selected MIT for original MAR code and examples, reserved rights for original artwork and sounds, and creator-chosen terms for independently authored community packs. The public copyright credit selected by the owner is **superdusto**.

The detailed publication package and contribution procedure are proposed in [ADR-0004](decisions/0004-code-and-asset-licensing.md). The existing significant-implementation contribution hold remains in effect pending maintainer adoption and explicit authorization in [CONTRIBUTING](../CONTRIBUTING.md). The owner's separate existing-material authority and draft-publication confirmation is recorded in that ADR; it is not an independent rights audit or a GitHub approving review.

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

## Reserved-asset inventory

No original robot artwork, models, textures, icons, sounds or logo files are present in the repository baseline for this package (`34bec980f4f909782aacf82da7c3c26cc2908b19`). No asset rights were audited or inferred from a bot account.

Before accepting a reserved asset, add its exact repository path, copyright holder/credit, provenance and applicable permission here. Maintain a separate entry or clearly bounded path group for every rights scope. Do not reserve an entire resource directory simply because Minecraft stores art and functional definitions together.

| Repository path | Rights holder / credit | Provenance and applicable terms |
| --- | --- | --- |
| No reserved files recorded yet | Not applicable | Asset inventory to be populated when actual files are proposed |

Third-party materials must carry their own notices and permissions; do not list them as original MAR-owned work. Package licenses and notices with any release containing covered material. Exact NeoForge metadata, download-channel setup and release auditing belong to the future build/release work.

## Contribution and adoption checks

The [contribution procedure](../CONTRIBUTING.md#contribution-rights-proposed) proposes inbound terms matching the affected material, an express human rights declaration tied to the reviewed revision, and separate checks of generation-tool terms and third-party provenance. It does not adopt DCO, a CLA or copyright assignment.

The owner expressly confirmed authority to license the existing original material in reviewed commit `2b5090b78495aae1da2aadf0e615843ec636efa6` and authorized draft PR publication in private project chat on 2026-10-27. No third-party exception was identified in that reply. This is an owner attestation, not proof of every file's provenance; third-party terms and newly identified exceptions still require review.

Before adopting the detailed package, review the exact notices, contribution procedure and any material rights exception. No additional declaration, sign-off or consent may be invented for the maintainer. Record implementation authorization separately when lifting the hold; publication of the licensing proposal does not establish that Minecraft behavior is implemented or verified.

## References

- [Authentic MIT text](https://spdx.org/licenses/MIT.txt)
- [Create's code/assets split](https://github.com/Creators-of-Create/Create/blob/mc1.21.1/dev/LICENSE.md), inspected 2026-10-27; a reference pattern, not MAR's asset permission text
- [Linux Foundation guidance on generation-tool terms and third-party material](https://www.linuxfoundation.org/legal/generative-ai)
