# Translation Quality Rubric

Used by **validate-translation**. A translation is delivered only when all six criteria pass.

## Criteria

| # | Criterion | Pass | Fail |
|---|---|---|---|
| 1 | Accuracy | Every idea matches the source | Meaning added, dropped, or distorted |
| 2 | Completeness | Every source segment is translated | A sentence, list item, or caption is missing |
| 3 | Naturalness | Reads as if written in the target language | Translation-ese, source word order copied |
| 4 | Cultural adaptation | Idiom and references fit the target audience | Literal idiom that confuses the reader |
| 5 | Tone fidelity | Register matches the source | Formal source rendered casual, or the reverse |
| 6 | Format fidelity | Markers, links, code, and structure intact | Broken markdown, translated code, dead link text |

## Tone and register

| Source register | Target handling |
|---|---|
| Casual chat or social post | Keep contractions and short sentences |
| Technical article | Keep terms consistent; define an unfamiliar term once |
| Formal or academic | Keep formal syntax; avoid slang |
| Humor, irony, wordplay | Re-create the effect, not the literal words |

## Common pitfalls

| Pitfall | Fix |
|---|---|
| Translation-ese ("进行...的操作") | Use the verb directly |
| Literal idiom ("雨后春笋" → "bamboo shoots after rain") | Use the target equivalent ("spring up like mushrooms") |
| Over-translation of names | Keep the established English or Chinese form |
| Leftover untranslated source text | Translate every human-readable segment |
| Translated code or identifiers | Restore the original verbatim |
| Comment or explanation appended | Delete it; output the translation only |

## Outcome

| Result | Action |
|---|---|
| All six criteria pass | Deliver the translation |
| Any criterion fails | Revise and re-run the full rubric |
