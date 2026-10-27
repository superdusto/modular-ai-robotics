# Mechanical Decision Gate

**Status:** Implemented validator and CI workflow; repository merge-rule enforcement requires separate GitHub settings. Created 2026-10-26.

This process adapts selected reliability principles from the project's privately supplied `architect-revised.md` reference into checks that a deterministic program can actually perform. **It does not copy that supplied document into the public repository.** The source is a prompt-engineering specification, not a claim that static text can guarantee engineering correctness.

## What is mechanical

The script at [`scripts/check_decisions.py`](../scripts/check_decisions.py) checks **all numbered ADR files**, not just newly changed ones:

- One valid JSON metadata block near the top; schema version, filename/ID match and unique claim IDs.
- A named owner, valid date, linked GitHub issue, impact and explicit decision/verification statuses.
- Defined `## Context`, `## Decision`, `## Alternatives`, `## Consequences`, `## Evidence and uncertainty`, `## Verification plan` and `## Revisit triggers` sections, all containing nontrivial content.
- Each material claim records `kind`, **ESTABLISHED / CONDITIONAL / UNVERIFIED / NOT AVAILABLE** status, a version/environment `scope`, and `sources`. Supported or negative capability claims require at least one source URL.
- An ADR marked `verification_state=passed` must cite a test-evidence URL. Accepted decisions may explicitly remain `not_run`; approval of a design and proof of implementation are separate.
- A superseded ADR must identify an existing successor record.

The validator intentionally **does not** fetch source URLs or assert their meaning. It cannot check whether a claim is true, whether the decision is wise, whether a test really passed, whether a reviewer approved the decision, or whether external APIs are safe. Humans must verify the technical substance and the authorization/effects in actual Minecraft/NeoForge environments.

## Run locally

From the repository root:

```sh
python3 scripts/check_decisions.py --root .
python3 -m unittest discover -s tests -p 'test_decision_gate.py' -v
```

Only the Python standard library is needed. The negative tests intentionally verify that invalid decisions fail validation; they are not Minecraft integration tests.

## Automated CI

`.github/workflows/decision-gate.yml` runs `decision-gate` on every pull request, push to `main`, merge-group evaluation, and manual dispatch. It has read-only repository permissions and no user secrets or external AI inference.

The check reports success/failure in GitHub Actions after it runs, but **an optional check is not a merge-blocking rule**.

## Make it a required check (repository-owner action)

1. Open repository **Settings > Rules > Rulesets > New ruleset > New branch ruleset**.
2. Name it `Require Decision Gate`; set **Active** and target the default branch `main`.
3. Enable **Require a pull request before merging** and **Require status checks to pass before merging**.
4. Add the exact check name **`decision-gate`** to the required status checks after the workflow has reported a run. Avoid path filters that could leave required checks pending. If available, select GitHub Actions as the expected status-check provider.
5. Limit bypass exceptions; consider blocking force pushes and branch deletion. Verify the ruleset is active by attempting to merge an intentionally invalid ADR through a test pull request.

The single-owner repository should be careful with mandatory approval counts: a user cannot satisfy a required approval by approving their own PR. `CODEOWNERS` declares intended reviewers but is not itself a required review gate. Require human code-owner reviews after adding another qualified reviewer if this is desired.

## Exact enforcement boundary

- **Local Python process:** rejects malformed records in paths it examines; it does not prevent a GitHub commit by itself.
- **GitHub Actions:** can report a failing check on the PR/ref it actually tests; it does not prove factual correctness.
- **Active GitHub ruleset requiring `decision-gate` and PRs:** can block covered merges into `main` when the check fails. It does not constrain unprotected branches, off-platform document decisions or actors explicitly permitted to bypass rules. Admins can change repository settings.
- **Source-code trust:** scripts and workflows are repository code that can be changed in a PR. Treat changes to them or ADR policy as high-impact, and review them closely. `CODEOWNERS` communicates that expectation; a separate GitHub required-review setting is needed to enforce it.

**The strongest claim without checking an active ruleset is: `CI validation is available`, not `all decisions are mechanically enforced`.** The verified state of rulesets and branch protection should be assessed periodically.

## Decision workflow

1. Create or update a GitHub issue describing the decision, constraints, candidate approaches and consequences.
2. Copy [`docs/decisions/TEMPLATE.md`](decisions/TEMPLATE.md) to a numbered record and fill its machine-readable metadata.
3. Classify individual load-bearing claims; include actual version-scoped primary sources, and flag unknowns `UNVERIFIED` rather than inventing evidence.
4. Identify permissions and ownership boundaries; describe degraded behavior and safe failure for absent external technology mods.
5. State a testable acceptance plan, then run this checker and its tests.
6. Review facts and reasoning; accept or reject the ADR through an accountable owner/reviewer decision. Do not confuse `status=accepted` with `verification_state=passed`.
7. Run any integration tests needed before claiming observed runtime behavior. Supersede old ADRs explicitly rather than deleting history.

For Issue #2, key constraints include **ADR-0002's standalone core**, no mandatory external content mods, optional adapter isolation, safe fallback and player authorization. A structural ADR validator can require these constraints to be addressed in a decision, but cannot mechanically demonstrate them without an actual mod implementation and runtime tests.

## Sources and maintenance

- GitHub: [Required status checks](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- GitHub: [Creating repository rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository)
- GitHub: [Troubleshooting required checks](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)