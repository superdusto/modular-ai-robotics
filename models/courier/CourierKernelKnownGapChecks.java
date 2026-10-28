// SPDX-License-Identifier: MIT
// Copyright (c) 2026 superdusto

import java.util.ArrayList;
import java.util.List;

/** Reproduces known defects in the preserved candidate; these are not fixed-behavior verdicts. */
public final class CourierKernelKnownGapChecks {
    private static final CourierKernel.Context ALLOW = CourierKernel.Context.permitted();
    private record Observation(String id, String name, int assertions) {}
    private static final List<Observation> observations = new ArrayList<>();
    private static int assertions;

    private static void check(boolean value, String message) {
        assertions++;
        if (!value) throw new AssertionError(message);
    }

    private static CourierKernel.Job job(int source) {
        return new CourierKernel.Job("job", "owner", "request", 16, source, 16, 20, 6, 6);
    }

    private static void unload(CourierKernel.Job job, int quantity, boolean shortfall) {
        check(job.pickup("load", quantity, shortfall, ALLOW).equals("SUCCEEDED"), "fixture load");
        check(job.arriveDestination("destination", ALLOW).equals("SUCCEEDED"), "fixture destination");
        check(job.unload("unload", quantity, ALLOW).equals("SUCCEEDED"), "fixture unload");
    }

    private static void service(CourierKernel.Job job) {
        check(job.home("home", ALLOW).equals("SUCCEEDED"), "fixture home");
        check(job.charge("charge", ALLOW).equals("SUCCEEDED"), "fixture charge");
    }

    private static void emptyRecoveryRemainsBlocked(CourierKernel.Job job, boolean closedBatch) {
        int source = job.source(), destination = job.destination(), production = job.productionLeft();
        int recovery = job.recoveryLeft(), service = job.serviceLeft();
        check(job.cargo() == 0 && job.fenced() && job.recoveryRequired(), "restored empty job is fenced");
        check(job.resume("owner", job.epoch()).equals("RECOVERY_REQUIRED"), "ordinary resume cannot clear recovery");
        var proof = new CourierKernel.CargoEvidence(job.id, job.request, job.extracted(),
                job.delivered(), 0, true, true);
        check(job.resumeRetainedCargo("recover-empty", "owner", job.epoch(), "recovered", proof, ALLOW)
                .equals("CARGO_NOT_ELIGIBLE"), "positive cargo required by existing recovery");
        check(job.continueBatch("continue", "owner", "next", ALLOW).equals("BLOCKED"), "batch continuation blocked");
        String physicalBlock = closedBatch ? "BATCH_CLOSED" : "RECOVERY_REQUIRED";
        check(job.pickup("fresh-load", 0, false, ALLOW).equals(physicalBlock), "no pickup workaround");
        check(job.home("fresh-home", ALLOW).equals(physicalBlock), "no home workaround");
        check(job.charge("fresh-charge", ALLOW).equals(physicalBlock), "no charge workaround");
        check(job.fenced() && job.recoveryRequired(), "fence remains after denied commands");
        check(job.source() == source && job.destination() == destination && job.cargo() == 0,
                "known gap performs no item effects");
        check(job.productionLeft() == production && job.recoveryLeft() == recovery && job.serviceLeft() == service,
                "denied dispatch does not replenish or spend physical/recovery work");
    }

    private static void postTerminalStop(boolean cancel) {
        var job = job(64);
        unload(job, 16, false);
        service(job);
        check(job.state() == CourierKernel.State.SUCCEEDED, "job completed before new control");
        int production = job.productionLeft(), service = job.serviceLeft();
        long epoch = job.epoch();
        var ack = job.stop("late-stop", "owner", epoch, cancel, true);
        check(ack.accepted() && ack.fenced(), "candidate accepts post-terminal control");
        check(job.state() == (cancel ? CourierKernel.State.CANCELLED : CourierKernel.State.SUSPENDED),
                "known defect overwrites completed status");
        check(job.epoch() == epoch + 1 && job.cancelRequested() == cancel, "candidate mutates control state");
        check(job.source() == 48 && job.destination() == 16 && job.cargo() == 0 && job.delivered() == 16,
                "status defect does not reverse completed delivery");
        check(job.productionLeft() == production && job.serviceLeft() == service, "control retains spent work");
    }

