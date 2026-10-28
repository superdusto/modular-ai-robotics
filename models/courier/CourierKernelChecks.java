// SPDX-License-Identifier: MIT
// Copyright (c) 2026 superdusto

import java.util.ArrayList;
import java.util.List;
import static java.lang.System.out;

/** Independently stated scenario oracles for a candidate model, not Minecraft fixtures. */
public final class CourierKernelChecks {
    private static final CourierKernel.Context ALLOW = CourierKernel.Context.permitted();
    private record ScenarioResult(String id, String name, int assertions) {}
    private static final List<ScenarioResult> passed = new ArrayList<>();
    private static int assertions;
    private static void check(boolean value, String message) {
        assertions++; if (!value) throw new AssertionError(message);
    }
    private static CourierKernel.Job job(int source, int capacity) {
        return new CourierKernel.Job("job", "owner", "request", 16, source, capacity, 20, 6, 6);
    }
    private static CourierKernel.CargoEvidence evidence(CourierKernel.Job j) {
        return new CourierKernel.CargoEvidence(j.id, j.request, j.extracted(), j.delivered(), j.cargo(), true, true);
    }
    private static CourierKernel.Job partialJob() {
        var j = job(64, 16); j.pickup("l", 16, false, ALLOW);
        j.arriveDestination("d", ALLOW); j.unload("u6", 6, ALLOW); return j;
    }
    private static void deliveredBatch(CourierKernel.Job j, int actual, boolean shortfall) {
        check(j.pickup("load", actual, shortfall, ALLOW).equals("SUCCEEDED"), "load");
        check(j.arriveDestination("destination", ALLOW).equals("SUCCEEDED"), "destination");
        check(j.unload("unload", actual, ALLOW).equals("SUCCEEDED"), "unload");
        check(j.home("home", ALLOW).equals("SUCCEEDED"), "home");
        check(j.charge("charge", ALLOW).equals("SUCCEEDED"), "charge");
    }
    private static void scenario(String id, String name, Runnable run) {
        int before = assertions;
        run.run();
        passed.add(new ScenarioResult(id, name, assertions - before));
    }
    public static void main(String[] args) {
        if (!"25".equals(System.getProperty("java.specification.version")))
            throw new IllegalStateException("The candidate model requires JDK 25");
        scenario("M01", "normal delivery requires final service", () -> {
            var j = job(64, 16);
            j.pickup("l", 16, false, ALLOW); j.arriveDestination("d", ALLOW); j.unload("u", 16, ALLOW);
            check(j.state() != CourierKernel.State.SUCCEEDED, "delivery alone cannot finish job");
            j.home("h", ALLOW); check(j.state() != CourierKernel.State.SUCCEEDED, "home alone");
            j.charge("c", ALLOW); check(j.state() == CourierKernel.State.SUCCEEDED, "full completion");
            check(j.source() == 48 && j.cargo() == 0 && j.destination() == 16, "closed count oracle");
        });
        scenario("M02", "source shortfall suspends and needs same-job owner continuation", () -> {
            var j = job(10, 16); deliveredBatch(j, 10, true);
            check(j.state() == CourierKernel.State.SUSPENDED && j.reason().equals("source_shortfall"), "shortfall state");
            int budget = j.productionLeft(); j.duplicateOriginalRequest("request", 16);
            j.fixtureExternalSourceInflow(6);
            check(j.pickup("automatic", 6, false, ALLOW).equals("BATCH_CLOSED"), "no automatic next batch");
            check(j.source() == 6 && j.delivered() == 10, "inflow does not trigger pickup");
            check(j.continueBatch("bad", "stranger", "a2", ALLOW).equals("UNAUTHORIZED"), "owner required");
            check(j.continueBatch("continue", "owner", "a2", ALLOW).equals("RECORDED"), "owner continuation");
            check(j.productionLeft() == budget && j.extracted() == 10 && j.batch() == 2, "retain accounting and limits");
            j.continueBatch("continue", "owner", "a2", ALLOW); check(j.batch() == 2, "command replay");
            j.pickup("load", 10, true, ALLOW); // Historical replay must not certify this batch.
            check(!j.succeeded(CourierKernel.Step.LOAD), "old load is not a new batch certificate");
            check(j.arriveDestination("old-edge", ALLOW).equals("DEPENDENCY_BLOCKED"), "fresh batch dependency");
            j.pickup("load2", 6, false, ALLOW); j.arriveDestination("destination2", ALLOW);
            j.unload("unload2", 6, ALLOW); j.home("home2", ALLOW); j.charge("charge2", ALLOW);
            check(j.extracted() == 16 && j.delivered() == 16 && j.cargo() == 0, "remaining six only");
            check(j.source() + j.cargo() + j.destination() == 16, "initial ten plus explicit inflow six");
        });
        scenario("M03", "capacity-limited batch is not a source shortfall", () -> {
            var j = job(64, 10); deliveredBatch(j, 10, false);
            check(j.state() == CourierKernel.State.SUSPENDED && j.reason().equals("capacity_limited"), "capacity reason");
            check(j.source() == 54 && j.extracted() == 10 && j.delivered() == 10, "bounded capacity");
        });
        scenario("M04", "nonterminal partial pickup holds cargo and blocks downstream", () -> {
            var j = job(64, 16);
            check(j.pickup("partial", 7, false, ALLOW).equals("PARTIAL"), "partial effect");
            check(j.cargo() == 7 && j.source() == 57 && j.reason().equals("pickup_incomplete"), "retain known cargo");
            check(j.arriveDestination("d", ALLOW).equals("DEPENDENCY_BLOCKED"), "no destination release");
            check(j.pickup("topup", 9, false, ALLOW).equals("PICKUP_BLOCKED"), "no top-up");
            var falseProof = job(64, 16);
            check(falseProof.pickup("fake", 7, true, ALLOW).equals("INVALID_SHORTFALL_PROOF"), "no invented shortfall");
            check(falseProof.source() == 64 && falseProof.cargo() == 0, "false proof has no effect");
        });
        scenario("M05", "partial unload blocks home but permits separately scoped safety service", () -> {
            var j = job(64, 16); j.pickup("l", 16, false, ALLOW); j.arriveDestination("d", ALLOW);
            check(j.unload("u", 6, ALLOW).equals("PARTIAL"), "partial insertion");
            check(j.home("h", ALLOW).equals("DEPENDENCY_BLOCKED"), "no normal return");
            check(j.safetyReturn("s", ALLOW).equals("SERVICE_ONLY"), "separate service");
            check(!j.succeeded(CourierKernel.Step.HOME) && !j.succeeded(CourierKernel.Step.UNLOAD), "no normal certificates");
            check(j.delivered() == 6 && j.cargo() == 10, "safety preserves quantities");
        });
        scenario("M06", "retained cargo needs owner validation after simulated restoration", () -> {
            var original = partialJob();
            var j = original.snapshotCopy(); int budget = j.productionLeft();
            check(j.unload("blocked", 10, ALLOW).equals("RECOVERY_REQUIRED"), "restoration cannot dispatch");
            check(j.resumeRetainedCargo("owner-resume", "owner", j.epoch(), "recovered", evidence(j), ALLOW)
                    .equals("RESUME_VALIDATED"), "owner and attributable cargo evidence");
            j.arriveDestination("fresh-destination", ALLOW); j.advanceActiveTicks(2);
            check(j.unload("u10", 10, ALLOW).equals("SUCCEEDED"), "remaining cargo unload");
            check(j.source() == 48 && j.delivered() == 16 && j.cargo() == 0 && j.productionLeft() == budget - 2, "no renewed pickup or budget");
            int after = j.productionLeft(); j.unload("u10", 10, ALLOW);
            check(j.delivered() == 16 && j.productionLeft() == after, "effect replay returns receipt");
        });
        scenario("M07", "record stop works under physical uncertainty and cancellation remains open", () -> {
            var j = job(64, 16); j.pickup("l", 16, false, ALLOW); j.markUncertain();
            var ack = j.stop("cancel", "owner", 0, true, true);
            check(ack.accepted() && ack.fenced() && !ack.effectsResolved(), "separate stop facts");
            check(j.cancelRequested() && j.state() == CourierKernel.State.RECOVERING, "not falsely terminal");
            check(j.resume("owner", j.epoch()).equals("CANCELLED"), "cannot resume cancelled delivery");
            check(j.safetyReturn("s", ALLOW).equals("UNCERTAIN"), "no movement of relevant unknown state");
            check(j.cargo() == 16, "no disposal");
            check(j.stop("cancel", "owner", 0, true, true).equals(ack), "duplicate stop");
        });
        scenario("M08", "stop survives exhausted model work and failed write is explicit", () -> {
            var j = new CourierKernel.Job("j", "owner", "r", 16, 64, 16, 0, 0, 0);
            var ack = j.stop("stop", "owner", 0, false, false);
            check(ack.accepted() && ack.fenced() && !ack.recordWriteAccepted(), "failed write cannot claim persistence");
            check(j.safetyReturn("return", ALLOW).equals("RECORD_WRITE_FAILED"), "failed storage also fences service");
            check(j.controlRecords() == 1 && j.cargo() == 0, "bounded control state");
            var denied = j.stop("foreign", "foreign", j.epoch(), true, true);
            check(!denied.accepted() && !j.cancelRequested(), "control authority independent");
        });
        scenario("M09", "newer stop rejects stale resume", () -> {
            var j = job(64, 16); j.stop("s1", "owner", 0, false, true);
            long old = j.epoch(); j.stop("s2", "owner", old, false, true);
            check(j.resume("owner", old).equals("UNAUTHORIZED_OR_STALE") && j.fenced(), "stale resume fence");
        });
        scenario("M10", "recovery reads use protected finite reserve and denial consumes it", () -> {
            var j = new CourierKernel.Job("j", "owner", "r", 16, 64, 16, 1, 6, 6);
            j.pickup("l", 16, false, ALLOW); j.markUncertain();
            check(j.productionLeft() == 0 && j.recoveryLeft() == 6, "reserve isolated");
            check(j.recoveryPass(false, true) == 1, "no unauthorized evidence");
            check(j.recoveryLeft() == 3 && j.readsLeft() == 2 && j.passesLeft() == 1, "denial charged");
            check(j.recoveryPass(false, false) == 0 && j.recoveryLeft() == 0, "finite recovery exhaustion");
            check(j.snapshotCopy().recoveryPass(true) == 0, "snapshot cannot renew quota");
            check(j.stop("s", "owner", j.epoch(), false, true).accepted(), "control independent of work");
        });
        scenario("M11", "unknown physical context and missing budget history block effects", () -> {
            var unknown = new CourierKernel.Context(true, true, false, true, true, true, true);
            var j = job(64, 16);
            check(j.pickup("l", 16, false, unknown).equals("CONTEXT_BLOCKED"), "unknown custody");
            check(j.source() == 64 && j.cargo() == 0, "blocked context no effect");
            var copy = j.copyWithMissingBudgetHistory();
            check(copy.pickup("new", 16, false, ALLOW).equals("BUDGET_UNKNOWN"), "no default budget");
            check(copy.stop("s", "owner", 0, false, true).accepted(), "record stop still available");
        });
        scenario("M12", "continuation receipts cannot consume the protected stop capacity", () -> {
            var j = new CourierKernel.Job("j", "owner", "r", 64, 64, 1, 100, 6, 6,
                    new CourierKernel.RetryPolicy(java.util.stream.LongStream.rangeClosed(1, 63).boxed().toList(), 1000, 100));
            for (int i = 0; i < 16; i++) {
                check(j.pickup("l" + i, 1, false, ALLOW).equals("SUCCEEDED"), "capacity pickup");
                j.arriveDestination("d" + i, ALLOW); j.unload("u" + i, 1, ALLOW);
                check(j.continueBatch("c" + i, "owner", "attempt" + i, ALLOW).equals("RECORDED"), "continuation receipt");
            }
            check(j.stop("protected-stop", "owner", j.epoch(), false, true).accepted(), "reserved stop after receipt pressure");
        });
        scenario("M13", "control retention exhaustion refuses resume before losing future stop capacity", () -> {
            var j = job(64, 16);
            for (int i = 0; i < 16; i++) {
                check(j.stop("s" + i, "owner", j.epoch(), false, true).accepted(), "finite retained stop");
                String result = j.resume("owner", j.epoch());
                check(result.equals(i < 15 ? "VALIDATE_BEFORE_DISPATCH" : "CONTROL_CAPACITY_OR_STORAGE"), "reserve before resume");
            }
            check(j.fenced(), "exhaustion leaves dispatch disabled");
        });
        scenario("M14", "operation and original-request collisions reject changed intent", () -> {
            var j = job(64, 16); j.pickup("l", 16, false, ALLOW);
            boolean collision = false;
            try { j.pickup("l", 7, false, ALLOW); } catch (IllegalArgumentException e) { collision = true; }
            check(collision, "operation collision"); collision = false;
            try { j.duplicateOriginalRequest("request", 12); } catch (IllegalArgumentException e) { collision = true; }
            check(collision && j.cargo() == 16 && j.source() == 48, "request collision no new effect");
        });
        scenario("M15", "completed jobs and closed batches cannot restart normal work under new operation IDs", () -> {
            var complete = job(64, 16); deliveredBatch(complete, 16, false);
            int production = complete.productionLeft(), service = complete.serviceLeft();
            check(complete.arriveDestination("late-destination", ALLOW).equals("TERMINAL"), "terminal movement fenced");
            check(complete.charge("late-charge", ALLOW).equals("TERMINAL"), "terminal normal charging fenced");
            check(complete.state() == CourierKernel.State.SUCCEEDED && complete.productionLeft() == production
                    && complete.serviceLeft() == service, "terminal state and budgets retained");
            var shortfall = job(10, 16); deliveredBatch(shortfall, 10, true);
            var restored = shortfall.snapshotCopy();
            check(restored.arriveDestination("late", ALLOW).equals("BATCH_CLOSED"), "closed batch needs owner continuation");
            check(restored.state() == CourierKernel.State.SUSPENDED && restored.delivered() == 10, "no automatic resumption");
        });
        scenario("M16", "retained-cargo recovery requires current owner rights and fresh destination context", () -> {
            var j = partialJob().snapshotCopy(); int p = j.productionLeft();
            int r = j.recoveryLeft();
            check(j.resumeRetainedCargo("foreign", "stranger", j.epoch(), "r1", evidence(j), ALLOW)
                    .equals("UNAUTHORIZED_OR_STALE"), "foreign controller rejected");
            check(j.recoveryLeft() == r, "foreign caller cannot spend recovery allocation");
            check(j.resumeRetainedCargo("stale", "owner", j.epoch() - 1, "r1", evidence(j), ALLOW)
                    .equals("UNAUTHORIZED_OR_STALE"), "stale owner command rejected");
            var denied = new CourierKernel.Context(false, true, true, true, true, true, true);
            check(j.resumeRetainedCargo("denied", "owner", j.epoch(), "r1", evidence(j), denied)
                    .equals("CONTEXT_BLOCKED"), "restored rights must be current");
            check(j.fenced() && j.cargo() == 10 && j.delivered() == 6, "denied recovery retains custody");
            check(j.resumeRetainedCargo("valid", "owner", j.epoch(), "r2", evidence(j), ALLOW)
                    .equals("RESUME_VALIDATED"), "fresh owner continuation");
            check(j.batch() == 1 && j.extracted() == 16 && j.productionLeft() == p, "same batch and original production limits");
            j.arriveDestination("d", ALLOW); // A historical success is not a fresh arrival observation.
            check(!j.succeeded(CourierKernel.Step.DESTINATION), "old navigation replay does not restore freshness");
            check(j.unload("stale-destination", 10, ALLOW).equals("DEPENDENCY_BLOCKED"), "old destination receipt stale");
            j.arriveDestination("new-destination", ALLOW); j.advanceActiveTicks(2);
            check(j.unload("remaining", 10, ALLOW).equals("SUCCEEDED"), "only actual remainder");
            j.home("home", ALLOW); j.charge("charge", ALLOW);
            check(j.state() == CourierKernel.State.SUCCEEDED && j.source() == 48 && j.destination() == 16 && j.cargo() == 0,
                    "full recovered batch and service");
        });
        scenario("M17", "denied cargo reads and unattributable matching totals cannot clear recovery", () -> {
            var j = partialJob().snapshotCopy();
            var deniedRead = new CourierKernel.CargoEvidence(j.id, j.request, 16, 6, 10, false, true);
            check(j.resumeRetainedCargo("denied", "owner", j.epoch(), "r1", deniedRead, ALLOW).equals("READ_DENIED"), "read gate independent");
            check(j.readsLeft() == 3 && j.recoveryLeft() == 4, "denied read consumes read and work");
            var unproven = new CourierKernel.CargoEvidence(j.id, j.request, 16, 6, 10, true, false);
            check(j.resumeRetainedCargo("unproven", "owner", j.epoch(), "r2", unproven, ALLOW).equals("EVIDENCE_MISMATCH"), "totals alone insufficient");
            check(j.resumeRetainedCargo("exhausted", "owner", j.epoch(), "r3", evidence(j), ALLOW).equals("RECOVERY_EXHAUSTED"), "no fresh allocation under new ID");
            check(j.fenced() && j.source() == 48 && j.delivered() == 6 && j.cargo() == 10, "no inventory repair");
            var other = partialJob().snapshotCopy();
            var wrongJob = new CourierKernel.CargoEvidence("other-job", other.request, 16, 6, 10, true, true);
            check(other.resumeRetainedCargo("wrong", "owner", other.epoch(), "r1", wrongJob, ALLOW).equals("EVIDENCE_MISMATCH"), "lineage matters");
        });
        scenario("M18", "cancelled or uncertain custody cannot become eligible through a matching recovery request", () -> {
            var cancelled = partialJob(); cancelled.stop("cancel", "owner", 0, true, true);
            var c = cancelled.snapshotCopy();
            check(c.resumeRetainedCargo("r", "owner", c.epoch(), "r1", evidence(c), ALLOW).equals("CANCELLED"), "cancel persists");
            check(c.cancelRequested() && c.fenced() && c.cargo() == 10, "no cancellation laundering");
            var u = partialJob(); u.markUncertain(); u = u.snapshotCopy();
            check(u.resumeRetainedCargo("r", "owner", u.epoch(), "r1", evidence(u), ALLOW).equals("UNCERTAIN"), "aggregate proof cannot resolve unknown effect");
            check(u.uncertain() && u.fenced(), "uncertainty preserved");
        });
        scenario("M19", "recovery command replay cannot undo a newer stop", () -> {
            var j = partialJob().snapshotCopy(); var proof = evidence(j); long oldEpoch = j.epoch();
            check(j.resumeRetainedCargo("r", "owner", oldEpoch, "r1", proof, ALLOW).equals("RESUME_VALIDATED"), "initial continuation");
            int recovery = j.recoveryLeft(); j.stop("newer-stop", "owner", j.epoch(), false, true); long stopEpoch = j.epoch();
            check(j.resumeRetainedCargo("r", "owner", oldEpoch, "r1", proof, ALLOW).equals("RESUME_VALIDATED"), "retained historical result");
            check(j.fenced() && j.epoch() == stopEpoch && j.recoveryLeft() == recovery, "replay is not a new grant");
            boolean collision = false;
            try { j.resumeRetainedCargo("r", "owner", oldEpoch, "different", proof, ALLOW); }
            catch (IllegalArgumentException e) { collision = true; }
            check(collision, "changed continuation intent collides");
        });
        scenario("M20", "partial and zero insertions use cumulative increasing backoff across restoration", () -> {
            var j = partialJob(); int p = j.productionLeft();
            check(j.nextInsertionTick() == 2 && j.insertionAttempts() == 1, "first declared delay");
            check(j.unload("second", 0, ALLOW).equals("RETRY_WAIT") && j.productionLeft() == p, "early eligibility is not an action");
            j.advanceActiveTicks(1);
            check(j.unload("second", 0, ALLOW).equals("RETRY_WAIT") && j.insertionAttempts() == 1, "still early");
            j.advanceActiveTicks(1);
            check(j.unload("second", 0, ALLOW).equals("PARTIAL"), "zero effect retry at due tick");
            check(j.nextInsertionTick() == 6 && j.insertionAttempts() == 2 && j.cargo() == 10, "second larger delay");
            j = j.snapshotCopy();
            check(j.activeTick() == 2 && j.nextInsertionTick() == 6 && j.insertionAttempts() == 2, "clock and attempts retained");
            j.resumeRetainedCargo("r", "owner", j.epoch(), "r1", evidence(j), ALLOW); j.arriveDestination("fresh", ALLOW);
            j.advanceActiveTicks(3); check(j.unload("third", 10, ALLOW).equals("RETRY_WAIT"), "owner cannot shorten wait");
            j.advanceActiveTicks(1); check(j.unload("third", 10, ALLOW).equals("SUCCEEDED"), "same queued identity can execute when due");
            check(j.insertionAttempts() == 3 && j.delivered() == 16 && j.cargo() == 0, "exactly third attempt finishes");
        });
        scenario("M21", "insertion retry exhaustion cannot be renewed by owner or restoration", () -> {
            var j = job(64, 16); j.pickup("l", 16, false, ALLOW); j.arriveDestination("d", ALLOW);
            j.unload("u1", 0, ALLOW); j.advanceActiveTicks(2); j.unload("u2", 0, ALLOW);
            j.advanceActiveTicks(4); j.unload("u3", 0, ALLOW); int p = j.productionLeft();
            check(j.unload("u4", 16, ALLOW).equals("RETRY_LIMIT"), "three total attempts");
            check(j.productionLeft() == p && j.insertionAttempts() == 3, "no fourth effect invocation");
            j = j.snapshotCopy();
            check(j.resumeRetainedCargo("r", "owner", j.epoch(), "r1", evidence(j), ALLOW).equals("DELIVERY_EXHAUSTED"), "owner cannot reset attempts");
            check(j.source() == 48 && j.cargo() == 16 && j.delivered() == 0, "exhaustion retains cargo");
        });
        scenario("M22", "no-progress deadline is not extended by zero effects or new identities", () -> {
            var j = new CourierKernel.Job("j", "owner", "r", 16, 64, 16, 20, 6, 6,
                    new CourierKernel.RetryPolicy(List.of(2L, 4L), 100, 5));
            j.pickup("l", 16, false, ALLOW); j.arriveDestination("d", ALLOW); j.unload("u", 0, ALLOW);
            j.advanceActiveTicks(5);
            check(j.unload("late", 16, ALLOW).equals("NO_PROGRESS_EXHAUSTED"), "exact no-progress boundary");
            j = j.snapshotCopy();
            check(j.resumeRetainedCargo("r", "owner", j.epoch(), "r1", evidence(j), ALLOW).equals("NO_PROGRESS_EXHAUSTED"), "no renewed deadline");
            check(j.cargo() == 16 && j.delivered() == 0 && j.insertionAttempts() == 1, "expired proposal performs no effect");
        });
        scenario("M23", "active deadline fences delivery while bounded recovery and stop remain available", () -> {
            var j = new CourierKernel.Job("j", "owner", "r", 16, 64, 16, 20, 6, 6,
                    new CourierKernel.RetryPolicy(List.of(2L, 4L), 5, 20));
            j.pickup("l", 16, false, ALLOW); j.arriveDestination("d", ALLOW); j.advanceActiveTicks(5);
            check(j.unload("expired", 16, ALLOW).equals("ACTIVE_DEADLINE_EXHAUSTED"), "active deadline");
            check(j.recoveryPass(true) == 1, "finite evidence work independent");
            check(j.stop("s", "owner", j.epoch(), false, true).accepted(), "record-only stop independent");
            j = j.snapshotCopy();
            check(j.activeTick() == 5 && j.resumeRetainedCargo("r", "owner", j.epoch(), "r1", evidence(j), ALLOW)
                    .equals("ACTIVE_DEADLINE_EXHAUSTED"), "clock retained");
            check(j.cargo() == 16 && j.delivered() == 0, "no late delivery");
        });
        scenario("M24", "real material progress advances the no-progress boundary without renewing attempt caps", () -> {
            var j = new CourierKernel.Job("j", "owner", "r", 16, 64, 16, 20, 6, 6,
                    new CourierKernel.RetryPolicy(List.of(2L, 4L), 100, 5));
            j.pickup("l", 16, false, ALLOW); j.arriveDestination("d", ALLOW); j.unload("u1", 4, ALLOW);
            j.advanceActiveTicks(3); check(j.unload("u2", 4, ALLOW).equals("PARTIAL"), "actual second progress");
            j.advanceActiveTicks(3); check(j.unload("u3", 8, ALLOW).equals("RETRY_WAIT"), "backoff still applies");
            j.advanceActiveTicks(1); check(j.unload("u3", 8, ALLOW).equals("SUCCEEDED"), "finish before new no-progress boundary");
            check(j.insertionAttempts() == 3 && j.delivered() == 16, "progress does not renew attempts");
        });
        scenario("M25", "partial-pickup cargo cannot be promoted into a completed load by recovery", () -> {
            var j = job(64, 16); j.pickup("partial", 7, false, ALLOW); j = j.snapshotCopy();
            check(j.resumeRetainedCargo("r", "owner", j.epoch(), "r1", evidence(j), ALLOW).equals("CARGO_NOT_ELIGIBLE"), "load certificate still required");
            check(j.source() == 57 && j.cargo() == 7 && !j.succeeded(CourierKernel.Step.LOAD), "no source repair or fabricated success");
        });
        scenario("M26", "invalid time and retry bounds are rejected without moving model state", () -> {
            boolean rejected = false;
            try { new CourierKernel.RetryPolicy(List.of(4L, 2L), 100, 20); }
            catch (IllegalArgumentException e) { rejected = true; }
            check(rejected, "backoff must increase"); rejected = false;
            try { new CourierKernel.RetryPolicy(List.of(2L), 0, 20); }
            catch (IllegalArgumentException e) { rejected = true; }
            check(rejected, "finite positive deadline");
            var j = job(64, 16); rejected = false;
            try { j.advanceActiveTicks(-1); } catch (IllegalArgumentException e) { rejected = true; }
            check(rejected && j.activeTick() == 0 && j.source() == 64, "clock cannot run backwards");
        });
        scenario("M27", "owner continuation cannot start a new pickup after cumulative insertion attempts are exhausted", () -> {
            var j = job(64, 4);
            for (int i = 0; i < 3; i++) {
                check(j.pickup("l" + i, 4, false, ALLOW).equals("SUCCEEDED"), "one capacity batch");
                j.arriveDestination("d" + i, ALLOW); j.unload("u" + i, 4, ALLOW);
                if (i < 2) check(j.continueBatch("c" + i, "owner", "a" + i, ALLOW).equals("RECORDED"), "remaining bounded continuation");
            }
            check(j.continueBatch("over-limit", "owner", "extra", ALLOW).equals("BLOCKED"), "no new batch without an insertion allowance");
            check(j.pickup("over-limit-load", 4, false, ALLOW).equals("PICKUP_BLOCKED"), "no additional stranded pickup");
            check(j.insertionAttempts() == 3 && j.extracted() == 12 && j.delivered() == 12 && j.cargo() == 0,
                    "original job counts and limits retained");
        });
        out.println("{\"scenarios_passed\":" + passed.size() + ",\"assertions\":" + assertions
                + ",\"scope\":\"candidate_in_memory_model_only\",\"java_version\":\"" + System.getProperty("java.version") + "\",\"scenarios\":[");
        for (int i = 0; i < passed.size(); i++) out.println("  \"" + passed.get(i).name() + "\"" + (i + 1 < passed.size() ? "," : ""));
        out.println("],\"scenario_results\":[");
        for (int i = 0; i < passed.size(); i++) {
            var result = passed.get(i);
            out.println("  {\"id\":\"" + result.id() + "\",\"name\":\"" + result.name()
                    + "\",\"assertions\":" + result.assertions() + "}" + (i + 1 < passed.size() ? "," : ""));
        }
        out.println("]}");
    }
}
