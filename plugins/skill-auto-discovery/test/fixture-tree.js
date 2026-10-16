// Hermetic fixture trees for the discovery suite. Every builder writes one
// claudeDir under the OS temp dir and registers it for removal after the suite.
import { mkdir, mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { dirname, join } from 'node:path';
import { after } from 'node:test';

const roots = [];

async function makeRoot() {
  const root = await mkdtemp(join(tmpdir(), 'skill-auto-discovery-unit.'));
  roots.push(root);
  return root;
}

async function write(file, content) {
  await mkdir(dirname(file), { recursive: true });
  await writeFile(file, content);
}

function frontmatter(fields) {
  const lines = Object.entries(fields).map(([key, value]) => `${key}: ${value}`);
  return `---\n${lines.join('\n')}\n---\n\n# skill body\n`;
}

after(async () => {
  await Promise.all(roots.map((root) => rm(root, { recursive: true, force: true })));
});

// A version-2 (array) install state, its cache v1 + cache v2 roots, and a
// marketplace manifest that also declares a plugin which is not installed.
export async function createPluginCacheTree() {
  const root = await makeRoot();

  await write(
    join(root, 'cache/plugin-alpha/skills/cache-installed/SKILL.md'),
    frontmatter({
      name: 'cache-installed',
      description: 'Skill from the version-1 Claude plugin cache.',
    }),
  );
  await write(join(root, 'cache/mkt-beta/beta/1.0.0/skills/beta-skill/SKILL.md'), '# no frontmatter\n');
  await write(
    join(root, 'cache/plugin-delta/skills/cache-uninstalled/SKILL.md'),
    frontmatter({ name: 'cache-uninstalled', description: 'Skill from an uninstalled plugin.' }),
  );
  // One id reachable through two install paths: the cache v1 dir and a v2 installPath.
  await write(
    join(root, 'cache/plugin-x/skills/draft-adr/SKILL.md'),
    frontmatter({ name: 'draft-adr', description: 'COLLISION-MARKER' }),
  );
  await write(
    join(root, 'cache/mkt-x/plugin-x/2.0.0/skills/draft-adr/SKILL.md'),
    frontmatter({ name: 'draft-adr', description: 'COLLISION-MARKER' }),
  );

  await write(
    join(root, 'marketplaces/mkt-gamma/.claude-plugin/marketplace.json'),
    JSON.stringify(
      {
        name: 'mkt-gamma',
        plugins: [
          { name: 'gamma', skills: ['./plugins/gamma/skills'] },
          { name: 'delta-mkt', skills: ['./plugins/delta-mkt/skills'] },
        ],
      },
      null,
      2,
    ),
  );
  await write(
    join(root, 'marketplaces/mkt-gamma/plugins/gamma/skills/mkt-installed/SKILL.md'),
    frontmatter({ name: 'mkt-installed', description: 'Skill declared by the Claude marketplace manifest.' }),
  );
  await write(
    join(root, 'marketplaces/mkt-gamma/plugins/delta-mkt/skills/mkt-uninstalled/SKILL.md'),
    frontmatter({ name: 'mkt-uninstalled', description: 'Skill of an uninstalled marketplace plugin.' }),
  );

  await write(
    join(root, 'installed_plugins.json'),
    JSON.stringify(
      {
        version: 2,
        plugins: {
          // The recorded installPath is deliberately stale so the cache route resolves it.
          'plugin-alpha@mkt-alpha': [
            { scope: 'user', installPath: join(root, 'cache/mkt-alpha/plugin-alpha/9.9.9'), version: '9.9.9' },
          ],
          'beta@mkt-beta': [
            { scope: 'user', installPath: join(root, 'cache/mkt-beta/beta/1.0.0'), version: '1.0.0' },
          ],
          'plugin-x@mkt-x': [
            { scope: 'user', installPath: join(root, 'cache/mkt-x/plugin-x/2.0.0'), version: '2.0.0' },
          ],
          'gamma@mkt-gamma': [
            { scope: 'user', installPath: join(root, 'cache/mkt-gamma/gamma/1.0.0'), version: '1.0.0' },
          ],
        },
      },
      null,
      2,
    ),
  );

  return root;
}

// A version-1 (object) install state. The id-rule fixtures ride the marketplace
// route, whose declared path is the walked root in both before and after F-2.
export async function createLegacyTree() {
  const root = await makeRoot();

  await write(
    join(root, 'legacy-install/skills/legacy-skill/SKILL.md'),
    frontmatter({ name: 'legacy-skill', description: 'Skill of a version-1 install record.' }),
  );
  await write(
    join(root, 'marketplaces/mkt-legacy/.claude-plugin/marketplace.json'),
    JSON.stringify({ name: 'mkt-legacy', plugins: [{ name: 'rules', skills: ['./plugins/rules/skills'] }] }, null, 2),
  );
  await write(
    join(root, 'marketplaces/mkt-legacy/plugins/rules/skills/SKILL.md'),
    frontmatter({ name: 'legacy-rules', description: 'Root-level SKILL.md.' }),
  );
  await write(
    join(root, 'marketplaces/mkt-legacy/plugins/rules/skills/teams/release/SKILL.md'),
    frontmatter({ name: 'release', description: 'Nested SKILL.md.' }),
  );
  await write(
    join(root, 'marketplaces/mkt-legacy/plugins/rules/skills/rules-notes.md'),
    frontmatter({ name: 'rules-notes', description: 'Root-level Markdown inside the subtree.' }),
  );

  await write(
    join(root, 'installed_plugins.json'),
    JSON.stringify(
      {
        version: 1,
        plugins: {
          'legacy@mkt-legacy': { installPath: join(root, 'legacy-install') },
          'rules@mkt-legacy': { installPath: join(root, 'legacy-missing') },
        },
      },
      null,
      2,
    ),
  );

  return root;
}

// A claudeDir with no install state at all.
export async function createEmptyTree() {
  return makeRoot();
}

// A claudeDir whose install state is unreadable JSON.
export async function createBrokenTree() {
  const root = await makeRoot();
  await write(join(root, 'installed_plugins.json'), '{ "plugins": [ truncated');
  return root;
}
