"""Original boolean probe sequences with independently specified expected states."""


def make_case(index):
    kind = index % 10
    data = {"probes": []}
    if kind == 0:
        data["failure_threshold"] = 0
        description = "reject zero consecutive-failure thresholds"
    elif kind == 1:
        data["success_threshold"] = True
        description = "reject booleans as success thresholds"
    elif kind == 2:
        data["probes"] = ["ok"]
        description = "reject non-boolean probe outcomes"
    elif kind == 3:
        data["initial_ready"] = "yes"
        description = "reject non-boolean initial readiness"
    elif kind == 4:
        data["unknown"] = index
        description = "reject unknown probe-policy fields"
    elif kind == 5:
        data.update({"failure_threshold": 2, "probes": [True, False, False]})
        expected = {"states": ["ready", "ready", "unready"], "ready": False, "success_streak": 0, "failure_streak": 2}
        description = "retain readiness until the consecutive-failure limit"
    elif kind == 6:
        data.update({"success_threshold": 2, "failure_threshold": 1, "probes": [True, False, True, True]})
        expected = {"states": ["unready", "unready", "unready", "ready"], "ready": True, "success_streak": 2, "failure_streak": 0}
        description = "require consecutive successes after an interrupted recovery"
    elif kind == 7:
        data.update({"initial_ready": True, "failure_threshold": 3, "probes": [False, False, True, False]})
        expected = {"states": ["ready", "ready", "ready", "ready"], "ready": True, "success_streak": 0, "failure_streak": 1}
        description = "reset failure streaks when a probe succeeds"
    elif kind == 8:
        initial = (index // 10) % 2 == 0
        data["initial_ready"] = initial
        expected = {"states": [], "ready": initial, "success_streak": 0, "failure_streak": 0}
        description = "preserve initial readiness when no probes are supplied"
    else:
        count = 1 + (index // 10) % 5
        data.update({"success_threshold": count, "probes": [True] * count})
        expected = {"states": ["unready"] * (count - 1) + ["ready"], "ready": True, "success_streak": count, "failure_streak": 0}
        description = "become ready exactly at the consecutive-success threshold"
    case = {"id": "health-{:04d}".format(index), "description": description, "input": data}
    case.update({"expected_error": True} if kind < 5 else {"expected": expected})
    return case
