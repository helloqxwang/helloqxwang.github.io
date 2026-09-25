import { existsSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../', import.meta.url));
const python = process.env.MEDIA_PYTHON || `${root}.media-venv/${process.platform === 'win32' ? 'Scripts/python.exe' : 'bin/python'}`;
if (!existsSync(python)) {
  console.error('Set up photo processing once: npm run media:setup (Python 3.9–3.12 required).');
  process.exit(1);
}
const result = spawnSync(python, ['scripts/prepare-media.py'], { cwd: root, stdio: 'inherit' });
if (result.error) console.error(result.error.message);
process.exit(result.status ?? 1);
