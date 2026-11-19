# Verification and risk review lane

Review only evidence quality and non-functional risk.

Look for:

- acceptance criteria without a meaningful automated or documented check;
- tests that cannot fail for the changed behavior, missing failure-path tests, or unverified migrations;
- security, privacy, electrical safety, performance, memory, timing, recovery, and data-loss risks relevant to the change;
- build, packaging, feature-flag, or platform combinations left unverified;
- claims that exceed the observed evidence.

Do not prefer a different architecture or duplicate a demonstrated correctness defect. Report the exact missing evidence or risk, why it matters, and the smallest check or mitigation that would clear the blocker.
