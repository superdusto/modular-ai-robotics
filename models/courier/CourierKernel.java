// SPDX-License-Identifier: MIT
// Copyright (c) 2026 superdusto

import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Set;

/** Candidate in-memory design model. No Minecraft, disk, network or actor authentication. */
public final class CourierKernel {
    public enum State { NEW, CARRYING, UNLOADING, SUSPENDED, RECOVERING, CANCELLED, SUCCEEDED }
    public enum Step { LOAD, DESTINATION, UNLOAD, HOME, CHARGE }
    private enum Allocation { PRODUCTION, SERVICE }

    /** Values emulate already-established server evidence; never use as client authorization. */
    public record Context(boolean rights, boolean body, boolean custody, boolean energy,
                          boolean loaded, boolean hardware, boolean serviceGrant) {
        public static Context permitted() { return new Context(true, true, true, true, true, true, true); }
        boolean physicalReady() { return rights && body && custody && energy && loaded && hardware; }
    }
    public record ControlAck(boolean accepted, boolean recordWriteAccepted,
                             boolean fenced, boolean effectsResolved, long epoch) {}
    /** Synthetic active-time limits, not measured Minecraft tick or performance defaults. */
    public record RetryPolicy(List<Long> backoffTicks, long activeTickLimit, long noProgressTickLimit) {
        public RetryPolicy {
            backoffTicks = List.copyOf(backoffTicks);
            if (backoffTicks.size() > 63 || activeTickLimit <= 0 || activeTickLimit > 1_000_000
                    || noProgressTickLimit <= 0 || noProgressTickLimit > 1_000_000)
                throw new IllegalArgumentException("Invalid finite model limits");
            long previous = 0;
            for (long delay : backoffTicks) {
                if (delay <= previous || delay > 1_000_000) throw new IllegalArgumentException("Backoff must increase");
                previous = delay;
            }
        }
        public static RetryPolicy fixtureDefault() { return new RetryPolicy(List.of(2L, 4L), 100, 20); }
        public int maxAttempts() { return backoffTicks.size() + 1; }
    }
    /** Already-attributed fixture evidence, never a client-supplied proof or physical repair request. */
    public record CargoEvidence(String job, String request, int extracted, int delivered, int cargo,
                                boolean readAllowed, boolean receiptsAttributable) {}
    private record Operation(String intent, String result) {}

    public static final class Job {
        public final String id, owner, request;
        public final int requested, cargoCapacity;
        private final RetryPolicy retryPolicy;
        private int source, destination, cargo, extracted, delivered;
        private int production, recovery, service, recoveryReads = 4, recoveryPasses = 2;
        private int batch = 1;
        private long epoch;
        private long activeTick, lastMaterialProgressTick, nextInsertionTick;
        private int insertionAttempts;
        private boolean fenced, cancelled, uncertain, recordWriteFailed, batchClosed, recoveryRequired, budgetsKnown = true;
        private State state = State.NEW;
        private String reason = "", attempt = "initial", destinationContextAttempt = "";
        private final Set<String> attemptIds = new HashSet<>(Set.of("initial"));
        private final Map<String, Operation> operations = new HashMap<>();
        private final Map<String, String> certificates = new HashMap<>();
        private final Map<String, Operation> commands = new HashMap<>();
        private final Map<String, ControlAck> stopAcks = new HashMap<>();

