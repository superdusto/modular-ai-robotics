# First courier scope and review decisions

The first courier milestone is one persistent ground robot carrying actual items between two authorized vanilla containers, with one home/charging dock. For this first prototype only, use one execution policy: after a completed batch leaves the delivery goal incomplete, another pickup requires explicit owner-authorized continuation. Automatic repeat trips remain a future design alternative; they are not permanently prohibited. The general behavior-pack importer is deferred.

This records the project owner's initial scope choice on 2026-10-27. The detailed engine rules and verification plan below remain proposals for review. It does not accept ADR-0003, select a pack format, or establish that a Minecraft implementation works.

## Decision provenance and review

Source: the owner's private project discussion on 2026-10-27. In response to the recommendation to implement the stricter profile first and defer automatic repeat trips, the owner replied, "I like this idea." That selection covered the first prototype policy, including owner-authorized continuation after an incomplete batch, rather than adoption of every detailed contract rule.

This is an agent-authored record of that privately communicated selection. It is not a GitHub-recorded maintainer acknowledgment or an approving review; no publicly linkable GitHub acknowledgment of the selection is cited here. The distinction remains visible for review, without treating the private discussion as a public approval record or reopening the unchanged scope choice.

Review follows the repository's [maintainer-led, AI-assisted process](../decision-gate.md#maintainer-review-and-merge-protection). AI technical feedback does not itself supply maintainer adoption or a GitHub approving review.

## Status and reading order

| Subject | Status | Reference |
| --- | --- | --- |
| Minecraft Java 26.1.2, NeoForge and JDK 25 | Accepted initial platform; exact project build pins remain to be selected | [ADR-0001](../decisions/0001-initial-platform.md) |
| Standalone offline core with optional integrations | Accepted project requirement | [ADR-0002](../decisions/0002-standalone-core-optional-integrations.md) |
| One initial policy with owner-authorized continuation | Owner-selected first prototype scope | This document |
| Actions, quantities, guards, controls, budgets and recovery | Proposed contract | [Courier engine contract](contract.md) |
| Acceptance scenarios and evidence boundaries | Proposed; full cases not run | [Courier verification plan](verification.md) |
| Capability-driven integration ports | Proposed | [ADR-0003](../decisions/0003-capability-driven-integration-ports.md) |

The first repository implementation stage should be a deterministic state/eligibility kernel and an in-memory model harness with fixed server-owned bindings. A separate pinned development workspace and real client/server tests follow. This documentation change publishes neither model code nor a playable mod; local modeling does not supply repository-reproducible runtime evidence.

## Selected scope

Use one robot, one material job at a time, exclusive cargo ownership, two distinct enrolled vanilla endpoints, one dimension and a finite approved work area. The dock is for service, not a third job-item store. Commands, observations and future imported packs cannot grant resource rights.

The initial policy distinguishes these situations:

- A source-shortfall or capacity-limited batch can deliver its proven actual cargo. If the requested total remains incomplete after batch service, suspend and require owner authorization for another pickup within the same job and original remaining limits.
- A partial insertion can retry the proven remainder under fresh rights, finite attempts and declared backoff. This is continuation of the carried batch, not permission for another pickup.
- Restored cargo belongs to its original job and receipts. Recovery must validate that custody and current authority before physical continuation; it must not demand empty cargo or repeat an earlier extraction.

Keep the automatic repeat-trip policy as a future alternative for later design review. Do not implement a second profile or a configurable policy switch in the first kernel. Pack import, migration, other professions, additional chassis and optional adapters remain later stages. The repository's [knowledge-pack proposal](../knowledge-packs.md) continues to leave the file format unselected.

## Decisions still requiring review

| ID | Decision | Proposed starting point / remaining evidence |
| --- | --- | --- |
| CDR-01 | Guard and control boundary | Separate record-only controls, protected reads, accounting correction and physical actions; specify effective fence and persistence acknowledgment separately |
| CDR-02 | Recovery and control allocations | Reserve finite reads/work and control record/queue/scheduling capacity before effects; choose measured production limits and retention policy later |
| CDR-03 | Partial outcomes and cancellation | Keep smaller nonterminal partial pickups held; distinguish cancel intent from effect resolution and retained custody |
| CDR-04 | Authority and resource identity | Define enrollment, delegation, endpoint incarnation, exact components, provider discovery/applicability and separately scoped service grants |
| CDR-05 | Persistence and failure scope | Select actual save/receipt owners, restore lineage and supported failure model; demonstrate conservation independently of safe stopping |
| CDR-06 | Build and contribution prerequisites | Pin exact NeoForge/build tools and clarify project license/contribution terms before significant implementation submission |

These questions should be resolved against the concrete contract and observable tests, without treating model assumptions as world facts. Numeric quotas, energy units, provider hooks and durable save behavior remain unverified.

## Next milestones

1. Review the proposed contract and verification oracles, recording adopted details separately from remaining questions.
2. Submit a narrowly scoped standalone model and tests once contribution terms permit it; record exact source, JDK, commands and results.
3. Establish a pinned minimal NeoForge build and isolated client/server startup.
4. Bind real server authority, physical handlers, identity, energy and save ownership, then execute the standalone courier cases before expanding scope.

This work advances [controller/action contract issue #3](https://github.com/superdusto/modular-ai-robotics/issues/3) and [courier test-plan issue #6](https://github.com/superdusto/modular-ai-robotics/issues/6). A documentation review does not close their implementation or runtime evidence requirements. See [CONTRIBUTING](../../CONTRIBUTING.md) for current contribution and licensing prerequisites.
