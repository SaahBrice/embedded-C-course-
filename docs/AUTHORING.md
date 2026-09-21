# Authoring Levels and Sublevels

The curriculum is data-driven. `curriculum/levels.toml` defines the ordered levels; each coding sublevel is a self-contained package discovered through its `level.toml`. New packages can be inserted without changing command dispatch code.

## Level definition

Each `[[levels]]` table contains:

```toml
[[levels]]
id = "stable-level-id"
title = "Readable Level Title"
order = 1
objective = "One coherent main objective."
learning_outcomes = ["Concrete outcome one", "Concrete outcome two"]
overview = "01-directory/LEVEL.md"
sublevels = ["first-problem", "second-problem", "third-problem", "fourth-problem", "final-release"]
final_battle = "final-release"
final_integrates = ["first-problem", "second-problem", "third-problem"]
topic_practice = [
  { topic = "strict diagnostics", sublevels = ["first-problem", "second-problem", "third-problem", "fourth-problem", "final-release"] },
]
```

A level must contain at least five genuinely distinct coding sublevels in the built-in course. The final battle occurs exactly once, must be the last ID, and `final_integrates` names at least three earlier sublevels whose skills its contract combines. Each `topic_practice` entry names a real skill cluster and at least five different coding sublevels that practise it; the union of those clusters must cover the whole level. Curate those lists from the work performed—do not generate neighboring windows merely to reach five. Every sublevel belongs to exactly one level, and the global order in `levels.toml` must match package order. `LEVEL.md` explains the main objective, prerequisites, why the concepts belong together, expected outcomes, ordered sublevels, practice clusters, and final battle.

Do not create several sublevels by pointing different names at the same starter, contract, and tests. The authoring validator detects that duplication.

## Sublevel package

```text
NNN-stable-id/
  level.toml
  briefing.md
  lesson.md
  debrief.md
  solution.md
  hints/01.md 02.md 03.md
  starter/
  reference/
  checks/              # trusted harnesses
```

The stable `id` uses lowercase letters, digits, and hyphens. `order` controls sequence. Increment `version` when the learner contract or acceptance criteria changes. `stage` identifies the containing level. The first sublevel has no prerequisite; each later package depends on the immediately preceding sublevel ID, which enforces progressive unlocking.

Every package declares a 45–60 minute target where appropriate, at least two objectives, hints, content paths, starter and reference paths, and one or more checks. Paths are relative and may not contain `..`. The built-in course never requires a reflection or essay check.

The briefing must be usable without terminal context and contain exactly five second-level headings: `Your task`, `Why firmware engineers care`, `Read the function signature`, `Concrete examples`, and `Expected failure behavior`. Merge the starter's specific defect into the firmware-relevance section. Put the editable files, run command, test command, and success condition inside `Your task`. Keep each fact in one place. A copy named `BRIEFING.md` is automatically placed in every attempt.

## Supported checks

- `c_harness` compiles learner sources against a trusted sublevel harness. A matching `checks/visible.c` should provide transparent examples for `./learn run`.
- `c_program` compiles a complete program and checks exact stdout and exit status.
- `c_test_pair` proves learner-written tests accept a good module and reject a defective module.
- `project_harness` runs trusted multi-file build, install, relocation, or integration checks in temporary directories.
- `manual_evidence` verifies non-empty fields in an explicitly self-attested hardware record.
- `file_exists`, `text_regex`, `markdown_response`, and direct `command` checks remain available for external curricula, although the built-in campaign uses executable coding checks instead of prose quotas.

Keep declarations in learner-owned public headers and expected results in `checks/`. Never place credentials, network access, automatic flashing, destructive commands, or learner-editable expected values in a check.

## Reference and validation

`reference/` must be a complete working answer with the same shape as the starter. `solution.md` explains why it works and may show the important code. The validator copies each reference into a temporary attempt and runs its checks.

To insert a sublevel, choose a permanent ID and order between its neighbors. Make it depend on the former predecessor, update the successor's prerequisite, and add the ID at the matching position in `levels.toml`. To add a level, add its packages, `LEVEL.md`, and one new level table. Existing completion IDs remain valid.

Before shipping, run:

```bash
./learn validate --all-solutions
./scripts/test_all.sh
```

The generated built-in curriculum is reproduced by `tools/build_curriculum.py` followed by `tools/enhance_curriculum.py`; both support a separate output root for reproducibility tests.
