# Knowledge Packs (Research Proposal)

## Purpose
Allow players and contributors to expand robot work definitions, operating preferences and supported resource knowledge without recompiling the mod.

## Initial scope
Prefer structured, declarative data with versioned schema and validation (exact file format TBD). Candidate data: job templates, permitted goals, resource tags, module requirements, priority policy and robot profiles.

## Important distinction
A data file can compose **implemented** actions. It cannot create arbitrary new Java behavior, interpret unknown mod GUIs, or grant a robot permission to alter protected areas.

## Document import
Uploading PDFs, Word documents, or free-form text is a possible **future conversion workflow**, not a promised built-in natural-language understanding engine. A converter would need to extract supported data and present a reviewable, validated representation before activation.

## Trust boundary
Treat imported packs as untrusted:
- Validate schema, namespaced identifiers, bounds and references.
- Never execute embedded code, macros, scripts, commands or network requests.
- No override of owner, protection rules, authorization, or hidden configuration.
- Support preview, explicit enable/disable, rollback and version migration.
- Reject ambiguous world-mutating operations.

## Adaptive memory
Store world observations and past outcomes separately from imported policy. Learn to avoid failed paths or improve task selection without treating experience as authority to bypass restrictions.
