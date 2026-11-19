# Language review skill contract

Each supported programming language provides one review profile containing three real, separately discoverable skills. The common harness defines their responsibilities and interface; it does not pretend that generic prompts are language expertise.

## Required profile

For a language such as `rust`, the profile must name three different skills:

| Lane | Required language-specific knowledge | Excluded ownership |
|---|---|---|
| `correctness` | language semantics, runtime behavior, error handling, concurrency and resource rules | architecture preferences and test sufficiency |
| `architecture` | module/package boundaries, public contracts, dependency direction and ecosystem-specific structural costs | ordinary behavior bugs and verification evidence |
| `verification-risk` | native formatter, linter, compiler, test runner, feature/build matrix and relevant non-functional evidence | choosing a different design or duplicating demonstrated bugs |

Recommended names are `<project>-<language>-review-correctness`, `<project>-<language>-review-architecture`, and `<project>-<language>-review-verification`, but the harness records actual skill IDs rather than inferring names.

Do not register a partial profile. If any lane is missing, the language cannot pass the local review gate.

After the three concrete skills are selected, register their exact IDs under that language in `harness/review-profiles.json`. Keep the registry empty for a language until all three skills exist; never add placeholder IDs.

## Common inputs

Every skill receives the same:

- full immutable commit SHA and intended base;
- acceptance criteria and non-goals;
- changed files in its language scope;
- applicable `AGENTS.md`, architecture, and project rules;
- language/toolchain version and project adapter when known.

Reviewers are distinct, read-only, run independently, and do not see other reports before finishing. Each reviewer loads only its assigned review skill.

## Finding ownership

Route by the claim:

- a concrete trigger producing wrong behavior belongs to `correctness`;
- a boundary or ownership violation whose harm exists even while current behavior works belongs to `architecture`;
- an unproven completion claim or non-functional risk without a demonstrated behavior defect belongs to `verification-risk`.

An out-of-lane concern goes in `notes` with the target lane; it is not a blocker until that lane independently confirms it. Style and preference are never blockers unless a scoped repository rule makes them requirements.

## Required report

Each skill returns one JSON object:

```json
{
  "schema": 2,
  "commit": "<full SHA>",
  "language": "rust",
  "lane": "correctness",
  "skill": "<actual language-specific skill ID>",
  "reviewer": "<distinct agent ID>",
  "verdict": "pass",
  "blocking_findings": [],
  "notes": []
}
```

`verdict` is `fail` when blocking findings remain. A new commit invalidates every report.

## Current limitation

The initial gate accepts one language profile per commit. If a future change materially spans multiple programming languages, stop and extend the evidence layout to one three-skill profile per affected language before reviewing it; do not silently choose a primary language.
