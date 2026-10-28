# Project Vision

## Goal
Create persistent, autonomous, upgradeable robotic companions for Minecraft that work locally and offline. Potential platforms include ground robots, drones, humanoid machines, and heavy mechs. Physical form must not define the decision-making architecture.

## Intended experience
Robots can join a player's base, accept goals, make bounded decisions, carry out meaningful work, coordinate resources, assist with adventures, and return to charging or storage stations. They should feel independent while respecting player instructions and game protections.

## Architectural principles
- Core autonomy works without network connectivity or paid AI inference.
- Jobs use reusable actions and capability requirements, not one-off hard-coded AI for every occupation.
- Hardware enables functions; policy separately authorizes actions.
- Persistence covers identity, inventory, jobs, home, and failure recovery.
- Our mod owns the useful core: robots, autonomy, docking/charging, jobs and basic upgrade progression without another content mod ([ADR-0002](decisions/0002-standalone-core-optional-integrations.md)).
- Optional adapters support mod-specific mechanics only where evidenced.
- Declarative knowledge packs may configure behavior; arbitrary imported prose is not automatically executable.
- No universal player equivalence or mod interoperability is promised.

## Non-goals for the first release
General artificial intelligence, full real-player simulation, arbitrary GUI automation, every mod/loader/version, player-scale mech piloting, or requiring hosted services.

## First proof
A persistent ground courier transfers items between two authorized containers and returns to a dock, safely resuming across save/reload. After that, validate a hardware-gated mining action.

## Decision status
Initial target is **Minecraft Java 26.1.2 + NeoForge + JDK 25** ([ADR-0001](decisions/0001-initial-platform.md)). The owner selected MIT code and reserved original assets; the detailed licensing/contribution package is [proposed in ADR-0004](decisions/0004-code-and-asset-licensing.md). Exact robot appearance and optional adapter selection remain under evaluation. The standalone-first architecture is accepted ([ADR-0002](decisions/0002-standalone-core-optional-integrations.md)).
