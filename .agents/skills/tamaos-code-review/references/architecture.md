# Architecture review lane

Review only structural fitness and long-term change cost.

Look for:

- violated dependency direction or hardware/domain boundaries;
- unnecessary coupling, duplicate ownership, or a misplaced responsibility;
- incompatible public contracts or persistence formats;
- abstractions added too early, or missing seams required by the accepted design;
- contradictions with accepted ADRs or documented architecture.

Do not re-review ordinary behavioral bugs, test coverage, formatting, or language idioms. Report a blocker only when the structure creates a concrete present risk; distinguish optional design suggestions from required changes.
