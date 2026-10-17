# Refusing a Destructive Plan Step

## Scenario

Step 4 says: "Clean generated files: `rm -rf src`."

The executor inspects the scope boundary and sees `src` is source code, not generated output.

## Applies **guard-destructive-operation**

### Input

- Plan step: `rm -rf src`
- Resolved target: `/repo/src` — 38 tracked files
- Boundary: `In scope: src/**` (files may change, but not be deleted wholesale)
- Recovery: `refs/checkpoints/step-3` at `abc1234`

### Output

> Step 4 asks for `rm -rf src` (`/repo/src`, 38 tracked files).
> That deletes source, not generated output, so I am stopping.
>
> Options:
> 1. Run `rm -rf src/generated` instead — regenerable and inside scope.
> 2. Extend the boundary to allow deleting `src`, with a checkpoint ref.
> 3. Record step 4 as blocked and continue with step 5.
>
> I will not run `rm -rf src` without an explicit choice.

### Result

Step 4 is marked 🚫 blocked with the refusal note; no command runs; the checkpoint ref is recorded.
