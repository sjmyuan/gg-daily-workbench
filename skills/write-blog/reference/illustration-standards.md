# Illustration Standards

## Suggestion types
Scan the body for four high-value image spots:

| Spot | Type | Example |
|---|---|---|
| Process or steps | Flowchart / diagram | Multi-step operation, architecture, decision flow |
| Comparison or data | Chart | Number comparison, trend, effect difference |
| Abstract concept | Concept diagram | A mental model hard to convey in text |
| Real scene | Screenshot / photo | Tool UI, code output, physical reference |

## Suggestion block content
Each illustration-suggestion block states: position (right after which paragraph), image type, content description (key elements), and purpose (what the reader understands and how much text it saves).

- 2–4 suggestions per article; favor the highest-value spots.

## Generation rules
- Default format: SVG for all illustration types (flowchart, architecture, sequence, concept, chart).
- PlantUML only when the user explicitly requests it.
- Match the article's language and overall tone in the image text.
- Generate from the article context: extract key terms, steps, and relationships so the image matches the prose.

## File placement
- Save in the assets folder next to the article file.
- Name files `article-name-illustration-name.svg`.
- Choose the illustration name as an English or pinyin keyword from the content.
- Replace the suggestion block with `![description](assets/filename.svg)` and an optional caption line `*caption*`.

## Post-generation check

Text inside a diagram goes stale as soon as the body is revised, and it never shows up in a prose diff. After generating or regenerating any illustration:

1. **Title treatment consistent**: if the article's diagrams carry a main heading, every one of them does. A single diagram missing its heading is the tell (hit once in practice).
2. **Wording matches the current body**: re-grep each SVG's text against the body for terms the body has since dropped — a diagram kept the word "返工" after the article had stopped using it.
3. **Checks re-run after every regeneration**: XML parses, no element overlaps, no text overflows its container, smallest font ≥14px.
4. **Placement confirmed**: file lives in the article's `assets/` folder as `<article-name>-<illustration-name>.svg`, referenced from the article as `../assets/<file>.svg`, with the suggestion block replaced by `![desc](../assets/<file>.svg)` plus an optional caption line.

## Optimization
- On user change requests, re-scan the article context, regenerate, and overwrite the original file (keep the filename).
