# embedded-ci-lab — Gemini CLI working rules

You are helping create the project `embedded-ci-lab` step by step.

## Project goal
Build a small Python-based CI pipeline runner that:
- reads pipeline definitions from YAML,
- validates their basic structure,
- executes steps sequentially,
- stops on failure,
- produces a JSON report.

This project must start simple and grow incrementally.
Do not jump to advanced architecture too early.

## Core workflow
- Work in small, sequential steps.
- Do only what is requested in the current step.
- Prefer the simplest working solution first, then improvements later.
- Do not add extra dependencies unless they are explicitly needed for the current task.
- Do not redesign the architecture unless it is necessary for the current step.
- Do not rewrite already working code without a clear reason.
- If you want to propose something more advanced, suggest it separately but do not implement it without confirmation.
- For implementation tasks, prefer: plan -> confirm -> implement.
- Keep changes minimal and easy to review.

## Scope control
If the current step is small, do not anticipate future steps.

Do not add:
- new features outside the request,
- speculative abstractions,
- premature optimizations,
- large refactors without approval,
- cloud integrations before the local MVP is stable,
- Yocto/BitBake/QEMU implementation before explicitly requested.

## End of every step
At the end of each step:
1. Run tests relevant to the current step.
2. Fix any failures.
3. Give a short report containing:
   - what changed,
   - which commands were run,
   - whether tests are green.

## Git workflow
- Keep `main` stable and releasable.
- Use a short-lived feature branch for each completed step or tightly scoped task.
- Prefer one branch per step, for example:
  - `feature/project-skeleton`
  - `feature/yaml-loader`
  - `feature/pipeline-validate`
  - `feature/sequential-runner`
  - `feature/json-report`
  - `feature/logging`
  - `feature/step-timeouts`
  - `feature/step-retries`
- Keep commits small, atomic, and focused on one logical change.
- Do not mix unrelated changes in one commit.
- Prefer Conventional Commits for commit messages.
- At the end of each completed step, if tests pass:
  1. review the diff,
  2. suggest a branch name,
  3. suggest one or more commit messages,
  4. suggest git commands to commit and push.
- Do not run `git commit`, `git push`, `git merge`, `git rebase`, or create/delete branches unless explicitly asked.
- If tests fail, do not suggest merging to `main`.

## Naming guidance
- Use lowercase names.
- Use hyphens in branch names.
- Keep branch names short and descriptive.
- Keep commit messages short and explicit.
- Prefer commit format:
  - `feat(scope): short description`
  - `fix(scope): short description`
  - `docs(scope): short description`
  - `test(scope): short description`
  - `refactor(scope): short description`
  - `ci(scope): short description`

## Current implementation order
Implement in this order unless explicitly changed:
1. Project skeleton
2. YAML loading
3. Validate command
4. Sequential execution
5. JSON reporting
6. Logging
7. Timeout support
8. Retry support
9. Cleanup refactor
10. GitHub Actions test workflow
11. Mock embedded pipeline example
12. Advanced features only after confirmation

## If you go out of scope
Stop. You went beyond the current step.

Roll back mentally to the last completed goal and complete only the current small step.

You must not:
- add new features,
- change architecture without need,
- rewrite already working code,
- add dependencies without a clear reason.

First, list what belongs to the current step and what does not.
Then make only the minimum necessary changes.
At the end, run tests and fix problems.

## Output style
When responding during implementation:
- be concise,
- show the exact files changed,
- show the commands run,
- summarize results clearly,
- avoid long explanations unless asked.