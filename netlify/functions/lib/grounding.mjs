// Numeric provenance only. Shared regression cases cover Python parity.
const numericPattern = () =>
  /(?<![A-Za-z0-9_.])(-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+(?:\.\d+)?)(?!\d|\.\d|[A-Za-z_])/g;
function cleanText(text) {
  return text
    .replace(/^\s*\d+[.)、]\s+/gm, "")
    .replace(/(?:UDB\s*)?[學教]\d+(?:-\d+)?/g, "")
    .replace(/(?<=\d)pp\b/g, " 個百分點");
}
function collectNumbers(obj, out) {
  if (obj == null || typeof obj === "boolean") return;
  if (typeof obj === "number" && Number.isFinite(obj)) out.add(obj);
  else if (typeof obj === "string") {
    for (const m of cleanText(obj).matchAll(numericPattern()))
      out.add(Number(m[1].replaceAll(",", "")));
  } else if (typeof obj === "object") {
    for (const value of Object.values(obj)) collectNumbers(value, out);
  }
}
export function checkGrounding(answer, dossier, prompt) {
  const allowed = new Set();
  collectNumbers(dossier, allowed);
  const ungrounded = [];
  let checked = 0;
  for (const m of cleanText(answer).matchAll(numericPattern())) {
    const raw = m[1],
      value = Number(raw.replaceAll(",", "")),
      precision = raw.includes(".") ? raw.split(".")[1].length : 0;
    const scale = 10 ** Math.min(precision, 8);
    checked++;
    if (
      ![...allowed].some(
        (a) =>
          Math.abs(Math.floor(a * scale + 0.5 + 1e-8) / scale - value) < 1e-8,
      )
    )
      ungrounded.push(raw);
  }
  return {
    ok: ungrounded.length === 0,
    checked,
    ungrounded,
    method: "numeric_only",
    note: "僅驗證數值是否存在於來源；不代表指標、系所、學年或語意已核實。",
  };
}
