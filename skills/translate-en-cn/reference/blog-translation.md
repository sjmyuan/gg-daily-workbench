# Blog-Post Translation Conventions

Used by **translate-blog-post**. Detect the target blog's actual fields and keep its structure; do not invent fields the target does not use.

## Front matter

| Field | Handling |
|---|---|
| `title` | Translate to the target language |
| `excerpt` / `description` / `summary` | Translate; keep to one or two sentences |
| `tags` / `categories` | Translate each tag; use the target blog's canonical spelling and order |
| `slug` / `permalink` | Generate a target-language kebab-case slug from the translated title |
| `date`, `last_modified_at` | Copy verbatim |
| `layout`, `classes`, `toc` | Copy verbatim |
| Custom or unknown fields | Copy verbatim unless clearly human-readable text |

## Slug generation

- Build the slug from the translated title in kebab-case.
- Drop articles, prepositions, and punctuation when the result stays readable.
- Keep the slug unique; append a qualifier on collision.
- Match the target blog's URL style exactly (trailing slash, nesting).

## Body

| Element | Handling |
|---|---|
| Headings | Translate; use the target blog's case convention (English: sentence case) |
| Prose | Translate per the quality rubric |
| Lists | Translate items; keep markers and nesting |
| Code blocks | Copy verbatim; keep the language tag |
| Inline code, commands, identifiers | Copy verbatim |
| Images | Keep the URL; translate alt text and captions |
| Tables | Translate cell text; keep structure |
| Callouts and blockquotes | Keep markers; translate content |
| Math and symbols | Copy verbatim |

## Links

| Link type | Handling |
|---|---|
| External link | Keep the URL; translate the link text |
| Internal link to another source-blog post | Re-point to that post's equivalent in the target blog |
| Anchor link | Translate the fragment to match the translated heading |
| Image or asset link | Keep the URL verbatim |

## Target style

Match the target blog's visible conventions, not the source blog's:

- English posts use an English slug, an English title, and English tags.
- Headings are sentence case and descriptive.
- Prose reads as native English, not a close rendering of the Chinese.
- The excerpt summarizes the post in the target language.
