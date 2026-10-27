# Product Requirements and Scope

**Status:** Planning baseline, 2026-10-26. The scope categories below are intentions, not promises of implemented support. See [ADR-0001](decisions/0001-initial-platform.md) for the accepted technical target.

## Non-negotiable project constraints
- **R-001 — Offline-first:** Core gameplay/autonomy must function without an internet connection, external account, paid inference, ChatGPT API or subscription.
- **R-002 — Owner control:** Player-configured goals, work areas and server permissions restrict what robots may do. Missing/unsupported authority checks must not be interpreted as permission.
- **R-003 — Server authority:** Every world-changing action uses a verified, server-side path. Hardware capability does not confer authorization.
- **R-004 — Persistent integrity:** Keep robot identity, owner, inventory, energy and work state consistent across save/reload, interruptions and permitted chunk unloads; avoid duplication or silent loss.
- **R-005 — Modular actions:** Compose jobs from reusable, validated actions. Chassis provides movement and hardware; decisions and job definitions remain conceptually separate.
- **R-006 — Extensible, not magically universal:** Integrate supported vanilla/common interfaces first, with explicit optional adapters. No blanket compatibility with every mod or graphical screen.
- **R-007 — Trust-boundary clarity:** Imported data, robot observations and optional externally authored plans are untrusted inputs; they cannot execute arbitrary code or override permissions.

## First executable prototype — required
- One ground robot with stable identity, owner, energy, cargo and configurable home/charging dock.
- Player-facing means to assign and inspect a bounded delivery task, pause/recover and see why work is blocked (UI design TBD).
- Transport specified items between two **authorized** vanilla or otherwise verified compatible containers.
- Validate distance, capacity, available items, loaded state and server-side permission before interactions.
- Correctly handle actual extraction/insertion amounts, partial delivery, blocked/full targets, bounded retries and interruptions.
- Reconcile state across restart and chunk transitions without inventing work while chunks are inactive.
- Automated/manual acceptance checks for no duplication/loss and safe failure.

## Next test milestones — planned
- Mining module that gates permission to request an excavation action **as a hardware capability**; independently validate ownership/protection before mining.
- One approved exposed ore mining/collection/delivery loop with tool, drops and inventory accounting.
- Reusable job definitions (courier, selected farming/processing work) that reference capability IDs.
- A flying drone executing the same high-level courier objective through a separate aerial navigation implementation.
- Job queues, work reservations and coordination for more than one robot.
- Optional adapters for selected storage, energy, recipe and technology mods, version verified.

## Long-term concepts — not v1 commitments
- Specialized industrial workers, humanoid robots, player-following companions and large mechs.
- Construction/blueprints, large excavation, exploration, defense and contextual assistance.
- Progression through replaceable tools, batteries, cargo, sensors, manipulators and mobility modules.
- Swapping one persistent controller identity between chassis (with exactly one active embodiment unless multi-body semantics are deliberately designed).
- Resource quotas, advanced supply-chain planning, social flavor/personality and richer command interfaces.
- Importable **structured** knowledge/job/policy packs; optional later conversion from Word/PDF/plain English with review and validation.
- Adaptive memory of useful locations, route failures, unfinished jobs and observed outcomes. No neural-network training required.
- Optional external tools (including locally run or user-operated language models) may author candidate packs, but never become required for running the mod.

## Explicit non-goals
- A ChatGPT or other LLM service directing each game action.
- A paid API dependency.
- General artificial intelligence or unrestricted self-modifying machine code.
- Full player equivalence, automatic support for every mod/UI, or unrestricted simulation in unloaded chunks.
- Supporting multiple game versions and mod loaders at project inception.

## Acceptance, prioritization and traceability
Work is gated by observed behavior, not release dates. The first priority is reliable delivery and recovery, not broad feature count. See [Verification Plan](verification-plan.md) for acceptance checks, [Player Experience](player-experience.md) for still-proposed interaction patterns, and [Roadmap](development-roadmap.md) for milestones.

Related GitHub issues: [#2](https://github.com/superdusto/modular-ai-robotics/issues/2), [#3](https://github.com/superdusto/modular-ai-robotics/issues/3), [#4](https://github.com/superdusto/modular-ai-robotics/issues/4), [#5](https://github.com/superdusto/modular-ai-robotics/issues/5), [#6](https://github.com/superdusto/modular-ai-robotics/issues/6), [#7](https://github.com/superdusto/modular-ai-robotics/issues/7).
