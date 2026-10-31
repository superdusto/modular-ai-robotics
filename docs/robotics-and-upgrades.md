# Robot Platforms and Hardware

## Concept
A persistent controller may operate a supported physical platform equipped with modules. One platform is enough for the first prototype. Transferring an identity between bodies is a future possibility, not an initial requirement.

## Candidate chassis
- Ground utility robot: transport, base work, farming/mining with tools.
- Flying drone: light delivery, collection, scouting; requires separate aerial navigation.
- Humanoid robot: flexible tools, defense and accompaniment.
- Heavy industrial mech: high-capacity work, large collisions, later-stage concept.

## Modules
Navigation, sensors, cargo, battery, manipulator, mining tool, construction tool, combat system, communications and processing equipment.

## Invariant
Installed hardware controls what an action *can* do. Work-zone rules, game protections and permissions separately determine what it *may* do.

## Energy
A battery/dock model can motivate useful logistics and recovery, but its exact values and tiers remain game-design choices. Charging and reload must preserve energy accurately.

## Prototype
Start with one ground courier; add a mining module only after item transport works reliably.

## Appearance and graphics packs

The owner selected a [compact bipedal utility scout reference](visual-design/compact-utility-scout-v0.1.0/README.md) for one robot and supplied [segmented modular companion](visual-design/segmented-modular-companion-v0.1.0/README.md) and [hovering utility drone](visual-design/hover-utility-drone-v0.1.0/README.md) concepts. These appearance references do not select every pictured capability, final names or the first courier's final chassis.

The planned graphics offering has at least Low, Medium and High packs, with Ultra optional and aiming toward the supplied references' finer mechanical detail. The [graphics pack plan](visual-design/graphics-quality-tiers-v0.1.0.md) proposes consistent gameplay and recognizable robot identities across tiers, with geometry, textures and decorative effects scaled together. Packaging, renderer support, performance budgets and implementation remain later decisions.
