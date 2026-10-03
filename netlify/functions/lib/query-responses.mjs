// Deterministic source-scoped responses; parity-tested against query_responses.py.
export const SLUG_NAMES = {
  ib: "國際貿易與經營系",
  ba: "企業管理系",
  accounting: "會計資訊系",
  finance: "財務金融系",
  insurance: "保險金融管理系",
  stat: "應用統計系",
  tax: "財政稅務系",
};
const slugsAll = Object.keys(SLUG_NAMES);
const number = (v) => (v == null ? "—" : String(v));
const normalize = (s) =>
  (s || "").replaceAll("台", "臺").replace(/^國立/, "").trim();
const sameSchool = (a, b) => normalize(a) === normalize(b);
function sameDept(dept, school, target) {
  let v = normalize(dept),
    prefix = normalize(school);
  if (v.startsWith(prefix)) v = v.slice(prefix.length);
  return v === normalize(target);
}
export function selectedSlugs(message, aliases) {
  let remaining = message;
  const selected = new Set();
  for (const [alias, slug] of Object.entries(aliases).sort(
    (a, b) => b[0].length - a[0].length,
  )) {
    if (remaining.includes(alias)) {
      selected.add(slug);
      remaining = remaining.replaceAll(alias, "");
    }
  }
  if (/全院|商學院|全校|各系|哪(?:一)?個系|哪些系/.test(message))
    return slugsAll;
  return slugsAll.filter((s) => selected.has(s));
}
export function requestedYear(message) {
  const m = message.match(/(?<!\d)(1\d{2})\s*(?:學年度|學年|年度|年)/);
  return m ? Number(m[1]) : null;
}
export function flow(d, school, dept = null, year = null) {
  const m = d.module5 || {},
    years = year != null ? [String(year)] : (m.years || []).map(String);
  let available =
    Array.isArray(m.destinations) &&
    years.length > 0 &&
    years.every((y) => (m.years || []).map(String).includes(y));
  const rows = (m.destinations || []).filter(
    (r) => sameSchool(r.school, school) && years.includes(String(r.year)),
  );
  if (dept != null && rows.some((r) => !r.dept || r.dept === "—"))
    available = false;
  const count = available
    ? rows
        .filter((r) => dept == null || sameDept(r.dept, r.school, dept))
        .reduce((a, r) => a + r.count, 0)
    : null;
  return { count, years, unit: "records", source: m.source ?? null };
}
const period = (years) =>
  years.length ? years.join("、") + " 學年" : "期間未知";
