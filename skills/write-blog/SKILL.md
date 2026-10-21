---
name: write-blog
description: Assist blog writing: gather ideas, fill gaps, and keep one document as the evolving draft with citations and illustrations. Use when writing, composing, reviewing, refining, referencing, or illustrating blog articles.
---

<when-to-use-this-skill>
- User wants existing content or scattered ideas shaped into a blog article
- User wants their material reviewed for gaps before writing
- User asks to compose a draft from collected material
- User shares links or sources to cite in the article
- User wants an existing draft reviewed and improved
- User wants language, style, or reader fit refined
- User wants illustrations generated for the article
</when-to-use-this-skill>

<knowledge>
<reference-index>

| Topic | Rule | Details |
|---|---|---|
| Audience | Technical readers want detail and logic, managers want rationale, impact, ROI and reusable methods, and both want evidenced claims. | — |
| Language | Match the user's language, defaulting to Chinese, and avoid translation-ese. | — |
| Markdown | Never write `**"term"**` — a quote inside a bold span breaks rendering. | — |
| Writing styles | Four styles (deep analysis, narrative, practical guide, opinion) plus article structure. Recommend one and confirm before composing. | [reference/writing-styles.md](reference/writing-styles.md) |
| Human voice | A written statement, not a chat: bans AI-flavor words, short-sentence runs, flourish, summary endings, chatty register. Gate before delivery. | [reference/human-voice.md](reference/human-voice.md) |
| Prose density | Too-terse prose reads as AI even with a clean blacklist. Deletion test, measured floors, deep-dive and verifiable-quantity budgets. | [reference/prose-density.md](reference/prose-density.md) |
| Style exemplars | Hand-written samples, markers, loose paragraphs. **A supplied sample outranks every heuristic**, with each deviation logged as an exemption. | [reference/style-exemplars.md](reference/style-exemplars.md) |
| Document state | The article document is the only state. Edit in place, report changes only. | [reference/document-as-single-source.md](reference/document-as-single-source.md) |
| Illustrations | Suggest 2–4 positions per article, and generate SVG on request. | [reference/illustration-standards.md](reference/illustration-standards.md) |

</reference-index>
<context-loading-guide>

| Load when | Provides | File |
|---|---|---|
| Marker blocks or update loop unclear | Document-as-single-source convention | [reference/document-as-single-source.md](reference/document-as-single-source.md) |
| Choosing a style or structuring | Four styles with structure and fit | [reference/writing-styles.md](reference/writing-styles.md) |
| Composing, reviewing, refining prose | Blacklist, rhythm, chatty-voice section, delivery gate | [reference/human-voice.md](reference/human-voice.md) |
| A draft reads terse or summary-like | Deletion test, density floors, expansion moves, colloquial ladder | [reference/prose-density.md](reference/prose-density.md) |
| Matching a personal voice, or a sample is shared | Exemplars, the author's samples, the exemption procedure | [reference/style-exemplars.md](reference/style-exemplars.md) |
| Suggesting or generating an illustration | Image types, placement, naming, SVG rules | [reference/illustration-standards.md](reference/illustration-standards.md) |
| User pastes content or shares scattered ideas | Walkthrough of ingest, collect, and gaps | [examples/ingest-and-collect.md](examples/ingest-and-collect.md) |
| User asks to draft, review, or refine an article | Walkthrough of compose, reference, review, refine | [examples/compose-and-review.md](examples/compose-and-review.md) |
| User asks to generate an illustration | Walkthrough of SVG generation and placement | [examples/generate-illustrations.md](examples/generate-illustrations.md) |

</context-loading-guide>
</knowledge>

