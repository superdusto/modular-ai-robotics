# Architecture Decision Records

Decision records capture project choices, their context, evidence, and reasons for revisiting them. They distinguish **accepted decisions** from **proposals** and **open research**.

| Record | Status | Decision |
| --- | --- | --- |
| [0001 — Initial platform target](0001-initial-platform.md) | Accepted, 2026-10-26 | Minecraft Java 26.1.2, NeoForge, Java 25 for the first development target |
| [0002 — Standalone core and optional integrations](0002-standalone-core-optional-integrations.md) | Accepted, 2026-10-26 | Independently usable mod; no mandatory third-party content mod; optional isolated adapters |
| [0003 — Capability-driven ports and adapter isolation](0003-capability-driven-integration-ports.md) | Proposed, 2026-10-27 | Server-side gateway, guarded optional packages, player enrollment, NeoForge-first item transfers and future AE2 adapter |
| [0004 — MIT code and reserved original assets](0004-code-and-asset-licensing.md) | Accepted, 2026-10-28 | Policy revision 67911cf approved and merged in PR #20: MIT code/examples, reserved original assets, independent pack licensing and express human contribution grants; implementation hold remains |

## Conventions
- **Accepted** means the owner has chosen a baseline; it does not establish that implementation or testing has succeeded.
- **Proposed** is an option pending a decision.
- **Superseded** preserves history and links to its replacement.
- Decisions should cite version-specific primary sources and list conditions that would justify reconsidering them.
- Do not silently turn desired features or architectural assumptions into verified capabilities.

See [Requirements](../requirements.md), [Risks and Open Questions](../risks-and-open-questions.md), and the [Development Roadmap](../development-roadmap.md).
