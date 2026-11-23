// The World in One Day — news-image-20261121 entry.
// The picture of the day is entry.png beside this file, drawn by draw.py
// (kept in the repository as the record of how it was made). The contest
// program's whole job is to place those exact bytes at /output/entry.png,
// identically on every run, so this copies the file and nothing else.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
