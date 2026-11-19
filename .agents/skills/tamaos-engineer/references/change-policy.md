# Engineering change policy

## Before changing the system

1. Read the canonical source for the affected concern from `system-map.md`.
2. Inspect the actual files, commands, callers, and live GitHub state involved.
3. State the outcome, acceptance criteria, unknowns, and external side effects.
4. Confirm that the change belongs to the engineering system rather than a language agent.

## Repository changes

- Start from an up-to-date `main` and use a short-lived branch.
- Preserve the root `make` interface. Extend a project `.harness` adapter instead of teaching the root runner a language.
- Add a focused regression check for non-trivial harness logic.
- Run the narrow verification, `make ci`, and `git diff --check`.
- Submit a pull request, wait for required checks, squash-merge, and synchronize local `main`.

## External state

GitHub settings, pushes, merges, releases, deployments, credentials, and other external mutations require authority from the current task. Read-only inspection does not imply permission to change them.

Verify external state after mutation. Record stable policy in repository documentation and temporary execution evidence in the issue or pull request.

## Knowledge maintenance

Update `system-map.md` only when a stable engineering fact changes. Do not log routine work or duplicate GitHub history there. Use an ADR for a consequential decision with alternatives and reversal cost.

If a fact is unknown, name the check that will resolve it. If a check was not run, do not present the planned result as evidence.