function response(intent, text, table, facts, slugs, dataTime) {
  const allScope = slugs.length > 1,
    complete = facts.complete ?? true;
  return {
    intent,
    dept: {
      slug: allScope ? "all" : slugs[0],
      name:
        slugs.length === slugsAll.length
          ? "商學院全院"
          : allScope
            ? "跨系比較"
            : SLUG_NAMES[slugs[0]],
      school: "國立臺中科技大學",
    },
    response: text,
    table,
    chart: null,
    facts,
    model: "rule-based-ir-engine",
    reasoning: "按查詢範圍與資料期間直接計算。",
    grounding: {
      ok: complete ? true : null,
      method: "structured_sources",
      checked: table.rows.length,
      ungrounded: [],
      note: "數值由來源欄位計算；缺少資料時不宣稱完整。",
    },
    source: "UDB 系所指標／交叉查榜／出生數推估（各列標示期間）",
    drilldown_link: allScope ? "heatmap.html" : `${slugs[0]}/index.html`,
    data_time: dataTime,
  };
}
export function schoolResponse(school, dossiers, message) {
  const year = requestedYear(message),
    rows = [],
    flows = {},
    years = new Set();
  for (const slug of slugsAll) {
    const d = dossiers[slug] || {},
      f = flow(d, school, null, year);
    flows[slug] = f;
    for (const p of d.peers || []) {
      if (!sameSchool(p.school, school)) continue;
      const py = p.year,
        visible = year == null || String(py) === String(year);
      years.add(py == null ? "未知" : String(py));
      rows.push([
        SLUG_NAMES[slug],
        p.dept,
        visible ? `${py} 學年` : `缺 ${year} 學年（收錄 ${py}）`,
        visible ? number(p.enrollment_rate) + "%" : "—",
        visible ? number(p.dropout_rate) + "%" : "—",
        visible ? number(p.faculty_ratio) : "—",
        visible ? number(p.students_total) : "—",
        number(f.count),
        period(f.years),
      ]);
    }
  }
  const available = Object.values(flows)
      .map((f) => f.count)
      .filter((v) => v != null),
    complete = available.length === slugsAll.length;
  const total = complete ? available.reduce((a, b) => a + b, 0) : null,
    flowYears = [
      ...new Set(Object.values(flows).flatMap((f) => f.years)),
    ].sort();
  let text = `${school}：本院資料庫收錄 ${rows.length} 組系所對接；指標學年逐列標示。\n\n`;
  text += complete
    ? `交叉查榜（${period(flowYears)}）向該校外流共 **${total} 筆**。`
    : "交叉查榜資料不完整，無法提供全院外流總數。";
  text +=
    "跨系紀錄未去重，不代表不重複人數；表內外流為流向該校所有系所的紀錄。\n\n請問您詢問的是上述哪一個特定系所？還是系統中該校所有的系所？";
  return response(
    "school_intelligence",
    text,
    {
      title: `${school} 對接清冊`,
      headers: [
        "本院系所",
        "同儕系所",
        "指標學年",
        "註冊率",
        "退學率",
        "生師比",
        "在學人數",
        "流向整校紀錄（筆）",
        "查榜期間",
      ],
      rows,
    },
    { complete, school, flow_records: total, flows, years: flowYears },
    slugsAll,
    `指標：${period([...years].sort())}；查榜：${period(flowYears)}`,
  );
}
export function peerResponse(slug, school, dossiers, message) {
  const d = dossiers[slug],
    p = (d.peers || []).find((p) => sameSchool(p.school, school));
  if (!p) return null;
  const year = requestedYear(message),
    ownYear = d.meta.latest_year,
    peerYear = p.year,
    f = flow(d, school, p.dept, year),
    rows = [];
  const metrics = [
    ["新生註冊率", "K01", "enrollment_rate", "%", "UDB 學12-1"],
    ["學年度退學率", "K02", "dropout_rate", "%", "UDB 學13-1"],
    ["專任生師比", "K06", "faculty_ratio", "", "UDB 教1-1"],
  ];
  for (const [label, key, field, unit, source] of metrics) {
    const own =
        year == null || String(ownYear) === String(year)
          ? d.kpis?.[key]?.value
          : null,
      other =
        year == null || String(peerYear) === String(year) ? p[field] : null;
    const comparable =
      own != null &&
      other != null &&
      ownYear != null &&
      String(ownYear) === String(peerYear);
    const diff = comparable
      ? number(Number((own - other).toFixed(2))) +
        (unit === "%" ? " 個百分點" : "")
      : "學年不同或資料不足，不計差距";
    rows.push([label, number(own) + unit, number(other) + unit, diff, source]);
  }
  rows.push([
    "流向該校該系紀錄",
    "—",
    number(f.count) + " 筆",
    period(f.years),
    f.source || "資料缺失",
  ]);
  let text = `${SLUG_NAMES[slug]}（${ownYear} 學年）與${school}${p.dept}（${peerYear} 學年）指標如下。`;
  text +=
    f.count != null
      ? `\n交叉查榜（${period(f.years)}）：流向${school}${p.dept}共 **${f.count} 筆**。`
      : "\n缺少指定期間或目的系所資料，無法計算流向該系的紀錄。";
  text += "紀錄未跨年度去重，不代表不重複人數。";
  const complete =
    f.count != null &&
    (year == null ||
      (String(ownYear) === String(year) && String(peerYear) === String(year)));
  return response(
    "peer_comparison",
    text,
    {
      title: "系所實證對比",
      headers: [
        "指標",
        `本系（${ownYear}）`,
        `${p.dept}（${peerYear}）`,
        "本系減同儕／期間",
        "來源",
      ],
      rows,
    },
    {
      complete,
      school,
      peer_dept: p.dept,
      flow_records: f.count,
      years: f.years,
      indicator_years: [ownYear, peerYear],
    },
    [slug],
    `指標：${ownYear}／${peerYear} 學年；查榜：${period(f.years)}`,
  );
}
export function scopeResponse(message, intent, dossiers, slugs) {
  let year = requestedYear(message);
  const rows = [],
    missing = [],
    values = [],
    demo = intent === "demographics";
  const [key, label, unit] = message.includes("生師比")
    ? ["K06", "生師比", ""]
    : message.includes("退學")
      ? ["K02", "退學率", "%"]
      : message.includes("淨流失")
        ? ["K05", "淨流失率", "%"]
        : ["K01", "新生註冊率", "%"];
  const knownYears = slugs
    .map((s) => dossiers[s]?.meta?.latest_year)
    .filter((v) => v != null);
  year =
    year ?? (demo ? 117 : knownYears.length ? Math.max(...knownYears) : null);
  for (const slug of slugs) {
    const d = dossiers[slug] || {};
    let val, valid;
    if (demo) {
      const t =
        (d.demographics?.timeline || []).find(
          (t) => String(t.year) === String(year),
        ) || {};
      val = t.gap;
      valid = ["gap", "capacity", "est_baseline"].every((k) => t[k] != null);
      rows.push([
        SLUG_NAMES[slug],
        year,
        t.capacity ?? null,
        t.est_baseline ?? null,
        val ?? null,
        d.demographics?.source || "缺少資料",
      ]);
    } else {
      const k = d.kpis?.[key] || {};
      valid =
        year != null &&
        String(d.meta?.latest_year) === String(year) &&
        k.value != null;
      val = valid ? k.value : null;
      rows.push([SLUG_NAMES[slug], year, val, unit, k.source_id || "缺少資料"]);
    }
    if (!valid) missing.push(slug);
    else values.push([slug, val]);
  }
  const complete = missing.length === 0,
    facts = {
      complete,
      slugs,
      year,
      missing,
      metric: demo ? "gap" : key,
      values: Object.fromEntries(values),
    },
    scope = slugs.length === slugsAll.length ? "全院" : "所選系所";
  let text, headers;
  if (demo) {
    const total = complete ? values.reduce((a, [, v]) => a + v, 0) : null;
    facts.total_gap = total;
    text = complete
      ? `${scope} ${year} 學年基準推估缺口合計 ${number(total)} 人（推估入學數減核定名額）。`
      : `${year} 學年有系所缺少推估，無法提供${scope}總缺口。`;
    headers = ["系所", "學年", "名額", "基準推估", "缺口（人）", "來源"];
  } else {
    text = `${scope} ${year} 學年${label}比較如下。`;
    const threshold = message.match(/(?:超過|大於|高於)\s*(\d+(?:\.\d+)?)/);
    if (threshold) {
      const cutoff = Number(threshold[1]),
        matched = values.filter(([, v]) => v > cutoff).map(([s]) => s);
      Object.assign(facts, { threshold: cutoff, matched_slugs: matched });
      text +=
        "已收錄資料中超過提問門檻的系所：" +
        (matched.map((s) => SLUG_NAMES[s]).join("、") || "無") +
        "。";
    } else if (values.length && /最高|最低/.test(message)) {
      const best = (message.includes("最低") ? Math.min : Math.max)(
          ...values.map(([, v]) => v),
        ),
        matched = values.filter(([, v]) => v === best).map(([s]) => s);
      facts.matched_slugs = matched;
      text +=
        "已收錄資料中" +
        (message.includes("最低") ? "最低" : "最高") +
        "為" +
        matched.map((s) => SLUG_NAMES[s]).join("、") +
        `（${number(best)}${unit}）。`;
    }
    headers = ["系所", "學年", label, "單位", "來源"];
  }
  if (missing.length)
    text +=
      "缺少同年資料：" + missing.map((s) => SLUG_NAMES[s]).join("、") + "。";
  const result = response(
    demo ? "demographics" : "overview",
    text,
    { title: `${scope}同年比較`, headers, rows },
    facts,
    slugs,
    `${year} 學年`,
  );
  result.chart = {
    type: "bar",
    title: scope + (demo ? "推估缺口" : label),
    labels: slugs.map((s) => SLUG_NAMES[s]),
    datasets: [
      {
        label: demo ? "缺口（人）" : label,
        data: slugs.map((s) => facts.values[s] ?? null),
      },
    ],
  };
  return result;
}
