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
- Optional adapters support mod-specific mechanics only where evidenced.
- Declarative knowledge packs may configure behavior; arbitrary imported prose is not automatically executable.
- No universal player equivalence or mod interoperability is promised.

## Non-goals for the first release
General artificial intelligence, full real-player simulation, arbitrary GUI automation, every mod/loader/version, player-scale mech piloting, or requiring hosted services.

## First proof
A persistent ground courier transfers items between two authorized containers and returns to a dock, safely resuming across save/reload. After that, validate a hardware-gated mining action.

## Decision status
Minecraft version, mod loader, license, exact robot appearance, and standalone-vs-addon direction remain under evaluation.
