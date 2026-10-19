// Wraps the artifact-style index.html fragment in a full HTML document for static hosting.
import { cpSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";

const src = readFileSync("index.html", "utf8");
const split = src.indexOf("<style>");
const head = src.slice(0, split);
const body = src.slice(split);

const html = `<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
${head.trim()}
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
${body.trim()}
</body>
</html>
`;

rmSync("dist", { recursive: true, force: true });
mkdirSync("dist");
writeFileSync("dist/index.html", html);
cpSync("data", "dist/data", { recursive: true });