    private static void continuationBudgetBoundary() {
        for (int initialProduction = 4; initialProduction <= 6; initialProduction++) {
            var job = new CourierKernel.Job("job", "owner", "request", 16, 16, 8, initialProduction, 6, 6);
            unload(job, 8, false);
            service(job);
            int remaining = initialProduction - 3;
            check(job.productionLeft() == remaining && job.cargo() == 0 && job.delivered() == 8,
                    "first batch leaves the expected production remainder");
            check(job.succeeded(CourierKernel.Step.HOME) && job.succeeded(CourierKernel.Step.CHARGE),
                    "service is complete; this gap is independent of the missing service gate");
            check(job.continueBatch("next-batch", "owner", "second", ALLOW).equals("RECORDED"),
                    "candidate accepts continuation with any positive production remainder");
            check(job.productionLeft() == remaining, "continuation does not replenish the remainder");
            check(job.pickup("second-load", 8, false, ALLOW).equals("SUCCEEDED"), "second pickup admitted");
            String navigation = job.arriveDestination("second-destination", ALLOW);
            check(navigation.equals(remaining == 1 ? "EXHAUSTED" : "SUCCEEDED"),
                    "one remaining unit strands cargo before navigation");
            String delivery = job.unload("second-unload", 8, ALLOW);
            check(delivery.equals(remaining == 1 ? "DEPENDENCY_BLOCKED" : remaining == 2 ? "EXHAUSTED" : "SUCCEEDED"),
                    "two remaining units strand cargo before delivery; three permit the fixed path");
            check(job.productionLeft() == 0 && job.recoveryLeft() == 6 && job.serviceLeft() == 4,
                    "no production renewal or borrowing from protected work");
            check(job.source() == 0 && job.extracted() == 16 && job.delivered() == (remaining < 3 ? 8 : 16)
                    && job.cargo() == (remaining < 3 ? 8 : 0), "cargo and delivered counts retain exact custody");
            check(job.source() + job.destination() + job.cargo() == 16, "closed fixture conserves all items");
            if (remaining == 3) {
                check(job.home("second-home", ALLOW).equals("SUCCEEDED"), "sufficient-boundary normal home");
                check(job.charge("second-charge", ALLOW).equals("SUCCEEDED"), "sufficient-boundary normal charge");
                check(job.state() == CourierKernel.State.SUCCEEDED, "sufficient fixed-path boundary completes");
            }
        }
    }

    private static void observe(String id, String name, Runnable run) {
        int before = assertions;
        run.run();
        observations.add(new Observation(id, name, assertions - before));
    }

    public static void main(String[] args) {
        if (!"25".equals(System.getProperty("java.specification.version")))
            throw new IllegalStateException("Known-gap observations require JDK 25");
        observe("KG01", "empty restoration before first pickup remains fenced", () -> {
            emptyRecoveryRemainsBlocked(job(64).snapshotCopy(), false);
        });
        observe("KG02", "empty restoration after unload before service remains fenced", () -> {
            var job = job(64);
            unload(job, 16, false);
            check(!job.succeeded(CourierKernel.Step.HOME) && !job.succeeded(CourierKernel.Step.CHARGE),
                    "service incomplete at restoration boundary");
            emptyRecoveryRemainsBlocked(job.snapshotCopy(), false);
        });
        observe("KG03", "empty restoration after incomplete batch service remains fenced", () -> {
            var job = job(8);
            unload(job, 8, true);
            service(job);
            check(job.state() == CourierKernel.State.SUSPENDED && job.delivered() < job.requested,
                    "closed batch still needs another pickup");
            emptyRecoveryRemainsBlocked(job.snapshotCopy(), true);
        });
        observe("KG04", "post-completion pause overwrites terminal state", () -> postTerminalStop(false));
        observe("KG05", "post-completion cancel overwrites terminal state", () -> postTerminalStop(true));
        observe("KG06", "continuation admits pickup with insufficient remaining production work",
                CourierKernelKnownGapChecks::continuationBudgetBoundary);
        System.out.println("{\"scope\":\"candidate_known_gap_observations\",\"status\":\"observed_unfixed\","
                + "\"assertions\":" + assertions + ",\"observations\":[");
        for (int i = 0; i < observations.size(); i++) {
            var result = observations.get(i);
            System.out.println("  {\"id\":\"" + result.id() + "\",\"name\":\"" + result.name()
                    + "\",\"assertions\":" + result.assertions() + "}" + (i + 1 < observations.size() ? "," : ""));
        }
        System.out.println("]}");
    }
}
