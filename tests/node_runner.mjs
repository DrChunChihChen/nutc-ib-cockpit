// Run the actual Netlify handler offline. Only replace its JSON import for Node's loader.
import fs from "node:fs";
import { checkGrounding } from "../netlify/functions/lib/grounding.mjs";
import {
  schoolResponse,
  peerResponse,
  scopeResponse,
} from "../netlify/functions/lib/query-responses.mjs";
const root = new URL("../netlify/functions/", import.meta.url);
let src = fs.readFileSync(new URL("chat.js", root), "utf8");
src = src
  .replace(
    'import DOSSIERS from "./dossiers.json";',
    `const DOSSIERS = ${fs.readFileSync(new URL("dossiers.json", root), "utf8")};`,
  )
  .replaceAll(
    '"./lib/grounding.mjs"',
    JSON.stringify(new URL("lib/grounding.mjs", root).href),
  )
  .replaceAll(
    '"./lib/query-responses.mjs"',
    JSON.stringify(new URL("lib/query-responses.mjs", root).href),
  );
delete process.env.OPENROUTER_API_KEY;
globalThis.fetch = () => {
  throw new Error("Network forbidden in regression tests");
};
const handler = (
  await import(
    "data:text/javascript;base64," + Buffer.from(src).toString("base64")
  )
).default;
const input = JSON.parse(fs.readFileSync(0, "utf8")),
  results = [];
for (const item of input) {
  if (item.kind === "grounding")
    results.push(checkGrounding(item.answer, item.dossier, item.prompt));
  else if (item.kind === "scope")
    results.push(
      scopeResponse(item.message, item.intent, item.dossiers, item.slugs),
    );
  else if (item.kind === "peer")
    results.push(
      peerResponse(item.slug, item.school, item.dossiers, item.message),
    );
  else if (item.kind === "school")
    results.push(schoolResponse(item.school, item.dossiers, item.message));
  else {
    const r = await handler(
      new Request("http://localhost/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: item.message, ...item.context }),
      }),
    );
    if (r.status !== 200) throw new Error(await r.text());
    results.push(await r.json());
  }
}
console.log(JSON.stringify(results));
