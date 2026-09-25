import { defineConfig } from "astro/config";
import { mediaWatch } from "./scripts/media-watch.mjs";

export default defineConfig({
  site: "https://qianxu.wang",
  output: "static",
  vite: { plugins: [mediaWatch()] },
});
