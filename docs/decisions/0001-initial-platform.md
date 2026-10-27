# ADR-0001: Initial Minecraft Platform

<!-- decision-gate
{
  "schema_version": 1,
  "id": "ADR-0001",
  "title": "Initial Minecraft platform selection",
  "status": "accepted",
  "owner": "superdusto",
  "recorded_on": "2026-10-26",
  "issue": "https://github.com/superdusto/modular-ai-robotics/issues/1",
  "impact": "high",
  "verification_state": "not_run",
  "test_evidence": [],
  "claims": [
    {
      "id": "C1",
      "kind": "documented_fact",
      "status": "ESTABLISHED",
      "statement": "The official NeoForge 26.1.2 MDK specifies Minecraft 26.1.2, NeoForge 26.1.2.122 and Java toolchain 25.",
      "scope": "NeoForge 26.1.2 ModDevGradle template; reference configuration only, not an installed project build.",
      "sources": [
        "https://github.com/NeoForgeMDKs/MDK-26.1.2-ModDevGradle/blob/main/build.gradle",
        "https://github.com/NeoForgeMDKs/MDK-26.1.2-ModDevGradle/blob/main/gradle.properties"
      ]
    },
    {
      "id": "C2",
      "kind": "runtime_observation",
      "status": "UNVERIFIED",
      "statement": "Modular AI Robotics has not yet been built or tested as a Minecraft 26.1.2 NeoForge mod.",
      "scope": "Modular AI Robotics prototype, client, dedicated server and future robotics gameplay behavior.",
      "sources": []
    }
  ]
}
-->

- **Status:** Accepted (project-owner choice)
- **Decision date:** 2026-10-26 (America/Chicago)
- **Scope:** Initial prototype and research target; not a perpetual multi-version support promise.
- **Implementation status:** Planning only — no mod or build has been created.

## Context

The project needs one modding baseline for independent offline robotics development. The owner selected a greenfield target, but no implementation has been built or validated.

## Decision
Target **Minecraft: Java Edition 26.1.2**, **NeoForge**, and **JDK 25** for the first working prototype. Start with a single loader and a single Minecraft version. Choose exact NeoForge and development-tool versions when creating the workspace, then commit/pin them for reproducible builds.

Do not target ATM10 specifically. This decision does **not** settle whether the eventual project owns all robot entities or acts as an integration/addon for a compatible system. That question remains open in issue #2.

## Why this baseline
- **Confirmed game release:** Mojang published Java Edition 26.1.2 on 2026-04-09 as a 26.1 hotfix.
- **Confirmed loader support:** NeoForge maintains a 26.1.2 line and publishes an official 26.1.2 ModDevGradle template.
- **Confirmed JDK:** Minecraft 26.1 requires Java 25. The matching NeoForge MDK uses a Java 25 toolchain.
- **Suitable greenfield target:** The source-access/toolchain changes in 26.1 provide a plausible foundation for a new mod. This is a design preference, not a performance or integration guarantee.

## Observed upstream development-template versions
On 2026-10-26, the maintained [NeoForge 26.1.2 ModDevGradle template](https://github.com/NeoForgeMDKs/MDK-26.1.2-ModDevGradle) contained:

| Field | Observed reference |
| --- | --- |
| minecraft_version | 26.1.2 |
| neo_version | 26.1.2.122 |
| ModDevGradle plugin | 2.0.148 |
| Gradle wrapper | 9.2.1 |
| Java toolchain | 25 |

These values identify a source-backed **candidate scaffold**, not an installed or tested toolchain and not dependencies currently pinned by this repository. Recheck their compatibility when opening the build-system issue.

## Alternatives
- **1.21.1 + NeoForge + JDK 21:** Excellent historical ecosystem/reference implementations, but an older foundation for a new project. Still useful for learning and backport assessment.
- **Later 26.x Minecraft versions:** Newer but not required for the first prototype; adopting the latest version is not the main objective.
- **Fabric:** Viable alternative, but dual-loader support would increase early integration and testing work.

## Consequences
- Some robotics mods documented on 1.21.1 have **not been established** as available on 26.1.2. Their designs may remain useful, but their compiled code or extension APIs must not be treated as current dependencies.
- Mod-specific integration availability, stability, and protection behavior remain subject to individual version-specific research.
- Never assume entity/FakePlayer behavior, serialization, inventory capabilities, or world-storage paths carried forward unchanged from 1.21.1.
- No requirement to chase every upstream Minecraft update. Reevaluate only for concrete engineering benefit or blocking incompatibilities.

## Evidence and uncertainty

The cited upstream releases and ModDevGradle configuration document the proposed platform and its toolchain. They do not establish build success or third-party integration compatibility for our project. C1 is version-scoped documentary evidence; C2 remains unverified until an actual build and gameplay test.

## Verification plan

Pin a matching NeoForge/Gradle toolchain, build the minimal mod, launch a development client and dedicated server, test mod-owned robot persistence and authorized vanilla item transfer, and record exact versions, outputs and reproducible test evidence. These steps have not been run.

## Revisit triggers
Review if the chosen NeoForge/Java toolchain cannot support a minimal persistent robot, a high-priority integration is impossible on 26.1.2 and has no acceptable alternative, a security/support issue blocks use, or maintenance costs become disproportionate. Document any change in a superseding ADR.

## Primary sources (verified 2026-10-26)
1. [Mojang: Minecraft Java Edition 26.1.2](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-1-2)
2. [Mojang: Minecraft Java Edition 26.1 technical changes, Java 25](https://www.minecraft.net/en-us/article/minecraft-java-edition-26-1)
3. [NeoForged: 26.1 release notes](https://neoforged.net/news/26.1release/)
4. [NeoForged: 26.1 migration primer](https://docs.neoforged.net/primer/docs/26.1/)
5. [NeoForgeMDKs: MDK-26.1.2-ModDevGradle](https://github.com/NeoForgeMDKs/MDK-26.1.2-ModDevGradle)
6. [NeoForge Maven artifacts](https://maven.neoforged.net/releases/net/neoforged/neoforge/)

**Evidence boundary:** These sources establish official releases, documentation and a template. No local build, gameplay test or third-party mod integration was performed.
