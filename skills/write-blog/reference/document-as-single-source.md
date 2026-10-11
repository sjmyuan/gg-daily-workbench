# Document-as-Single-Source Convention

The article document is the only state carrier in a blog-writing session. Every turn updates it in place via file edits and reports only what changed. HTML comments separate auxiliary content from the article body.

## Body vs. comments
- The article body holds only clean prose — no markers.
- All auxiliary content lives in HTML comment blocks that name their role.

## Marker blocks

| Marker | Block | Purpose | Update rule |
|---|---|---|---|
| 📌 Title & Summary | `<!-- 📌 Title & Summary -->` … `<!-- /Title & Summary -->` | Title and summary candidates | Always present after the first draft; refresh when core content changes; never drop |
| 📋 Materials | `<!-- 📋 Materials -->` … `<!-- /Materials -->` | Raw ideas and fragments not yet in the body | Append continuously; move into the body once integrated |
| ❓ Gaps | `<!-- ❓ Gaps -->` … `<!-- /Gaps -->` | Missing evidence, logic, structure, or reader answers | Add at the relevant location; remove once filled |
| 💡 Assistant Notes | `<!-- 💡 Assistant Notes -->` … `<!-- /Assistant Notes -->` | Writing advice and improvement directions | Keep until the article is final; refresh on every update |
| 🖼️ Illustration Suggestions | `<!-- 🖼️ Illustration Suggestions -->` … `<!-- /Illustration Suggestions -->` | Where and what to illustrate | Replace with a Markdown image once realized |

## Summary candidates
- 2–3 candidates, each ≤120 characters, stating the article's core value.
- Ready for social media or the article description field.

## Output rules
- Edit the article document file in place with file-editing tools (e.g., in an editor like VS Code); do not paste the full document into the chat.
- Report only the changes made this turn: what was added, moved, or replaced, and where.
- Output the full document only when the user explicitly asks for it, or when the document file is being created for the first time.
- The user may stop at any point and resume from the document file.
- Never drop the Title & Summary block in any turn.
- Close every turn with 2–3 concrete next directions or deepening questions; never end with a passive "is this OK?".

## Note timeliness and supersede discipline

The next session reads these notes as current truth, so a stale note is a defect, not clutter.

- **Append, don't rewrite history**: one dated round entry per turn ("本轮 review-draft（date）：…"). Keep the earlier entries; they show the reasoning trail and stop the next session from re-litigating settled points.
- **Supersede explicitly**: when a later conclusion replaces an earlier note, edit the old entry to say "已被本条覆盖" (superseded by …). Two conflicting notes are worse than one stale note — a live session hit this three times in a row (the compose-time "请作者确认文体", the resolved "约定出处没点名", and the "配图已写成建议块" note that outlived the images).
- **Mark realized items**: when a note describes something that has since happened (an illustration suggestion now generated, a gap now filled), mark it realized so the next session does not redo it.
- **Mark composed-but-unconfirmed content**: any first-person detail that was written rather than supplied by the author must be flagged as unconfirmed in the notes until the author replaces it — never let it age into apparent fact.
