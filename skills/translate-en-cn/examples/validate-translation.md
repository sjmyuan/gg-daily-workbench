# Example: Validate a Draft Translation and Fix a Format Flaw

**Scenario**: The user submits an English sentence to translate and receives a draft that reads naturally but lost its inline code and bold markers.
The translation must pass the format-fidelity check before it is returned.

**Applies**: **detect-source-language**, **translate-text**, **validate-translation**

## Input to Translate

```markdown
Run `npm run build` and check the **build** output.
```

## Draft Translation (flawed)

```markdown
运行构建命令，并检查 构建 输出。
```

## Expected Behavior

**validate-translation** (per reference/translation-quality.md):

| # | Criterion | Result |
|---|---|---|
| 1 | Accuracy | Pass |
| 2 | Completeness | Pass |
| 3 | Naturalness | Pass |
| 4 | Cultural adaptation | Pass |
| 5 | Tone fidelity | Pass |
| 6 | Format fidelity | **Fail** — inline code translated, bold markers dropped |

Step 7 revises the draft for the failed criterion and re-runs the rubric.

## Expected Output

```markdown
运行 `npm run build`，并检查 **build** 的输出。
```
