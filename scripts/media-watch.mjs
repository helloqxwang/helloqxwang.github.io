import path from 'node:path';
import { spawn } from 'node:child_process';

/** Rebuild only local photo assets when originals or YAML change during preview. */
export function mediaWatch() {
  return {
    name: 'local-photo-processing',
    apply: 'serve',
    configureServer(server) {
      const root = server.config.root;
      const folders = ['headshots', 'Photos', 'config'].map(folder => path.join(root, folder));
      server.watcher.add(folders);
      let timer, running = false, pending = false;
      function prepare() {
        if (running) { pending = true; return; }
        running = true;
        const child = spawn(process.execPath, ['scripts/prepare-media.mjs'], { cwd: root, stdio: 'inherit' });
        child.on('error', error => server.config.logger.error(error.message));
        child.on('close', code => {
          running = false;
          if (code !== 0) server.config.logger.error('Photo processing failed; see the message above.');
          if (pending) { pending = false; prepare(); }
        });
      }
      const onChange = (_event, file) => {
        if (!folders.some(folder => file.startsWith(folder + path.sep))) return;
        if (!/\.(ya?ml|jpe?g|png|webp|avif|heic|heif|mov|mp4)$/i.test(file)) return;
        clearTimeout(timer);
        timer = setTimeout(prepare, 800);
      };
      server.watcher.on('all', onChange);
      server.httpServer?.once('close', () => { clearTimeout(timer); server.watcher.off('all', onChange); });
    },
  };
}
