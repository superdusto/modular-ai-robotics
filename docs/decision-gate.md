# Mechanical Decision Gate

Decision Gate validates a deliberately limited ADR document contract. Passing it does not establish technical truth, implementation success, or human approval.

## Required document contract

- Keep records as regular files directly in docs/decisions/, named NNNN-kebab-case.md. Subdirectories, symlinks, unsupported extensions, and duplicate numeric IDs fail. README.md and TEMPLATE.md are the only non-record exceptions.
- Include one JSON metadata comment within the first 500 characters. Duplicate keys, non-finite numbers, invalid field types and unknown top-level keys fail. Keep schema_version at 1.
- Use a visible H1 identifying the same ADR-NNNN as the filename and metadata.
- Include the seven required H2 sections: Context, Decision, Alternatives, Consequences, Evidence and uncertainty, Verification plan, and Revisit triggers.
- Use prose outside HTML comments, fenced code and indented code for the required title, headings and section content. Raw HTML is unsupported. These are explicit Markdown restrictions, not a complete Markdown rendering implementation.
- Content needs at least 20 characters, some character diversity, and must not be unchanged template instructions or simple repeated filler. This is a structural heuristic, not a test of meaningful reasoning.
- Classify claims and provide HTTPS source URLs for ESTABLISHED, CONDITIONAL and NOT AVAILABLE claims. A passed verification state needs at least one HTTPS test-evidence URL.
- Accepted decisions may remain not_run. Design acceptance and verified implementation are distinct.
- Superseded records must reference unique existing successors. Chains must be acyclic and end at an accepted record. Preserve historical ADR filenames; mark records superseded instead of deleting or renaming them.

## Run locally

From the repository root:

    python3 -B scripts/run_decision_gate_tests.py
    python3 -B scripts/check_decisions.py --root .
    python3 -B scripts/check_decisions.py --root . --base-ref FULL_BASE_COMMIT_SHA

Use an actual full 40-character trusted base commit in the last command. The two-argument local form performs document checks only; history preservation requires --base-ref. Git is required for history comparison. Python uses only the standard library.

The test runner requires both governance test modules to exist and contain tests. Import failures, test failures, empty required modules, and skipped tests fail the run. Workflow contract tests detect common unsafe changes; they are intentionally narrow source checks, not a general YAML security analyzer or an independent enforcer.

## CI execution and history

The decision-gate job runs on pull_request, pushes to main, merge_group, and workflow_dispatch. Keep its name stable for the required check. Do not add path filters, job conditions, dependencies that can skip it, or continue-on-error.

Checkout is pinned to commit 3d3c42e5aac5ba805825da76410c181273ba90b1, the actions/checkout v7 commit resolved by GitHub run 40452056114. Review future dependency updates explicitly. Checkout retains no persisted credentials and fetches full history. The token has only contents: read.

CI tests the validator first, then validates documents against the PR base SHA, merge-group base SHA, or push-before SHA. Manual dispatch falls back to the tested commit itself: it validates current documents but is not a historical transition check. Missing or invalid base commits fail closed. A first push with an all-zero before SHA needs a separately reviewed bootstrap; the existing repository does not require that exception.

History comparison reads Git tree names as data; it never executes code from the selected base. It prevents record disappearance, not arbitrary rewriting of existing decisions. Review remains necessary for content changes.

## Maintainer review and merge protection

Review is led by the maintainer, supported primarily by LLM reviews explicitly requested by the maintainer and by reproducible automated checks. The maintainer evaluates findings, resolves material issues, records any accepted residual risks, and is responsible for the final approval decision. This process does not claim independent human peer review. Account ownership or personal identity details are not part of the repository's review policy.

For changes to the validator, workflow, tests, ownership rules or this policy:

1. Request a substantive LLM review of the exact proposed revision, including bypass attempts, malformed inputs, workflow execution, permissions and regression coverage. Evaluate findings against the code and authoritative evidence; do not treat a model's recommendation as proof.
2. Record the reviewed commit, relevant findings, fixes, unresolved risks and reproducible test evidence. Re-review material changes after the review. Do not publish private account or integration details as review evidence.
3. Require the Decision Gate to pass on the latest revision and inspect what actually executed. Passing tests alone does not establish technical correctness or justify approval.
4. Complete the maintainer's review decision and satisfy the configured GitHub approval and status-check requirements before merging. LLM output does not itself count as a GitHub approving review.
5. Verify enforcement changes in a controlled test repository. Cover invalid ADRs, no-op validators, skipped jobs and replacement workflows without merging bypasses into this repository.

The active main-branch ruleset requires a PR, one approving review, dismissal of stale approvals, approval of the latest reviewable push, the decision-gate result from GitHub Actions, an up-to-date branch, resolved conversations, and blocked force pushes. Its bypass list is empty. Repository settings must be verified live; this document cannot configure them. Preserve these settings unless the maintainer explicitly authorizes a separate policy change. Do not add bypass exceptions or reduce protections to make a test pass.

CODEOWNERS identifies ownership and review routing. One listed code owner's approval can satisfy Code Owner review; listing two owners does not require both. Before enabling required Code Owner review, verify that the base branch ownership file and eligible reviewers support the intended process. GitHub uses the base branch file, so changing the PR's ownership file alone does not change who can satisfy that requirement for the PR.

Account-based approval rules do not prove independence of human judgment. Keeping approval authority outside an automated integration can provide useful separation of permissions, but must not be described as independent human peer review. The repository does not assert any account's integration configuration.

## Enforcement boundary

- The local Python process rejects malformed documents it examines. It cannot prevent commits.
- GitHub Actions executes PR-controlled code and reports a result. The workflow and tests can themselves be edited in the same PR. Pinning checkout and adding policy tests do not remove that trust boundary.
- GitHub's required check and account-based approval rules constrain covered merges while active. They do not establish reviewer identity independence or technical correctness. Administrators can change settings. The maintainer-led, LLM-assisted process above provides review evidence, not a guarantee against defects.
- Stronger automated tamper resistance needs a separately controlled check implementation with a verified execution and permission boundary. Do not claim this repository-local workflow provides that property.
- Skipping an entire workflow can leave a required check pending. Skipping a job with a condition can satisfy the check without execution. Manual workflow_dispatch results do not substitute for an eligible PR check.

## Technical evidence and implementation checks

URLs are syntax-checked, not fetched. Source relevance, authenticity, version applicability, ownership, test outcomes, and claim truth need independent verification. The issue field is a repository issue URL format, not a guarantee that the issue exists or approves the decision.

The checker does not require every code change to create an ADR, detect all contradictions, or prove that implementation obeys a decision. Review changes to decision-bearing code and reconcile conflicting ADR prose explicitly. ADR-0001 now records that ADR-0002 resolved the initially open core-versus-addon question.

Before changing verification_state to passed, record reproducible commands, exact versions/commit, observed outputs, and durable test evidence. For ADR-0002, separately verify a clean standalone client and server, vanilla courier behavior, persistence/recovery, player authorization, absent optional dependencies, disabled adapters and integration failure behavior. These Minecraft tests remain unrun until an actual implementation exists; governance tests do not substitute for them.

## Sources

- [Required status checks and skipped jobs](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/troubleshooting-required-status-checks)
- [Ruleset controls](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets)
- [Checkout commit observed in the successful PR run](https://github.com/superdusto/modular-ai-robotics/actions/runs/40452056114/job/122016823744?pr=13#step:1:31)
