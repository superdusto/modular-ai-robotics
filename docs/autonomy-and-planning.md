# Offline Autonomy and Behavior

The core mod must run without an external AI model, account, subscription, or internet access.

## Candidate control approach
- Rule-based prioritization for needs, jobs, urgent defense, charging and failures.
- Finite states for action lifecycle and recovery.
- Hierarchical task decomposition for multi-step occupations.
- Optional later planning methods such as GOAP only when demonstrated to improve known jobs.

## Example goal
Maintain an approved minimum quantity of iron ingots:
1. Check designated storage for shortages.
2. Prefer existing input material.
3. Request processing or mining only if required.
4. Allocate a capable robot and validate work boundaries.
5. Deliver and verify the resulting inventory.

## Memory
Persist only useful task observations: home, known storage, job checkpoints, blocked targets, route failures and resource availability. Revalidate cached world facts, especially after chunk unload or modpack changes.

## Failure semantics
Distinguish missing equipment, unsafe target, no permission, unloaded chunk, route failure, unavailable inputs and full destination. Retry with bounded backoff, replan within limits, or report blocked status.

## Future optional tooling
External language models may help author structured knowledge packs outside the game, but are never part of the required runtime or trusted execution path.