        public Job(String id, String owner, String request, int quantity, int initialSource,
                   int capacity, int production, int recovery, int service) {
            this(id, owner, request, quantity, initialSource, capacity, production, recovery, service,
                    RetryPolicy.fixtureDefault());
        }
        public Job(String id, String owner, String request, int quantity, int initialSource,
                   int capacity, int production, int recovery, int service, RetryPolicy retryPolicy) {
            if (quantity <= 0 || quantity > 64 || initialSource < 0 || capacity <= 0
                    || production < 0 || recovery < 0 || service < 0)
                throw new IllegalArgumentException("Invalid model fixture");
            this.id = Objects.requireNonNull(id); this.owner = Objects.requireNonNull(owner);
            this.request = Objects.requireNonNull(request); requested = quantity;
            source = initialSource; cargoCapacity = capacity;
            this.production = production; this.recovery = recovery; this.service = service;
            this.retryPolicy = Objects.requireNonNull(retryPolicy);
        }
        private Job(Job old) {
            this(old.id, old.owner, old.request, old.requested, old.source, old.cargoCapacity,
                    old.production, old.recovery, old.service, old.retryPolicy);
            destination = old.destination; cargo = old.cargo; extracted = old.extracted;
            delivered = old.delivered; recoveryReads = old.recoveryReads;
            recoveryPasses = old.recoveryPasses; batch = old.batch; epoch = old.epoch;
            fenced = old.fenced; cancelled = old.cancelled; uncertain = old.uncertain;
            recordWriteFailed = old.recordWriteFailed;
            batchClosed = old.batchClosed;
            recoveryRequired = old.recoveryRequired;
            activeTick = old.activeTick; lastMaterialProgressTick = old.lastMaterialProgressTick;
            nextInsertionTick = old.nextInsertionTick; insertionAttempts = old.insertionAttempts;
            destinationContextAttempt = old.destinationContextAttempt;
            attemptIds.addAll(old.attemptIds);
            budgetsKnown = old.budgetsKnown; state = old.state; reason = old.reason; attempt = old.attempt;
            operations.putAll(old.operations); certificates.putAll(old.certificates);
            commands.putAll(old.commands); stopAcks.putAll(old.stopAcks);
        }
        public Job snapshotCopy() { // Simulated activation, not disk serialization or durability.
            Job restored = new Job(this);
            restored.recoveryRequired = true; restored.fenced = true; restored.destinationContextAttempt = "";
            if (!restored.batchClosed && !restored.cancelled) restored.state = State.RECOVERING;
            return restored;
        }
        public Job copyWithMissingBudgetHistory() { Job j = snapshotCopy(); j.budgetsKnown = false; return j; }
        public int source() { return source; }
        public int destination() { return destination; }
        public int cargo() { return cargo; }
        public int extracted() { return extracted; }
        public int delivered() { return delivered; }
        public int productionLeft() { return production; }
        public int recoveryLeft() { return recovery; }
        public int serviceLeft() { return service; }
        public int readsLeft() { return recoveryReads; }
        public int passesLeft() { return recoveryPasses; }
        public int batch() { return batch; }
        public long epoch() { return epoch; }
        public State state() { return state; }
        public String reason() { return reason; }
        public boolean fenced() { return fenced; }
        public boolean cancelRequested() { return cancelled; }
        public boolean uncertain() { return uncertain; }
        public long activeTick() { return activeTick; }
        public long nextInsertionTick() { return nextInsertionTick; }
        public int insertionAttempts() { return insertionAttempts; }
        public boolean recoveryRequired() { return recoveryRequired; }
        public int controlRecords() { return commands.isEmpty() ? 0 : 1; }
        private String key(Step step) { return batch + ":" + step; }
        public boolean succeeded(Step step) {
            return "SUCCEEDED".equals(certificates.get(key(step)))
                    && (step != Step.DESTINATION || destinationContextAttempt.equals(attempt));
        }
        private void certify(Step step, String result) {
            certificates.put(key(step), result);
            if (step == Step.DESTINATION) destinationContextAttempt = attempt;
        }
        public void advanceActiveTicks(long ticks) {
            if (ticks < 0) throw new IllegalArgumentException("Active time cannot move backwards");
            activeTick = Math.addExact(activeTick, ticks);
            if (!cancelled && !uncertain && !batchClosed && activeTick >= retryPolicy.activeTickLimit) {
                state = State.SUSPENDED; reason = "active_deadline";
            }
        }
        private String timeBlock(boolean insertion) {
            if (activeTick >= retryPolicy.activeTickLimit) return "ACTIVE_DEADLINE_EXHAUSTED";
            if (insertion && activeTick - lastMaterialProgressTick >= retryPolicy.noProgressTickLimit)
                return "NO_PROGRESS_EXHAUSTED";
            return null;
        }
        private boolean spend(Allocation kind) {
            if (!budgetsKnown) return false;
            if (kind == Allocation.PRODUCTION) { if (production == 0) return false; production--; }
            else { if (service == 0) return false; service--; }
            return true;
        }
        private String perform(String op, String intent, Allocation allocation, Context context,
                               java.util.function.Supplier<String> effect) {
            Operation prior = operations.get(op);
            if (prior != null) {
                if (!prior.intent.equals(intent)) throw new IllegalArgumentException("Operation collision");
                return prior.result;
            }
            if (operations.size() >= 64) return "RECEIPT_CAPACITY";
            String result;
            if (batchClosed && !intent.equals("safetyReturn")) result = state == State.SUCCEEDED ? "TERMINAL" : "BATCH_CLOSED";
            else if (recordWriteFailed) result = "RECORD_WRITE_FAILED";
            else if (!budgetsKnown) result = "BUDGET_UNKNOWN";
            else if (recoveryRequired) result = "RECOVERY_REQUIRED";
            else if (allocation == Allocation.PRODUCTION && (fenced || cancelled)) result = "FENCED";
            else if (!intent.equals("safetyReturn") && timeBlock(false) != null) result = timeBlock(false);
            else if (!spend(allocation)) result = "EXHAUSTED";
            else if (uncertain) result = "UNCERTAIN";
            else if (!context.physicalReady()) {
                result = "CONTEXT_BLOCKED";
                if (intent.startsWith("unload:")) insertionAttempts++;
                if (allocation == Allocation.PRODUCTION) {
                    fenced = true; recoveryRequired = cargo > 0; state = State.SUSPENDED;
                }
            }
            else if (allocation == Allocation.SERVICE && !context.serviceGrant) result = "SERVICE_DENIED";
            else {
                if (intent.startsWith("unload:")) insertionAttempts++;
                result = effect.get();
            }
            operations.put(op, new Operation(intent, result));
            return result;
        }
        public String pickup(String op, int actual, boolean shortfallProof, Context context) {
            return perform(op, "pickup:" + actual + ":" + shortfallProof, Allocation.PRODUCTION, context, () -> {
                if (cargo != 0 || succeeded(Step.LOAD) || "pickup_incomplete".equals(reason)) return "PICKUP_BLOCKED";
                int target = Math.min(requested - extracted, cargoCapacity);
                if (actual < 0 || actual > target || actual > source) return "INVALID_EFFECT";
                boolean shortfall = actual > 0 && actual < target && actual == source && shortfallProof;
                if (shortfallProof && !shortfall) return "INVALID_SHORTFALL_PROOF";
                source -= actual; cargo += actual; extracted += actual;
                if (actual > 0) lastMaterialProgressTick = activeTick;
                if (actual == 0) { reason = "no_stock"; state = State.SUSPENDED; return "ZERO"; }
                if (actual == target || shortfall) {
                    certify(Step.LOAD, "SUCCEEDED"); state = State.CARRYING;
                    reason = shortfall ? "source_shortfall" : extracted < requested ? "capacity_limited" : "";
                    return "SUCCEEDED";
                }
                certify(Step.LOAD, "PARTIAL"); reason = "pickup_incomplete"; state = State.SUSPENDED;
                return "PARTIAL";
            });
        }
        public String arriveDestination(String op, Context context) {
            return perform(op, "destination", Allocation.PRODUCTION, context, () -> {
                if (!succeeded(Step.LOAD)) return "DEPENDENCY_BLOCKED";
                certify(Step.DESTINATION, "SUCCEEDED"); state = State.UNLOADING; return "SUCCEEDED";
            });
        }
        public String unload(String op, int actual, Context context) {
            Operation prior = operations.get(op);
            if (prior != null) {
                if (!prior.intent.equals("unload:" + actual)) throw new IllegalArgumentException("Operation collision");
                return prior.result;
            }
            if (recoveryRequired) return "RECOVERY_REQUIRED";
            if (fenced || cancelled) return "FENCED";
            if (!succeeded(Step.LOAD) || !succeeded(Step.DESTINATION) || cargo == 0) return "DEPENDENCY_BLOCKED";
            String timed = timeBlock(true);
            if (timed != null) { state = State.SUSPENDED; return timed; }
            if (insertionAttempts >= retryPolicy.maxAttempts()) { state = State.SUSPENDED; return "RETRY_LIMIT"; }
            if (activeTick < nextInsertionTick) return "RETRY_WAIT"; // Eligibility only; no effect invocation or receipt.
            return perform(op, "unload:" + actual, Allocation.PRODUCTION, context, () -> {
                if (actual < 0 || actual > cargo || actual > requested - delivered) return "INVALID_EFFECT";
                cargo -= actual; destination += actual; delivered += actual;
                if (actual > 0) lastMaterialProgressTick = activeTick;
                String result = cargo == 0 ? "SUCCEEDED" : "PARTIAL";
                certify(Step.UNLOAD, result); state = cargo == 0 ? State.UNLOADING : State.SUSPENDED;
                if (cargo > 0 && insertionAttempts < retryPolicy.maxAttempts())
                    nextInsertionTick = Math.addExact(activeTick, retryPolicy.backoffTicks.get(insertionAttempts - 1));
                return result;
            });
        }
        public String home(String op, Context context) {
            return perform(op, "home", Allocation.SERVICE, context, () -> {
                if (!succeeded(Step.UNLOAD) || cargo != 0 || fenced || cancelled) return "DEPENDENCY_BLOCKED";
                certify(Step.HOME, "SUCCEEDED"); return "SUCCEEDED";
            });
        }
        public String charge(String op, Context context) {
            return perform(op, "charge", Allocation.SERVICE, context, () -> {
                if (!succeeded(Step.HOME) || fenced || cancelled) return "DEPENDENCY_BLOCKED";
                certify(Step.CHARGE, "SUCCEEDED");
                state = delivered == requested && cargo == 0 ? State.SUCCEEDED : State.SUSPENDED;
                batchClosed = true;
                return "SUCCEEDED";
            });
        }
        public String safetyReturn(String op, Context context) {
            return perform(op, "safetyReturn", Allocation.SERVICE, context, () -> "SERVICE_ONLY");
        }
        public String continueBatch(String command, String actor, String newAttempt, Context context) {
            String intent = "continuation:" + actor + ":" + newAttempt;
            Operation prior = commands.get(command);
            if (prior != null) {
                if (!prior.intent.equals(intent)) throw new IllegalArgumentException("Command collision");
                return prior.result;
            }
            if (commands.size() >= 16) return "CONTROL_CAPACITY";
            if (!owner.equals(actor)) return "UNAUTHORIZED";
            if (fenced || cancelled || uncertain || recoveryRequired || recordWriteFailed
                    || !budgetsKnown || !context.physicalReady() || timeBlock(false) != null) return "BLOCKED";
            if (cargo != 0 || delivered >= requested || !succeeded(Step.UNLOAD) || production == 0
                    || insertionAttempts >= retryPolicy.maxAttempts()) return "BLOCKED";
            if (attemptIds.contains(newAttempt)) return "ATTEMPT_COLLISION";
            batch++; attempt = newAttempt; reason = ""; state = State.NEW; batchClosed = false;
            attemptIds.add(newAttempt); destinationContextAttempt = "";
            commands.put(command, new Operation(intent, "RECORDED"));
            return "RECORDED";
        }
        public String resumeRetainedCargo(String command, String actor, long expectedEpoch, String newAttempt,
                                          CargoEvidence evidence, Context context) {
            String intent = "cargo-continuation:" + actor + ":" + expectedEpoch + ":" + newAttempt + ":" + evidence;
            Operation prior = commands.get(command);
            if (prior != null) {
                if (!prior.intent.equals(intent)) throw new IllegalArgumentException("Command collision");
                return prior.result;
            }
            if (!owner.equals(actor) || epoch != expectedEpoch) return "UNAUTHORIZED_OR_STALE";
            if (commands.size() >= 16 || stopAcks.size() >= 16) return "CONTROL_CAPACITY";
            String result;
            if (cancelled) result = "CANCELLED";
            else if (uncertain) result = "UNCERTAIN";
            else if (recordWriteFailed || !budgetsKnown) result = "RECORD_OR_BUDGET_UNKNOWN";
            else if (timeBlock(true) != null) result = timeBlock(true);
            else if (insertionAttempts >= retryPolicy.maxAttempts() || production == 0) result = "DELIVERY_EXHAUSTED";
            else if (attemptIds.contains(newAttempt)) result = "ATTEMPT_COLLISION";
            else if (cargo <= 0 || !succeeded(Step.LOAD) || batchClosed) result = "CARGO_NOT_ELIGIBLE";
            else if (recoveryPasses == 0 || recoveryReads == 0 || recovery < 2) result = "RECOVERY_EXHAUSTED";
            else {
                recoveryPasses--; recoveryReads--; recovery -= 2; // One pass plus one independently gated cargo read.
                if (!evidence.readAllowed) result = "READ_DENIED";
                else if (!id.equals(evidence.job) || !request.equals(evidence.request)
                        || !evidence.receiptsAttributable || evidence.extracted != extracted
                        || evidence.delivered != delivered || evidence.cargo != cargo || extracted != delivered + cargo)
                    result = "EVIDENCE_MISMATCH";
                else if (!context.physicalReady()) result = "CONTEXT_BLOCKED";
                else {
                    attempt = newAttempt; attemptIds.add(newAttempt); epoch++;
                    fenced = false; recoveryRequired = false; destinationContextAttempt = "";
                    state = State.CARRYING; result = "RESUME_VALIDATED";
                }
            }
            commands.put(command, new Operation(intent, result));
            return result;
        }
        public ControlAck stop(String command, String actor, long expectedEpoch, boolean cancel, boolean recordWriteAccepted) {
            String intent = "stop:" + actor + ":" + expectedEpoch + ":" + cancel + ":" + recordWriteAccepted;
            Operation prior = commands.get(command);
            if (prior != null) {
                if (!prior.intent.equals(intent)) throw new IllegalArgumentException("Command collision");
                return stopAcks.get(command);
            }
            if (!owner.equals(actor) || expectedEpoch != epoch || stopAcks.size() >= 16)
                return new ControlAck(false, false, fenced, !uncertain, epoch);
            fenced = true; cancelled |= cancel; epoch++;
            recordWriteFailed |= !recordWriteAccepted;
            state = uncertain ? State.RECOVERING : cancelled ? State.CANCELLED : State.SUSPENDED;
            ControlAck ack = new ControlAck(true, recordWriteAccepted, true, !uncertain, epoch);
            commands.put(command, new Operation(intent, "STOP")); stopAcks.put(command, ack);
            return ack;
        }
        public String resume(String actor, long expectedEpoch) {
            if (!owner.equals(actor) || expectedEpoch != epoch) return "UNAUTHORIZED_OR_STALE";
            if (cancelled) return "CANCELLED";
            if (stopAcks.size() >= 16 || recordWriteFailed) return "CONTROL_CAPACITY_OR_STORAGE";
            epoch++;
            if (uncertain || recoveryRequired || cargo > 0) return "RECOVERY_REQUIRED";
            fenced = false; return "VALIDATE_BEFORE_DISPATCH";
        }
        public void markUncertain() { uncertain = true; state = State.RECOVERING; }
        /** Bounded evidence observations; these do not resolve unknown effects from aggregate counts. */
        public int recoveryPass(boolean... resourceReadable) {
            if (!budgetsKnown || recoveryPasses == 0 || recovery == 0) return 0;
            recoveryPasses--; recovery--; int observations = 0;
            for (boolean allowed : resourceReadable) {
                if (recoveryReads == 0 || recovery == 0) break;
                recoveryReads--; recovery--; if (allowed) observations++;
            }
            return observations;
        }
        /** Fixture actor inflow, not a courier action or an authorized product command. */
        public void fixtureExternalSourceInflow(int amount) {
            if (amount < 0) throw new IllegalArgumentException(); source = Math.addExact(source, amount);
        }
        public boolean duplicateOriginalRequest(String requestId, int quantity) {
            if (!request.equals(requestId) || requested != quantity) throw new IllegalArgumentException("Intent collision");
            return true;
        }
    }
}
