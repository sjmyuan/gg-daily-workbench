---
name: correct-english
description: Correct English grammar, spelling, punctuation, and style while preserving meaning, tone, and format. Use when correcting, proofreading, polishing, rephrasing, or fixing English text.
---

<when-to-use-this-skill>
- The user submits English text with grammar, spelling, or punctuation errors
- The user asks to proofread informal text such as a chat message or social post
- The user wants a sentence made clearer or more concise
- The user asks to rephrase an ambiguous or unclear English sentence
- The user submits text with a misspelled proper noun
- The user wants text polished without changing its tone or formatting
</when-to-use-this-skill>

<knowledge>

<correction-scope>
| Category | Correct |
|---|---|
| Grammar | Subject-verb agreement, tense, articles, prepositions |
| Spelling | Misspelled words and misspelled proper nouns |
| Punctuation | Missing or incorrect punctuation; Oxford commas; quotation marks |
| Clarity | Reword only a genuine ambiguity |
| Conciseness | Remove redundancy only when meaning survives |
| Dialect and slang | Convert non-standard forms to standard English |
</correction-scope>

<preservation-constraints>
- Preserve meaning; never add or drop information.
- Preserve tone: formal, casual, or humorous.
- Preserve formatting: line breaks, bullet points, emphasis.
- Preserve the original language variety unless the user asks otherwise.
- Preserve the author's voice; change no more than the error requires.
</preservation-constraints>

<output-contract>
- Return only the corrected text.
- Add no commentary, notes, explanations, or preamble.
- Do not wrap the corrected text in quotation marks.
- Never explain the corrections unless the user asks.
</output-contract>

<correction-criteria>
See [correction-criteria.md](reference/correction-criteria.md) — the 8-point checklist for **verify-correction**.
</correction-criteria>

<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Correcting informal or non-standard text | Worked correction of a chat message | [examples/correct-informal-message.md](examples/correct-informal-message.md) |
| Verifying a draft that may change meaning | Worked verification that catches meaning drift | [examples/verify-correction.md](examples/verify-correction.md) |

</context-loading-guide>

</knowledge>

<capabilities>

<correct-english-text>
**Objective**: Return corrected English text with every error fixed and the meaning, tone, and format intact.

1. Read the input and identify its format (standard prose or non-standard) and its tone.
2. Fix grammar, spelling, and punctuation errors.
3. Convert misspelled proper nouns to their correct forms.
4. Reword a sentence only where clarity or conciseness clearly improves.
5. Preserve all formatting: line breaks, bullet points, emphasis.
6. Preserve the original meaning and tone.
7. Output the corrected text alone, per **output-contract**.
8. Verify the result with **verify-correction** before returning it.
</correct-english-text>

<verify-correction>
**Objective**: Confirm the corrected text passes every criterion before it is returned.

1. Load [reference/correction-criteria.md](reference/correction-criteria.md).
2. Apply each of the 8 criteria to the corrected text.
3. Revise the text for any failed criterion.
4. Re-run the checklist until every criterion passes.
5. Return the text only after all criteria pass.
</verify-correction>

</capabilities>

<rules>
<rule>When the user submits English text to correct, proofread, or polish → use **correct-english-text**.</rule>
<rule>When a corrected draft is ready → use **verify-correction**.</rule>
</rules>
