import assert from 'node:assert/strict';
import { join } from 'node:path';
import test from 'node:test';

import { discoverInstalledSkills } from '../discovery.js';
import {
  createBrokenTree,
  createEmptyTree,
  createLegacyTree,
  createPluginCacheTree,
} from './fixture-tree.js';

const INSTALLED_IDS = ['alpha-release', 'beta-skill', 'cache-installed', 'draft-adr', 'mkt-installed'];
const UNLISTED_IDS = [...INSTALLED_IDS, 'cache-uninstalled', 'mkt-uninstalled'];
const LEGACY_IDS = ['SKILL', 'legacy-skill', 'release', 'rules-notes'];

const cacheTree = await createPluginCacheTree();
const legacyTree = await createLegacyTree();

async function discoveredIds(claudeDir) {
  const records = await discoverInstalledSkills({ claudeDir });
  return records.map((record) => record.id);
}

test('the version-2 array install shape reaches every recorded install path', async () => {
  const ids = await discoveredIds(cacheTree);

  assert.deepEqual(ids, INSTALLED_IDS);
});

test('the version-1 object install shape is read too', async () => {
  const ids = await discoveredIds(legacyTree);

  assert.deepEqual(ids, LEGACY_IDS);
});

test('the marketplace manifest route yields its declared skill', async () => {
  const records = await discoverInstalledSkills({ claudeDir: cacheTree });
  const record = records.find((entry) => entry.id === 'mkt-installed');

  assert.ok(record, 'mkt-installed was not discovered');
  assert.ok(record.path.includes(join('marketplaces', 'mkt-gamma')));
});

test('an unlisted cache plugin is excluded while a listed one is present', async () => {
  const ids = await discoveredIds(cacheTree);

  assert.deepEqual(ids, INSTALLED_IDS);
  assert.deepEqual(
    ids.filter((id) => UNLISTED_IDS.includes(id) && !INSTALLED_IDS.includes(id)),
    [],
  );
});

test('a marketplace plugin absent from the install state is excluded', async () => {
  const ids = await discoveredIds(cacheTree);

  assert.deepEqual(ids, INSTALLED_IDS);
  assert.equal(ids.includes('mkt-uninstalled'), false);
});

test('one id reached through two install paths is yielded once, in order', async () => {
  const ids = await discoveredIds(cacheTree);

  assert.deepEqual(ids, INSTALLED_IDS);
  assert.equal(ids.filter((id) => id === 'draft-adr').length, 1);
});

test('a missing or malformed install state yields no skills and no throw', async () => {
  const empty = await createEmptyTree();
  const broken = await createBrokenTree();

  assert.deepEqual(await discoveredIds(empty), []);
  assert.deepEqual(await discoveredIds(broken), []);
});

test('skill ids follow the path rules', async () => {
  const ids = new Set(await discoveredIds(legacyTree));

  assert.ok(ids.has('legacy-skill'), '<dir>/<name>/SKILL.md -> <name>');
  assert.ok(ids.has('release'), 'teams/release/SKILL.md -> release');
  assert.ok(ids.has('rules-notes'), 'root rules-notes.md -> rules-notes');
  assert.ok(ids.has('SKILL'), 'root SKILL.md -> SKILL');
});

test('records carry the registration shape with frontmatter fallbacks', async () => {
  const records = await discoverInstalledSkills({ claudeDir: cacheTree });
  const byId = new Map(records.map((record) => [record.id, record]));
  const fronted = byId.get('cache-installed');
  const bare = byId.get('beta-skill');

  assert.ok(fronted, 'cache-installed record is missing');
  assert.ok(bare, 'beta-skill record is missing');
  assert.deepEqual(Object.keys(fronted).sort(), ['content', 'description', 'id', 'name', 'path']);
  assert.equal(fronted.name, 'cache-installed');
  assert.equal(fronted.description, 'Skill from the version-1 Claude plugin cache.');
  assert.ok(fronted.path.endsWith(join('cache-installed', 'SKILL.md')));
  assert.ok(fronted.content.includes('cache-installed'));
  assert.equal(bare.name, 'beta-skill');
  assert.equal(bare.description, '');
});

test('Markdown outside a plugin skills subtree is not admitted', async () => {
  const ids = await discoveredIds(cacheTree);

  assert.deepEqual(ids, INSTALLED_IDS);
  assert.deepEqual(
    ids.filter((id) => ['README', 'agent-notes', 'CHANGELOG'].includes(id)),
    [],
  );
});
