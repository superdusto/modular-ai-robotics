# Minecraft Version and Integration Research

**Decision status: INITIAL TARGET ACCEPTED.** Minecraft Java Edition **26.1.2**, **NeoForge**, **JDK 25**. See [ADR-0001](decisions/0001-initial-platform.md). This is a development choice, not a demonstrated integration or build. Do not assume ATM10 compatibility.

## Selection criteria
1. Stability and availability of modding APIs, Java/toolchain, mappings and documentation.
2. Actual available builds of relevant robotics, logistics and technology mods.
3. Support for entity persistence, custom movement, block/interaction events, recipes, and item/energy capabilities.
4. Ease of isolated tests and future maintenance.
5. One loader/version initially. Separate builds/adapters for additional platforms if later justified.

## Alternatives recorded before selection
- Minecraft 1.21.1 / NeoForge: historical compatibility ecosystem with working robotics projects.
- Newer Minecraft / NeoForge: possibly better for greenfield code, but exact API and dependencies must be verified.
- Fabric only if chosen integrations or developer tradeoffs justify the alternate loader.

## Reference projects (architectural research, not dependencies)
- [OpenComputers: Modernized](https://github.com/habzg/OpenComputers-Modernized) — modular robots, drones, developer API.
- [PneumaticCraft: Repressurized](https://github.com/TeamPneumatic/pnc-repressurized) — drones, programmable work and specialized API.
- [CC: Tweaked](https://github.com/cc-tweaked/CC-Tweaked) — constrained robot/turtle actions.
- [Modular Drones](https://github.com/KesslerCascade/modular-drones) — customizable drone form factor.
- [MineColonies](https://github.com/ldtteam/minecolonies) — job scheduling and request logistics.
- [NeoForge documentation](https://docs.neoforged.net/).

## Integration tiers
1. Vanilla game operation.
2. Common tags, recipes, inventories and capabilities.
3. Optional documented mod API.
4. Large custom integration requiring special testing.
5. Unsupported or not verified.

A mod's presence, release compatibility, source code, and API stability are separate claims. Version-specific compatibility needs actual test evidence.

## Remaining research tasks
Verify exact toolchain versions when scaffolding, and record third-party mod versions/tags/commits, official sources, license, required dependencies, demonstrated action semantics and permissions. The initial baseline is selected; compatibility research remains open.
