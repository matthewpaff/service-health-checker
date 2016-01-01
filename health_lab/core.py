"""Evaluate mock probe hysteresis; no requests or process/container inspection."""


def threshold(value, label):
    if type(value) is not int or not 1 <= value <= 10:
        raise ValueError("{} must be an integer from 1 to 10".format(label))
    return value


def evaluate_health(data):
    allowed = {"probes", "failure_threshold", "success_threshold", "initial_ready"}
    if not isinstance(data, dict) or "probes" not in data or not set(data) <= allowed:
        raise ValueError("Supply probes and optional thresholds/initial_ready")
    probes = data["probes"]
    if not isinstance(probes, list) or len(probes) > 1000 or any(type(probe) is not bool for probe in probes):
        raise ValueError("probes must be a list of at most 1000 booleans")
    failures_required = threshold(data.get("failure_threshold", 3), "failure_threshold")
    successes_required = threshold(data.get("success_threshold", 1), "success_threshold")
    ready = data.get("initial_ready", False)
    if type(ready) is not bool:
        raise ValueError("initial_ready must be true or false")
    successes = failures = 0
    states = []
    for succeeded in probes:
        if succeeded:
            successes += 1
            failures = 0
            if successes >= successes_required:
                ready = True
        else:
            failures += 1
            successes = 0
            if failures >= failures_required:
                ready = False
        states.append("ready" if ready else "unready")
    return {"states": states, "ready": ready, "success_streak": successes, "failure_streak": failures}
