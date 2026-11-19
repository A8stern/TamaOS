# Correctness review lane

Review only observable behavior and failure handling.

Look for:

- incorrect results, state transitions, edge cases, and regressions;
- broken callers, contracts, compatibility, or error propagation;
- race, ordering, lifetime, overflow, and resource-state bugs where applicable;
- behavior that contradicts the acceptance criteria or repository invariants.

Do not review general code style, preferred abstractions, test quantity, or documentation unless they reveal a concrete behavior defect. Report each blocker with file/location, triggering scenario, impact, and the smallest safe correction.
