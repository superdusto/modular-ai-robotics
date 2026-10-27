# Player Experience and Progression (Proposed)

These are gameplay ideas from project discussions; they are **not confirmed features** or a completed UI specification.

## Core experience
A player builds or obtains a robot, assigns it a home/charging station, defines authorized work areas and gives useful tasks. The robot operates independently within its hardware and permissions and reports clear outcomes.

## Candidate interfaces
- Robot status: identity, owner, selected job, health/energy, cargo, installed modules, location and reason for being blocked.
- Home/dock panel: charge, pause/resume, return home, configure source/destination containers and work boundaries.
- Job configuration: direct bounded work orders before advanced natural-language or global-goal interfaces.
- Error feedback: insufficient equipment, target protected, path blocked, no input, destination full, energy low, or chunk unavailable.
- Player controls: interrupt, disable autonomy, edit authorized areas, and inspect task progress.

## Progression
Installable batteries, sensors, manipulators, mining tools, cargo upgrades, mobility devices and defenses can expand *physical capability*. Software/knowledge packs can change permitted job definitions and priorities without adding executable code.

## Forms and roles
- Ground utility robot first.
- Flying drone next to validate a shared task definition.
- Humanoid companion, specialized machines and heavy mech later.
- Optional identity transfer between chassis is a separate design decision.
- Piloted mechs, combat systems, advanced construction and personality are deferred concepts.

## Autonomy and memory
The robot may learn world-specific facts (storage locations, repeated path failures, unfinished jobs). These observations can influence planning but must be revalidated before acting. “Intelligent” refers to in-game rule/planning behavior, not a paid language-model service.

## What to decide later
Exact crafting recipes; progression tiers; aesthetics and animation; UI layouts; work-area selection controls; chunk loading and remote operation; combat consent; role-based multiplayer ownership; whether commands are available through dock, robot item or both.

Keep the first controls simple enough to make courier testing transparent and reproducible.
