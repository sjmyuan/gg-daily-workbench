#!/usr/bin/env node
// Validate every fenced ```mermaid block in Markdown files.
//
//   node scripts/validate_mermaid.mjs <file-or-dir> [...]
//
// Full parsing (recommended, once): npm i --prefix scripts mermaid jsdom
// Without those deps, built-in heuristic checks still run.
// Exit code: 0 when all blocks parse, 1 when any fail.
import { readFileSync, readdirSync, statSync, existsSync } from 'node:fs';
import { join, extname } from 'node:path';

const targets = process.argv.slice(2);
if (targets.length === 0) {
  console.error('usage: node validate_mermaid.mjs <file-or-dir> [...]');
  process.exit(2);
}

function walk(p, acc = []) {
  const s = statSync(p);
  if (s.isDirectory()) {
    for (const e of readdirSync(p)) walk(join(p, e), acc);
  } else if (extname(p) === '.md') {
    acc.push(p);
  }
  return acc;
}

function blocks(md) {
  const lines = md.split('\n');
  const out = [];
  let inBlock = false, start = 0, buf = [];
  lines.forEach((l, i) => {
    if (!inBlock && /^\s*```mermaid\s*$/.test(l)) { inBlock = true; start = i + 2; buf = []; return; }
    if (inBlock && /^\s*```\s*$/.test(l)) { out.push({ start, text: buf.join('\n') }); inBlock = false; return; }
    if (inBlock) buf.push(l);
  });
  if (inBlock) out.push({ start, text: buf.join('\n'), unterminated: true });
  return out;
}

// Dependency-free checks for the known breakers.
function heuristics(text) {
  const errs = [];
  const lines = text.split('\n');
  const isSequence = /^\s*sequenceDiagram\b/.test(lines[0] || '');
  const isFlow = /^\s*(flowchart|graph)\b/.test(lines[0] || '');
  lines.forEach((l, i) => {
    const ln = i + 1;
    const t = l.trim();
    const kw = t.match(/^(database|boundary|control|entity|collections|queue)\s+\S/);
    if (kw) errs.push(`L${ln}: "${kw[1]}" is not a lifeline keyword — use "participant"`);
    if (isSequence && /(->>|-->>|-\)|--\)|-->|->)\s*[^:]*:.*;/.test(l))
      errs.push(`L${ln}: ";" in sequence message text is a statement separator — reword to ","`);
    if (isSequence && /^\s*Note\b[^:]*:.*;/.test(l))
      errs.push(`L${ln}: ";" in a sequence Note is a statement separator — reword to ","`);
    if (isFlow && /\[[^\]"]*\|[^\]]*\]/.test(l))
      errs.push(`L${ln}: unquoted "|" in a flowchart label — quote the label or reword`);
  });
  return errs;
}

let mermaid = null;
try {
  const { JSDOM } = await import('jsdom');
  const dom = new JSDOM('<!DOCTYPE html><html><body></body></html>', { pretendToBeVisual: true });
  globalThis.window = dom.window;
  globalThis.document = dom.window.document;
  Object.defineProperty(globalThis, 'navigator', { value: dom.window.navigator, configurable: true });
  globalThis.SVGElement = dom.window.SVGElement;
  globalThis.Element = dom.window.Element;
  globalThis.Node = dom.window.Node;
  globalThis.HTMLElement = dom.window.HTMLElement;
  globalThis.DOMParser = dom.window.DOMParser;
  mermaid = (await import('mermaid')).default;
  mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });
} catch {
  mermaid = null;
}

const files = targets.flatMap((t) => (existsSync(t) ? walk(t) : []));
let total = 0, failed = 0;
for (const f of files) {
  for (const b of blocks(readFileSync(f, 'utf8'))) {
    total++;
    const errs = heuristics(b.text);
    if (b.unterminated) errs.push('unterminated mermaid fence');
    if (mermaid) {
      try {
        await mermaid.parse(b.text);
      } catch (e) {
        errs.push(String(e.message).split('\n').slice(0, 2).join(' ').slice(0, 180));
      }
    }
    if (errs.length) {
      failed++;
      console.log(`\nFAIL ${f}:L${b.start}`);
      for (const e of errs) console.log(`  - ${e}`);
    }
  }
}
console.log(
  `\n${total} mermaid block(s), ${failed} failed` +
    (mermaid ? '' : ' — heuristic checks only; install mermaid + jsdom for full parsing')
);
process.exit(failed ? 1 : 0);
