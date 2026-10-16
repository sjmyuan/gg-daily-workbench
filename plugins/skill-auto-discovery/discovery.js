// Discovers the skills shipped by installed Claude plugins, so a plugin can
// register the cache/marketplace skills the native loader cannot reach.
import { readFile, readdir } from 'node:fs/promises';
import { basename, dirname, join, relative } from 'node:path';

const SKILL_FILE = 'skill.md';

export async function discoverInstalledSkills({ claudeDir }) {
  const roots = await skillRoots(claudeDir, await readInstallState(claudeDir));

  const byId = new Map();
  for (const root of roots) {
    for (const file of await collectSkillFiles(root)) {
      const id = deriveSkillId(relative(root, file));
      if (!id || byId.has(id)) continue;
      byId.set(id, await buildRecord(id, file));
    }
  }

  return [...byId.keys()].sort().map((id) => byId.get(id));
}

// A missing or unreadable install state is not an error: nothing is installed.
async function readInstallState(claudeDir) {
  try {
    return JSON.parse(await readFile(join(claudeDir, 'installed_plugins.json'), 'utf8'));
  } catch {
    return {};
  }
}

// Every route an installed plugin can ship skills from, in precedence order.
async function skillRoots(claudeDir, installed) {
  const roots = [];
  for (const [key, entry] of Object.entries(installed.plugins ?? {})) {
    for (const root of await pluginRoots(claudeDir, key, entry)) roots.push(root);
  }
  return roots;
}

async function pluginRoots(claudeDir, key, entry) {
  const [pluginName, marketplace] = key.split('@');
  const roots = [join(claudeDir, 'cache', pluginName)];
  for (const installPath of installPaths(entry)) roots.push(installPath);

  for (const declared of await manifestSkillPaths(claudeDir, marketplace, pluginName)) {
    roots.push(join(claudeDir, 'marketplaces', marketplace, declared));
  }
  return roots;
}

// The install state carries both shapes: v1 an object, v2 an array of entries.
function installPaths(entry) {
  if (Array.isArray(entry)) return entry.map((record) => record.installPath).filter(Boolean);
  return entry?.installPath ? [entry.installPath] : [];
}

async function manifestSkillPaths(claudeDir, marketplace, pluginName) {
  if (!marketplace) return [];
  const manifestFile = join(claudeDir, 'marketplaces', marketplace, '.claude-plugin', 'marketplace.json');
  let manifest;
  try {
    manifest = JSON.parse(await readFile(manifestFile, 'utf8'));
  } catch {
    return [];
  }
  const plugin = (manifest.plugins ?? []).find((candidate) => candidate.name === pluginName);
  return plugin?.skills ?? [];
}

async function collectSkillFiles(root) {
  const files = [];
  let entries;
  try {
    entries = await readdir(root, { withFileTypes: true });
  } catch {
    return files;
  }
  for (const entry of entries) {
    const entryPath = join(root, entry.name);
    if (entry.isDirectory()) files.push(...(await collectSkillFiles(entryPath)));
    else if (isSkillDocument(entry.name)) files.push(entryPath);
  }
  return files;
}

function isSkillDocument(name) {
  return /\.md$/i.test(name);
}

// Root-level Markdown keeps its own name; SKILL.md takes its containing directory.
function deriveSkillId(relPath) {
  const name = basename(relPath);
  if (name.toLowerCase() === SKILL_FILE) {
    const dir = dirname(relPath);
    return dir === '.' ? 'SKILL' : basename(dir);
  }
  return name.replace(/\.md$/i, '');
}

async function buildRecord(id, file) {
  const content = await readFile(file, 'utf8');
  const frontmatter = readFrontmatter(content);
  return {
    id,
    name: frontmatter.name ?? id,
    description: frontmatter.description ?? '',
    path: file,
    content,
  };
}

// Single-line `name:`/`description:` values only — enough for registration.
function readFrontmatter(content) {
  const match = /^---\r?\n([\s\S]*?)\r?\n---/.exec(content);
  if (!match) return {};

  const fields = {};
  for (const line of match[1].split(/\r?\n/)) {
    const pair = /^(name|description):\s*(.+)$/.exec(line.trim());
    if (pair) fields[pair[1]] = pair[2].trim();
  }
  return fields;
}
