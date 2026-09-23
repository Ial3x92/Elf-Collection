---
name: fix-tests
description: Run checks and fix failing tests before push.
context: fork
---

# Fix Tests

Use this skill when the goal is to get the branch ready to push by repeatedly running checks and fixing failures.

1. Inspect what changed.
   - Run `git status --short`.
   - Review current diffs with `git diff --stat` and `git diff`.

2. Run the full local validation flow.
   - Run pre-commit checks with `uv run --frozen pre-commit run --all-files`.
   - Run `./run-tests.sh`.

3. Loop until clean.
   - Group related failures by root cause.
   - Apply minimal readable fixes that keep behavior stable unless tests show the behavior is incorrect.
   - Add or update focused tests for each bug fix.
   - Re-run pre-commit and the test script after each fix batch.

4. Final readiness check.
   - Confirm both commands pass with no failures.
   - Summarize what was fixed and list any remaining risks or follow-ups before push.