<capabilities>
<ingest-existing-content>
**Objective**: Classify pasted content and place it in the document.
1. Classify each pasted part as formed paragraph, rough draft, scattered note, or mixed.
2. Summarize the classification and which parts are usable.
3. Extract style cues (word choice, rhythm, perspective) into an assistant note.
4. Place formed paragraphs in the body and an assistant note beside them, then move drafts and notes to the materials block.
5. Mark found gaps in the gaps block.
6. Verify each part is classified and placed.
7. Edit the document file, report only the changes, and ask 2–3 guiding questions.
</ingest-existing-content>
<collect-ideas>
**Objective**: Develop the user's ideas through listening and questions.
1. Listen, and let the user speak without interruption.
2. Restate the core in 1–2 sentences to confirm understanding.
3. Ask 1–2 deepening questions (triggering event, reader takeaway, real example).
4. Append the points to the materials block.
5. Verify the materials block captured the new points.
6. Edit the document file and report only the new points.
</collect-ideas>
<identify-gaps>
**Objective**: Find missing evidence, logic, structure, or reader answers.
1. Check the logic chain: clear thesis, enough evidence, no broken transitions.
2. List gaps by type: evidence, logic, structure, or reader perspective.
3. Ask a concrete question or offer a direction for each gap.
4. Mark each gap in the gaps block at its location.
5. Remove gap markers once filled and integrate the content.
6. Verify each listed gap is marked or filled.
7. Edit the document file and report only the gaps marked or filled.
</identify-gaps>
<compose-blog>
**Objective**: Turn material into a draft that reads like a person wrote it.
1. Read reference/style-exemplars.md and state 2–3 style rules from it before composing.
2. Ask for a hand-written post or a published article as the voice reference (standing samples: style-exemplars). If given, record its markers as "本文风格清单", which outranks the heuristics.
3. Recommend a writing style from reference/writing-styles.md and confirm with the user.
4. Compose on the user's sentences: keep their phrasing, connect and reorder, fill gaps. **Never invent first-person experience** — every detail traces to supplied material, a missing one is a gap.
5. Apply reference/human-voice.md: plain words, varied rhythm, first person, anchors, written-statement register.
6. Apply reference/prose-density.md: dictate each section before tightening, give each section a deep dive and a verifiable quantity, and measure against the §3 floors.
7. Compose title and summary candidates, intro, body, and conclusion per the style's structure. For a sequel, link the previous post in the intro.
8. Put title and summary candidates in the title-and-summary block.
9. Add an assistant note per section: intent, weakness, improvement.
10. Edit the document file, output title and summary candidates plus a section outline, and ask 3–4 feedback questions.
11. Verify title, summary, and per-section notes are present, and record the density numbers.
12. Revise per feedback and refresh title and summary on core change.
</compose-blog>
<track-references>
**Objective**: Embed shared sources as inline links.
1. Extract the URL and title from each shared source.
2. Link it inline at the relevant paragraph with Markdown link syntax.
3. For a link to another post on the author's own site, take the slug from the archive, never from the title or file name (local `ai-can-not-catch-up-my-brain.md` ↔ published `...-thoughts`).
4. Confirm placement with the user.
5. Mark verbally mentioned, unlinked sources as gaps.
6. Verify every link before delivery: one HTTP status request per URL, expect 200, report the results.
7. Verify every shared source is linked inline.
</track-references>
<suggest-images>
**Objective**: Mark 2–4 high-value illustration positions.
1. Scan the body for image-worthy spots: flows, comparisons, abstract concepts, real scenes.
2. Add an illustration-suggestion block after each spot with position, type, content, and purpose.
3. Keep 2–4 per article, prioritizing the highest-value spots.
4. Replace the block with a Markdown image once the user provides a real image.
5. Verify each block carries position, type, content, and purpose.
</suggest-images>
<review-draft>
**Objective**: Improve the existing draft with refreshed notes.
1. Append new user content to the materials block and integrate it into the body.
2. Scan the full text and find 2–3 concrete improvement spots (argument, transition, evidence, rhythm).
3. Add refreshed notes at those spots, never repeating prior ones.
4. Mark new gaps and update title and summary on substantive change.
5. Verify notes are refreshed, not repeated.
6. Edit the document file, report only the changes, and list 2–3 next directions.
</review-draft>
<refine-style>
**Objective**: Make the prose natural, strong, reader-adapted, AI-flavor-free.
1. If a hand-written sample exists, load its markers first: the sample governs and every deviation is recorded as an exemption.
2. Remove stiff transitions, repeated patterns, and translation-ese.
3. Strengthen each section's opening line and make sure it does not restate the heading verbatim, nor the summary opening restate its section.
4. Match depth to reader: detail for technical readers, meaning and value for managers.
5. Check the reader journey from pain point to insight.
6. Apply reference/human-voice.md: replace blacklisted words (recording swaps), break telegraph runs, remove flourish-only parallels and 总结腔, rewrite chatty phrasing as flat statements.
7. Refill what the deletions flattened: expand under-density sections with a prose-density §4 move, then apply the §5 deep-dive and verifiable-quantity budgets.
8. End with a conclusion, an action, or an open question — never a forced summary unless the author asked for one.
9. Run the Human-Voice Gate (reference/human-voice.md §8) over the body, report pass / fixed / gap per check with the density numbers, and deliver only when all pass or gaps are deferred.
10. Verify opening lines are strong and depth matches the reader.
</refine-style>
<generate-illustrations>
**Objective**: Produce an illustration file from a suggestion.
1. Locate the requested suggestion block and read its type and content.
2. Extract key terms, steps, and relationships from the article context.
3. Generate SVG by default (PlantUML only on request) per reference/illustration-standards.md.
4. Save to the article's assets folder with the naming rule from reference/illustration-standards.md.
5. Replace the suggestion block with a Markdown image link and optional caption.
6. Verify the image matches the suggestion and the file is placed per the standards.
7. Regenerate and overwrite the file when the user requests changes.
</generate-illustrations>
</capabilities>

<rules>
<rule>Pasted existing content → **ingest-existing-content**.</rule>
<rule>New ideas or thoughts → **collect-ideas**.</rule>
<rule>Abundant material, or the user asks what is missing → **identify-gaps**.</rule>
<rule>Draft requested or material suffices → **compose-blog**.</rule>
<rule>Links or sources shared → **track-references**.</rule>
<rule>Draft exists and the user adds material or asks for review → **review-draft**.</rule>
<rule>Prose polish requested → **refine-style**.</rule>
<rule>An actual illustration requested → **generate-illustrations**.</rule>
<rule>Composing or reviewing a draft → also **suggest-images**.</rule>
<rule>Any prose work → human-voice rules plus the Gate, passed before delivery.</rule>
<rule>A draft reads terse or summary-like → **prose-density**: §3 floors and §5 budgets, where a shortfall is a gap, never padding.</rule>
<rule>A user-supplied sample is the style reference → record its markers, let it outrank the heuristics, log every exemption.</rule>
<rule>A sequel continues an earlier post → link it in the intro and closing, citing what it established rather than re-arguing.</rule>
</rules>
