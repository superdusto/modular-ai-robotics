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

## Merge protection and safe rollout

The existing active main-branch ruleset requires a PR, the decision-gate result from GitHub Actions, an up-to-date branch, resolved conversations, and blocked force pushes. Its bypass list is empty. Repository settings must be verified live; this document cannot configure them.

1. Add a second qualified collaborator. The nominated reviewer is @justdustn; the invitation must be accepted before their approval can satisfy repository requirements.
2. Require one approving review, dismiss stale approvals after new commits, and require approval of the most recent reviewable push. Preserve the existing required check, provider binding and empty bypass list.
3. Review and merge the hardening PR through that approval process. Its CODEOWNERS update covers all workflow files, scripts, tests, ADRs and this policy document with @superdusto and @justdustn.
4. After the updated CODEOWNERS reaches main, enable required Code Owner review. GitHub uses the base branch ownership file, so enabling it earlier can block this owner-authored migration PR: main initially names only @superdusto.
5. In a controlled test repository, verify that an invalid ADR, a no-op validator, a skipped gate job, and a replacement workflow cannot enter the protected branch without the required checks and independent review. Do not test by merging bypasses into this repository.

Do not add bypass exceptions or reduce existing protections to make a test pass. One listed code owner approval is sufficient; listing two owners does not require both. A reviewer must be independent of the PR author and latest reviewable pusher as required by the configured rules.

## Enforcement boundary

- The local Python process rejects malformed documents it examines. It cannot prevent commits.
- GitHub Actions executes PR-controlled code and reports a result. The workflow and tests can themselves be edited in the same PR. Pinning checkout and adding policy tests do not remove that trust boundary.
- GitHub's required check and independent review rules constrain covered merges while active. Administrators can change settings. Review approval is an accountable human judgment, not mathematical proof of correctness.
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
