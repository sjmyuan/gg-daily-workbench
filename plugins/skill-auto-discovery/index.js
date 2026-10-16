// Registers the skills shipped by installed Claude plugins, which the native
// loader does not reach. The skip set is the ctx.skill.list() snapshot read at
// setup, outside the synchronous transform callback.
import { homedir } from 'node:os';
import { join } from 'node:path';

import { discoverInstalledSkills } from './discovery.js';

export function createRegistration(native, candidates) {
  return (editor) => {
    for (const candidate of candidates) {
      if (native.has(candidate.id) || editor.get(candidate.id)) continue;
      editor.add(candidate);
    }
  };
}

export default {
  id: 'skill-auto-discovery',
  async setup(ctx) {
    const native = new Set((await ctx.skill.list()).data.map((skill) => skill.id));
    const candidates = await discoverInstalledSkills({
      claudeDir: join(homedir(), '.claude', 'plugins'),
    });

    await ctx.skill.transform(createRegistration(native, candidates));

    console.log(`skill-auto-discovery loaded ${candidates.length} installed plugin skills`);
    return () => {};
  },
};
