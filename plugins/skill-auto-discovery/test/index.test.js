import assert from 'node:assert/strict';
import test from 'node:test';

import { createRegistration } from '../index.js';

function skill(id) {
  return { id, name: id, description: '', path: `/tmp/${id}/SKILL.md`, content: '' };
}

test('the native snapshot alone decides the skip; an editor hit never suppresses a registration', () => {
  const native = new Set(['opencode', 'report', 'draft-adr']);
  const added = [];
  const editor = {
    add: (record) => added.push(record.id),
    // An editor reporting every candidate as present — the construct the probe
    // measured as harmful: a silent drop of the plugin's own contribution.
    get: () => ({ id: 'present-in-editor', name: 'present-in-editor', description: '', path: '/x', content: '' }),
  };

  createRegistration(native, [skill('draft-adr'), skill('cache-installed')])(editor);

  assert.deepEqual(added, ['cache-installed']);
});
