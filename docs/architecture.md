# Architecture Proposal (Not Final)

## Core principle
Separate **what an agent knows**, **what it decides**, **what its chassis can do**, and **what the server permits**.

```text
Player intent / local observations
           |
     Controller state
  goals, memory, priority
           |
  Job scheduler / planner
           |
 Capability requirements
           |
  Server action validator
           |
 Action implementations ---- optional mod adapters
           |
 Robot platform + modules
           |
 Minecraft server state
           |
 Verify / checkpoint / retry
```

## Candidate boundaries
1. **Identity and persistence:** Stable UUID, owner, home/dock, task checkpoints, cargo; versioned serialization and world-level indexes as needed.
2. **Agent controller:** Select objectives, maintain priority, interrupt work, record failures, and reconcile after reload.
3. **Task definitions:** Compose reusable actions for mining, transport, farming, crafting, defense, and building.
4. **Physical platform:** Ground or aerial movement, collision, tool mounting, energy, cargo and hardware restrictions.
5. **Capability catalog:** Describe available operations from installed modules, with preconditions and resource costs.
6. **Action gateway:** Validate actor, target, range, loaded state, work zone, permissions, equipment, inventory, and postconditions. Reject ambiguous authorization rather than treating an unsupported check as permission.
7. **Mod adapters:** Optional, separately tested support for established mod APIs; never assume unknown GUIs are automatable.
8. **Knowledge subsystem:** Validate declarative profiles and tasks, keep auditability, never execute imported scripts or override authorization.

Initially these are packages/interfaces inside **one mod**, not separate deployable systems.

## World and inventory safety
The authoritative game server owns state changes. Any AI or imported instruction may only propose tasks. Validate operations at execution time. Avoid direct mutations outside the action gateway. Item transfer must account for actual extracted quantities, insertion remainders, and save/reload reconciliation; simulation is not a universal transaction.

## Chassis separation
A task declares capability requirements (for example: navigate, item-extract, cargo, item-insert), not a specific robot class. A new flying chassis can reuse the courier job while implementing different navigation.

## Unresolved architecture tests
- Compare custom-entity versus player-context action semantics for block modification.
- Verify claims/permissions on any supported action path.
- Test inventory fault recovery and chunk-unload behavior.
- Determine whether a standalone mod or an addon to an existing robot platform is more maintainable.
