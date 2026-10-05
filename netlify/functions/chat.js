import DOSSIERS from "./dossiers.json";
import { checkGrounding } from "./lib/grounding.mjs";
import { selectedSlugs, schoolResponse, peerResponse, scopeResponse } from "./lib/query-responses.mjs";

const DEPT_ALIASES = {
  "國際貿易與經營": "ib", "國際貿易": "ib", "國貿": "ib", "國企": "ib", "國際企業": "ib", "國際商務": "ib",
  "企業管理": "ba", "企管": "ba", "工管": "ba", "工業管理": "ba", "工業工程": "ba",
  "會計資訊": "accounting", "會資": "accounting", "會計": "accounting",
  "財務金融": "finance", "財金": "finance", "金融": "finance",
  "保險金融管理": "insurance", "保金": "insurance", "保險": "insurance", "風險管理": "insurance", "風保": "insurance", "風管": "insurance",
  "應用統計": "stat", "應統": "stat", "統計": "stat", "資訊管理": "stat", "資管": "stat",
  "財政稅務": "tax", "財稅": "tax", "財政": "tax", "稅務": "tax"
};

const INTENT_RULES = [
  ["k24", ["K24", "k24", "綜合風險", "風險評級", "怎麼算", "計算公式", "公式", "權重"]],
  ["module5", ["競爭", "對手", "模組5", "模組 5", "流向", "外流", "搶走", "查榜", "落點", "重疊", "交叉", "競品", "敵校", "誰搶"]],
  ["demographics", ["少子化", "虎年", "117", "128", "名額", "缺口", "斷崖", "海嘯", "出生"]],
  ["partners", ["廠商", "產學", "實習", "雇主", "企業合作", "合作廠商", "公司"]],
  ["overview", ["註冊率", "退學", "休學", "生師比", "境外", "體質", "健康", "總覽", "警報", "預警", "指標", "同儕", "比較", "留存", "留存率", "淨流失", "流失率"]],
];

function detectSlug(text, defaultSlug = "ib") {
  if (!text) return defaultSlug;
  for (const [alias, slug] of Object.entries(DEPT_ALIASES).sort((a,b) => b[0].length - a[0].length)) {
    if (text.includes(alias)) return slug;
  }
  return defaultSlug;
}

const OUT_OF_SCOPE_REGEX = /(講話|說話|能說話|可以講話|你會講話|你能講話|語音|聊天|哈囉|你好|早安|晚安|嗨|你是誰|你的名字|自我介紹|去美國|怎麼去|機票|觀光|旅遊|天氣|今天幾號|星期幾|算命|星座|運勢|寫程式|寫代碼|寫python|寫javascript|寫一個Python爬蟲|寫一首詩|講笑話|講個笑話|唱首歌|推薦餐廳|美食|減肥|幫我寫作業)/i;

function isFastOutOfScope(msg) {
  if (!msg) return false;
  const substantive = msg.trim().replace(/^(?:(?:你好|您好|哈囉|早安|晚安|嗨)[，,！!。\s]*)+/, "");
  return OUT_OF_SCOPE_REGEX.test(substantive) || (!substantive && !!msg.trim());
}

async function classifyWithJev(msg, apiKey) {
  if (!apiKey || !msg || msg.trim().length < 2) return null;
  try {
    const payload = {
      model: "typesafe/jev-1.13",
      state: msg.trim(),
      questions: {
        is_ir_related: {
          type: "choice",
          instructions: "這條訊息是否與大專院校校務研究、招生、科系指標、少子化、產學等相關？",
          criteria: {
            ir: "與大學校務、註冊率、科系招生、少子化、產學等相關",
            out_of_scope: "日常閒聊、通用問題、旅遊交通、無關校務"
          }
        }
      }
    };
    const resp = await fetch("https://openrouter.ai/api/alpha/decisions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(3500)
    });
    if (resp.ok) {
      const data = await resp.json();
      const ans = data.answers?.is_ir_related;
      if (ans && ans.choice === "out_of_scope" && (ans.confidence ?? 1) >= 0.7) {
        return "out_of_scope";
      }
      if (ans && ans.choice === "ir") {
        return "ir";
      }
    }
  } catch (err) {
    console.warn("JEV classification skipped:", err.message);
  }
  return null;
}

function isRefusalText(text) {
  if (!text) return false;
  const refusalMarkers = [
    "僅處理校務", "只處理校務", "無關校務", "無法回答與校務無關", "非校務",
    "不在本助理服務範圍", "不在服務範圍", "無法提供旅遊", "無法回答此問題",
    "本助理僅專門處理", "無法處理非校務", "超出服務範圍", "無法回答日常",
    "日常閒聊"
  ];
  return refusalMarkers.some(m => text.includes(m));
}

const REFUSAL_RESPONSE = `本助理為國立臺中科技大學「校務研究（IR）決策助理」，專門服務系主任與校務研究人員，僅處理：系所指標、招生與生源、少子化推估、同儕競爭分析及產學合作等校務數據決策。

日常閒聊、語音互動或與校務無關之通用問題（如旅遊交通、個人生活諮詢），不在本系統服務範圍內。

請提出與校務決策或系所發展相關的實證問題（例如：「117年少子化缺口」、「國貿系與會資系註冊率比較」、「查榜競爭對手有誰」）。`;

const PEER_SCHOOL_ALIASES = {
  "高科": "國立高雄科技大學",
  "高科大": "國立高雄科技大學",
  "高雄科大": "國立高雄科技大學",
  "高雄科技大學": "國立高雄科技大學",
  "北商": "國立臺北商業大學",
  "北商大": "國立臺北商業大學",
  "台北商大": "國立臺北商業大學",
  "臺北商業大學": "國立臺北商業大學",
  "台北商業大學": "國立臺北商業大學",
  "逢甲": "逢甲大學",
  "逢甲大學": "逢甲大學",
  "勤益": "國立勤益科技大學",
  "勤益科大": "國立勤益科技大學",
  "勤益科技大學": "國立勤益科技大學",
  "雲科": "國立雲林科技大學",
  "雲科大": "國立雲林科技大學",
  "雲林科技大學": "國立雲林科技大學",
  "東海": "東海大學",
  "東海大學": "東海大學"
};

function detectPeerSchool(text) {
  if (!text) return null;
  for (const [alias, canonical] of Object.entries(PEER_SCHOOL_ALIASES).sort((a,b) => b[0].length - a[0].length)) {
    if (text.includes(alias)) return canonical;
  }
  return null;
}

function hasExplicitDept(text) {
  if (!text) return false;
  return Object.keys(DEPT_ALIASES).some(k => text.includes(k));
}

function route(msg) {
  for (const [intent, kws] of INTENT_RULES) {
    if (kws.some(k => msg.includes(k))) return intent;
  }
  if (hasExplicitDept(msg)) return "overview";
  return "general";
}

function slimDossier(d, sections) {
  const slim = { meta: d.meta };
  for (const k of (sections || [])) {
    if (d[k] !== undefined) slim[k] = d[k];
  }
  if (slim.demographics && slim.demographics.timeline) {
    const dm = { ...slim.demographics };
    dm.timeline = dm.timeline.filter(t => [113, 115, 117, 119, 121, 124, 128].includes(t.year));
    slim.demographics = dm;
  }
  if (slim.partners && slim.partners.clusters) {
    slim.partners = {
      csic_focus: slim.partners.csic_focus,
      clusters: slim.partners.clusters.map(c => ({
        category: c.category,
        companies: c.companies,
        verification: c.verification
      })),
      note: "名單為人工整理之候選清單；verified=false 者尚未經商工登記核對，回答時必須說明。"
    };
  }
  return JSON.stringify(slim, null, 1);
}

// ----------------- Grounding Check -----------------
// ----------------- Structured Builders -----------------
function kv(kpis, k) {
  return kpis?.[k]?.value;
}

function buildK24(d) {
  const { k24: k, kpis: kp, meta } = d;
  const labels = {
    K01: "註冊率",
    K05: "留存(100−淨流失)",
    K10: "同儕註冊率差",
    K19: "117 缺口耐受",
    K06: "生師比"
  };
  const rows = [];
  for (const [key, w] of Object.entries(k.weights || {})) {
    const raw = kv(kp, key);
    rows.push([
      labels[key] || key,
      key,
      `${Math.round(w * 100)}%`,
      raw !== undefined && raw !== null ? `${raw} ${kp?.[key]?.unit || ""}`.trim() : "無資料",
      k.subscores?.[key] ?? "—",
      k.contributions?.[key] ?? "—",
      kp?.[key]?.source_id || "—"
    ]);
  }
  let text = `${meta.dept_name} K24 = ${k.score}（${k.grade}）。`;
  if (k.missing && k.missing.length > 0) {
    text += ` 缺少指標：${k.missing.join(", ")}，分數以可得指標加權重算。`;
  }
  text += `\n公式：${k.formula}`;

  return {
    sections: ["kpis", "k24", "alerts"],
    source: "dept_data.json kpis（UDB 學12-1/學13-1/學14-1/學1-1/教1-1；內政部出生數推估）",
    fallback_text: text,
    drilldown_link: "heatmap.html",
    chart: {
      type: "radar",
      title: `${meta.dept_name} K24 五維子分數（0–100）`,
      labels: Object.keys(k.subscores || {}).map(x => labels[x] || x),
      datasets: [{
        label: "子分數",
        data: Object.values(k.subscores || {}),
        borderColor: "#059669",
        backgroundColor: "rgba(5,150,105,0.25)",
        borderWidth: 2
      }]
    },
    table: {
      title: `K24 計算明細（總分 ${k.score}）`,
      headers: ["維度", "指標", "權重", "原始值", "子分數", "加權貢獻", "來源"],
      rows
    }
  };
}

function buildModule5(d) {
  const m = d.module5;
  const meta = d.meta;
  if (!m) {
    return {
      sections: ["kpis"],
      source: "無交叉查榜檔",
      fallback_text: "本系目前沒有交叉查榜資料。"
    };
  }
  const rows = (m.top_destinations || []).map(t => [t.school, t.count, `${t.share_of_poached}%`]);
  let text = `${meta.dept_name}：交叉查榜本校系考生 ${m.own_candidates} 人（${(m.years || []).join("/")} 學年），留任 ${m.retained} 人（${m.retention_rate}%），外流 ${m.poached} 人，未分發 ${m.unplaced} 人。`;
  if (m.top_destinations && m.top_destinations.length > 0) {
    text += ` 外流最大去向：${m.top_destinations[0].school} ${m.top_destinations[0].count} 人。`;
  }

  return {
    sections: ["module5", "peers"],
    source: `交叉查榜 ${m.source}（${m.population_note}）`,
    fallback_text: text,
    chart: {
      type: "bar",
      title: `${meta.dept_name} 外流去向（人）`,
      labels: (m.top_destinations || []).map(t => t.school),
      datasets: [{
        label: "外流人數",
        data: (m.top_destinations || []).map(t => t.count),
        backgroundColor: "#2563eb",
        borderRadius: 6
      }]
    },
    table: {
      title: "外流去向 Top5",
      headers: ["學校", "人數", "占外流比例"],
      rows
    }
  };
}

function buildDemographics(d) {
  const { demographics: dm, meta } = d;
  const tl = dm?.timeline || [];
  const y117 = dm?.y117 || {};
  const y128 = dm?.y128 || {};
  const text = `${meta.dept_name} 核定名額 ${dm?.base_capacity}；117 學年基準推估新生 ${y117.est_baseline}，缺口 ${y117.gap} 人（${y117.gap_pct}%）；128 學年缺口 ${y128.gap} 人（${y128.gap_pct}%）。來源：${dm?.source || ""}。`;

  return {
    sections: ["demographics", "kpis", "alerts"],
    source: dm?.source || "",
    fallback_text: text,
    chart: {
      type: "line",
      title: `${meta.dept_name} 113–128 學年新生推估 vs 名額`,
      labels: tl.map(t => t.year),
      datasets: [
        { label: "基準推估", data: tl.map(t => t.est_baseline), borderColor: "#2563eb", fill: false },
        { label: "悲觀", data: tl.map(t => t.est_severe), borderColor: "#dc2626", fill: false },
        { label: "核定名額", data: tl.map(t => t.capacity), borderColor: "#6b7280", borderDash: [4, 4], fill: false }
      ]
    },
    table: {
      title: "推估明細",
      headers: ["學年", "出生數", "基準", "悲觀", "樂觀", "名額", "缺口", "缺口%"],
      rows: tl.map(t => [t.year, t.births, t.est_baseline, t.est_severe, t.est_aggressive, t.capacity, t.gap, t.gap_pct])
    }
  };
}

function buildPartners(d) {
  const p = d.partners || {};
  const meta = d.meta;
  const rows = [];
  for (const c of (p.clusters || [])) {
    for (const v of (c.verification || [])) {
      rows.push([
        c.category,
        v.name,
        v.tax_id || "—",
        v.status || "—",
        v.verified ? "已核對" : "未核對"
      ]);
    }
  }
  const nVer = rows.filter(r => r[4] === "已核對").length;
  const text = `${meta.dept_name} 候選合作廠商 ${rows.length} 家，其中 ${nVer} 家已經商工登記核對統編與狀態；其餘為人工整理清單，尚未驗證。對接營業項目：${p.csic_focus || "—"}。`;

  return {
    sections: ["partners", "kpis"],
    source: "dept_data.json partners（人工候選清單）＋ partners_verified.json（商工登記 API 核對結果）",
    fallback_text: text,
    table: {
      title: "候選廠商與商工登記核對狀態",
      headers: ["聚落", "公司", "統編", "登記狀態", "核對"],
      rows
    }
  };
}

function buildOverview(d) {
  const { kpis: kp, meta, alerts: al = [] } = d;
  const order = ["K01", "K02", "K03", "K04", "K05", "K06", "K07", "K09", "K10", "K19", "K23"];
  const rows = order
    .filter(k => kp?.[k])
    .map(k => [k, kp[k].name, kp[k].value, kp[k].unit, kp[k].source_id]);
  const peers = d.peers || [];

  const note = "已排除進修部夜間數據；進修四技因在職工作因素退學人數較高（60人），另列於戰情室學制診斷表。";
  let text = `${meta.dept_name}純日間部（${meta.latest_year || 114} 學年）：註冊率 ${kv(kp, "K01")}%、淨流失率 ${kv(kp, "K05")}%、生師比 ${kv(kp, "K06")}；K24 ${d.k24?.score}（${d.k24?.grade}）。\n（指標說明：${note}）`;
  if (al.length > 0) {
    text += ` 預警 ${al.length} 則：` + al.map(a => a.title).join("；");
  } else {
    text += " 目前無預警。";
  }

  let chart = null;
  if (peers.length > 0) {
    chart = {
      type: "bar",
      title: "本系 vs 同儕：新生註冊率（%）",
      labels: [meta.dept_name].concat(peers.map(x => `${x.school}${x.dept}`)),
      datasets: [{
        label: "註冊率",
        data: [kv(kp, "K01")].concat(peers.map(x => x.enrollment_rate)),
        backgroundColor: "#059669",
        borderRadius: 6
      }]
    };
  }

  return {
    sections: ["kpis", "k24", "alerts", "peers", "profile"],
    source: "dept_data.json（UDB 學1-1/學3-2/學12-1/學13-1/學14-1/教1-1；data.gov.tw 9622；純日間部口徑）",
    fallback_text: text,
    chart,
    table: {
      title: "核心指標（純日間部：四技＋二技＋五專）",
      headers: ["代碼", "指標", "值", "單位", "來源"],
      rows,
      note
    }
  };
}

function buildGeneral(d) {
  return {
    sections: ["kpis", "peers", "module5", "demographics", "partners", "alerts", "profile"],
    source: "dept_data.json（全系所實證數據庫與同儕數據）",
    fallback_text: "已為您整合檢索實證數據庫，請參閱上方分析結果。",
    chart: null,
    table: null,
    drilldown_link: null
  };
}

function isStrategicQuery(text) {
  if (!text) return false;
  return /(策略|怎麼看|如何看待|看法|建議|佈局|規劃|方向|作為院長|院長|診斷|對策|生源危機|轉型|因應|定位|招生成效|招生狀況|發展)/i.test(text);
}

function buildCollegeSummary(dossiers) {
  const depts = {};
  for (const [slug, d] of Object.entries(dossiers)) {
    const kp = d.kpis || {};
    const dm = d.demographics || {};
    const m5 = d.module5 || {};
    const prof = d.profile || {};
    depts[d.meta?.dept_name || slug] = {
      enrollment_rate: `${kp.K01?.value ?? "—"}%（純日間部註冊率，UDB 學12-1）`,
      dropout_rate: `${kp.K03?.value ?? "—"}%（純日間部退學率，UDB 學14-1）`,
      suspension_rate: `${kp.K04?.value ?? "—"}%（純日間部休學率，UDB 學13-1）`,
      retention_net_loss: `${kp.K05?.value ?? "—"}%（純日間部淨流失率，UDB 學13-1, 14-1）`,
      student_faculty_ratio: `${kp.K06?.value ?? "—"}（純日間部生師比，UDB 教1-1, 學1-1）`,
      scope_note: prof.scope_note || "純日間部基準",
      y117_demographic_gap: `${dm.y117?.gap ?? "—"} 人（${dm.y117?.gap_pct ?? "—"}%）`,
      top_competitors: (m5.top_destinations || []).slice(0, 3).map(t => `${t.school}${t.dept || ""}(${t.count}人)`),
      k24_grade: d.k24?.grade ?? "—",
      k24_score: d.k24?.score ?? "—"
    };
  }
  return {
    college_name: "國立臺中科技大學 商學院",
    analysis_scope: "全院 7 系全面以【純日間部】為基準（已嚴格排除進修部夜間在職流失數據）",
    departments: depts,
    total_y117_gap: "-122 人（-19.3%）",
    primary_competitors: [
      "國立高雄科技大學（全院累計外流 481 筆）",
      "國立雲林科技大學（123 筆）",
      "逢甲大學（107 筆）",
      "國立臺北商業大學（89 筆）"
    ]
  };
}

async function narrateCollegeStrategic({ userMsg, scoped, dossiers, apiKey, model, enableReasoning, history }) {
  const collegeSummary = buildCollegeSummary(dossiers);
  const isDean = /(院長|作為院長|院方)/.test(userMsg);

  const systemPrompt = `你是 國立臺中科技大學商學院 的院長級校務研究（IR）決策顧問與戰略大腦，服務對象是院長、系主任與校級決策主管。

## 角色設定與視角
${isDean ? "使用者明確要求以「作為商學院院長」視角發言。請以院長第一人稱高度（「身為商學院院長…」、「本院…」），展現宏觀、清晰且具備前瞻魄力的治理視野。" : "請站在「商學院整體戰略視角」，為院級主管提供客觀、深刻且具體可落地的戰略決策建言。"}
你唯一的數據依據是下方 <college_dossier>（收錄國貿、企管、會資、財金、保金、應統、財稅 7 大系所之實證數據）。

## 學制與統計口徑原則（極重要）：
全院分析一律以【純日間部】（日間四技、二技、五專、日間碩士）為絕對基準！
過去曾將進修部/夜間部在職學生因職場輪班或逾期未註冊的高流失率混入，造成會資、企管、財金退學率看似高達 7%~10% 的嚴重失真。
經校務研究精準分流核實：
- 全院 7 系純日間部新生註冊率極高（98.75% ~ 100.0%），整體招生吸引力強韌。
- 全院 7 系純日間部退學率均落在健康穩健區間（1.95% ~ 4.00%），日間四技學士更普遍僅 1.1% ~ 2.4%（企管日間四技僅 1.23%、會資日間四技 1.87%、應統 2.16%/四技 1.12%、國貿日間四技 1.21%、財金日間四技 2.14%、財稅日間四技 2.28%、保金四技 2.35%）。
- 任何退學與流失分析必須嚴格基於純日間部數據，絕不可再使用舊版未分流的進修部混合數字！

## 核心分析指引：
1. 【全院現況總評】：第一句直接定調全院招生體質（純日間部註冊率普遍高達 98.75%~100%，四技退學率僅 1%~2% 極為穩健；但面臨生師比負擔沉重、中部生源遭競校分流，以及 117 虎年少子化斷崖之長遠衝擊）。
2. 【各系現況與關鍵痛點剖析（純日間部基準）】：
   - 純日間部在學穩定度：說明各系日間部表現普遍穩健（純日間退學率：企管 1.95%、應統 2.16%、保金 2.25%、財金 2.43%、財稅 2.47%、國貿 2.82%、會資 4.00%），日間四技主體多在 1%~2%；會資與企管五專部科系探索轉換及進修部夜間流失另有專案輔導，不可與日間學士體質混為一談。
   - 師資負荷與教學資源：財金系專任生師比高達 40.2、財稅系 34.2、國貿系 33.7、會資系 27.0、應統系 26.4，專任師資負荷偏高，亟需彈性聘任與教學支持。
   - 跨校跨區生源外流：直面高科大（全院外流 481 筆）、雲科大（123 筆）、逢甲（107 筆）在中部技術高中生源的強烈吸力。
   - 少子化海嘯：117 虎年全院預估少子化缺口達 -122 人（-19.3%），全院各系缺口率普遍在 -18.6% ~ -20.0%。
3. 【四大戰略行動方針（Action Plan）】：
   - 跨系特色整合與 AI 賦能（如 AI+新商管跨域學程、ESG 綠色金融、數據會計與稅務科技）。
   - 生源前線深耕與防禦（強化中部技術高中宣傳，針對高科大重疊強項提出差異化定位）。
   - 學制與名額結構彈性調節（善用五專提前鎖定優秀生源，強化純日間部品質，優化進修部專班經營）。
   - 產學就業閉環對接（強化外銷經貿、在地金融機構與會計師事務所實習，打出「入學即就業」保證）。

## 輸出規範
- 觀點鮮明、嚴謹權威、條理分明。
- 數據嚴格符合 <college_dossier>，提及數字時括號標註出處（例如：114 學年 UDB 學12-1、學14-1 純日間部基準）。
- 250～450 字，條列清晰。
- 結尾註明：資料時點：2026-10-05；來源：教育部大專校院校務資訊公開平台（UDB 純日間部基準）、技專招聯會交叉查榜、內政部出生數推估。

<college_dossier>
${JSON.stringify(collegeSummary, null, 1)}
</college_dossier>`;

  const messages = [];
  for (const m of (history || []).slice(-6)) {
    if (m.role === "user" || m.role === "assistant") {
      messages.push({ role: m.role, content: m.content });
    }
  }
  messages.push({ role: "user", content: userMsg });

  try {
    const payload = {
      model,
      messages: [{ role: "system", content: systemPrompt }, ...messages],
      temperature: 0.3
    };
    if (enableReasoning) {
      payload.reasoning = { enabled: true };
    }

    const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${apiKey}`,
        "Content-Type": "application/json",
        "HTTP-Referer": process.env.SITE_URL || "https://nutc-ib-cockpit.netlify.app",
        "X-Title": process.env.SITE_NAME || "NUTC-IR-Autopilot"
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(35000)
    });

    if (orResp.ok) {
      const orData = await orResp.json();
      const choice = orData.choices?.[0];
      const narrative = choice?.message?.content?.trim() || null;
      const usedModel = orData.model || model;
      let reasoning = choice?.message?.reasoning || null;
      if (!reasoning && choice?.message?.reasoning_details) {
        const rd = choice.message.reasoning_details;
        if (Array.isArray(rd)) {
          reasoning = rd.map(x => (typeof x === "object" ? (x.text || JSON.stringify(x)) : String(x))).join("\n");
        }
      }
      const ground = checkGrounding(narrative, collegeSummary);
      return { narrative, reasoning, usedModel, ground };
    }
  } catch (err) {
    console.error("College strategic LLM call failed:", err);
  }
  return null;
}

const BUILDERS = {
  k24: buildK24,
  module5: buildModule5,
  demographics: buildDemographics,
  partners: buildPartners,
  overview: buildOverview,
  screenshot: buildOverview,
  general: buildGeneral
};

const SYSTEM_PROMPT_TEMPLATE = `你是 {school_name}{dept_name} 的校務研究（IR）決策助理，服務對象是系主任與校務研究人員。

## 資料契約
你唯一的數字來源是下方 <dossier>（JSON）。kpis 內每個指標含 value、unit、source_id、field。
- 回答中出現的每個數字、百分比、排名、校名、公司名，都必須能在 <dossier> 找到。
- 引用格式：數字後加括號標示來源，例：「99.53%（UDB 學12-1，114 學年）」。來源用短名（UDB 學12-1、交叉查榜、出生數推估、商工登記），同一來源在同一段落只標一次，不重複檔名。
- <dossier> 沒有的數字，一律寫「資料庫目前沒有這項資料」；不得估計、不得用常識補、不得引用訓練知識。
- partners 內 verified=false 的公司，必須說明「尚未經商工登記核對」。

## 學制與統計口徑原則（極重要）
- 本戰情室所有系所指標（新生註冊率、在學人數、休退學率、生師比等）全面以【純日間部】（四技、二技、五專、日間碩士）為唯一分析與評估基準，已嚴格排除進修部夜間在職流失數據。
- 說明或回答退學率、休學率或就學穩定度時，一律以純日間部數據為依據（各系純日間部退學率均在 1.95%~4.00% 穩健區間，日間四技學士更普遍僅 1.1%~2.4%），絕不可混入進修部/夜間部在職學生數據。若提問涉及夜間部或進修部，需明確指明其為進修在職特殊樣態，不得混淆為日間部體質。

## 推理規則
- 使用者問「是不是 X」或給一個數字問對不對：先用 <dossier> 的數字算一次，再表態，第一句不得直接說對或不對。
- 比較系所時，只比 <dossier> 同時有的指標，並標明學年。
- 不做因果推論；可說「同期發生」，不可說「因為…所以…」，除非 dossier 有該推估模型輸出（demographics）。
- 建議動作要綁回觸發它的指標或 alert。

## 同儕系所與特定主題查詢規則
- 當詢問特定同儕學校或系所（如「北商」、「高科大」、「逢甲」、「勤益」等）：
  - 聚焦於該同儕系所，從 <dossier> 的 peers 數據中整合該校系之 114 學年公開指標（如新生註冊率、在學人數、學年度退學率、專任生師比、境外生比率等）。
  - 客觀陳述該校表現與可比性，必要時可與本系現況進行簡潔對比，但不得混淆本系與同儕的主客體數據。
  - 資料庫未收錄的非公開資訊或歷史年份，明確註明「資料庫目前僅收錄該校 114 學年度 UDB 審定數據」。
- 當詢問綜合性或特定單項議題時：
  - 嚴格僅針對提問主題萃取直接相關的數據進行整合回答，條理分明。
  - 嚴禁主動堆疊無關模組資料（例如問同儕現況時，不扯入本系 K24 綜合公式或產學統編名單）。

## 範圍
只處理：校務指標、招生與生源、同儕比較、少子化推估、產學與雇主。範圍外的問題，一句話說明本助理只處理校務研究問題。

## 對人的限制
不評價任何自然人。涉及人時只陳述 <dossier> 中的次數或狀態。

## 輸出
- 第一句就是結論；不寫開場白、不重述問題、不自我介紹、不提及模型名稱或自身能力。
- 150–300 字；需要列舉用條列。
- 使用者附截圖時：先描述截圖中看得到的圖表與數值，再對照 <dossier>；不符要明說。
- 結尾固定一行：「資料時點：{fetched_at}；來源：」後接本次引用的 source_id 清單。

<dossier>
{dossier_json}
</dossier>`;

export default async (req, context) => {
  const headers = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Content-Type": "application/json; charset=utf-8"
  };

  if (req.method === "OPTIONS") {
    return new Response("", { status: 200, headers });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method Not Allowed" }), {
      status: 405,
      headers
    });
  }

  try {
    const body = await req.json().catch(() => ({}));
    const userMsg = String(body.message || "").slice(0, 2000);
    const image = body.image;
    const history = body.history || [];
    const defaultSlug = body.default_slug || "ib";
    const slug = detectSlug(userMsg, body.slug || defaultSlug);

    const d = DOSSIERS[slug] || DOSSIERS["ib"];
    if (!d) {
      return new Response(JSON.stringify({ error: "Dossier not found" }), {
        status: 404,
        headers
      });
    }

    const meta = d.meta;
    const apiKey = process.env.OPENROUTER_API_KEY;
    const model = process.env.OPENROUTER_MODEL || "google/gemini-3.8-flash";
    const enableReasoning = process.env.OPENROUTER_REASONING !== "false";

    let intent = image ? "screenshot" : route(userMsg);

    // 1. 快速過濾範圍外問題（閒聊、個人助理、旅遊交通等）
    if (!image) {
      if (isFastOutOfScope(userMsg)) {
        intent = "out_of_scope";
      } else if (intent === "general" && !detectPeerSchool(userMsg) && !hasExplicitDept(userMsg) && apiKey && !apiKey.includes("your_openrouter_api_key_here")) {
        // 2. 透過 JEV 決策模型進行進階分類
        const jevChoice = await classifyWithJev(userMsg, apiKey);
        if (jevChoice === "out_of_scope") {
          intent = "out_of_scope";
        }
      }
    }

    // 若判定為校務範圍外，立即拒答，嚴格不附帶任何圖表或表格
    if (intent === "out_of_scope") {
      return new Response(JSON.stringify({
        intent: "out_of_scope",
        dept: { slug, name: meta.dept_name, school: meta.school_name },
        response: REFUSAL_RESPONSE,
        model: "typesafe/jev-1.13",
        reasoning: "經 JEV-1.13 決策分類器與校務邊界政策檢驗，判定該諮詢為非校務研究範圍（out_of_scope）。依安全規範啟動拒答，嚴格不附帶任何統計圖表與指標明細。",
        grounding: { ok: true, note: "範圍外拒答，無引用數據" },
        source: "IR 邊界防護與 JEV-1.13 決策路由",
        data_time: meta.fetched_at || "2026-10-02"
      }), {
        status: 200,
        headers
      });
    }

    // 3. 處理同儕學校諮詢 (全校性 or 特定系所對比)
    const peerSchoolCanonical = !image ? detectPeerSchool(userMsg) : null;
    const hasDept = hasExplicitDept(userMsg);

    const slugs = selectedSlugs(userMsg, DEPT_ALIASES);
    let scoped = null;
    if (peerSchoolCanonical && (!hasDept || slugs.length === 7)) {
      scoped = schoolResponse(peerSchoolCanonical, DOSSIERS, userMsg);
    } else if (peerSchoolCanonical && hasDept) {
      scoped = peerResponse(slug, peerSchoolCanonical, DOSSIERS, userMsg);
    }
    if (!scoped && !image && slugs.length > 1) {
      scoped = scopeResponse(userMsg, intent, DOSSIERS, slugs);
      if (scoped && apiKey && !apiKey.includes("your_openrouter_api_key_here") && isStrategicQuery(userMsg)) {
        const collegeResult = await narrateCollegeStrategic({
          userMsg,
          scoped,
          dossiers: DOSSIERS,
          apiKey,
          model,
          enableReasoning,
          history
        });
        if (collegeResult && collegeResult.narrative) {
          scoped.response = collegeResult.narrative;
          scoped.reasoning = collegeResult.reasoning;
          scoped.model = collegeResult.usedModel;
          scoped.grounding = collegeResult.ground;
        }
      }
    }
    if (scoped) return new Response(JSON.stringify(scoped), { status: 200, headers });

    const builder = BUILDERS[intent] || BUILDERS.general;
    const structured = builder(d);

    let narrative = null;
    let reasoning = null;
    let usedModel = null;
    let ground = { ok: null, note: "模型未設定，僅顯示數據" };

    if (apiKey && !apiKey.includes("your_openrouter_api_key_here")) {
      const prompt = userMsg.trim() || (image ? "請解讀我截取的這張戰情圖表" : "請給我本系目前最重要的三個訊號");
      const systemPrompt = SYSTEM_PROMPT_TEMPLATE
        .replace("{school_name}", meta.school_name)
        .replace("{dept_name}", meta.dept_name)
        .replace("{fetched_at}", meta.fetched_at || "2026-10-02")
        .replace("{dossier_json}", slimDossier(d, structured.sections));

      const messages = [];
      for (const m of history.slice(-6)) {
        if (m.role === "user" || m.role === "assistant") {
          messages.push({ role: m.role, content: m.content });
        }
      }

      if (image && typeof image === "string" && image.startsWith("data:image/")) {
        messages.push({
          role: "user",
          content: [
            { type: "text", text: prompt },
            { type: "image_url", image_url: { url: image } }
          ]
        });
      } else {
        messages.push({ role: "user", content: prompt });
      }

      try {
        const payload = {
          model,
          messages: [{ role: "system", content: systemPrompt }, ...messages],
          temperature: 0.2
        };
        if (enableReasoning) {
          payload.reasoning = { enabled: true };
        }

        const orResp = await fetch("https://openrouter.ai/api/v1/chat/completions", {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${apiKey}`,
            "Content-Type": "application/json",
            "HTTP-Referer": process.env.SITE_URL || "https://nutc-ib-cockpit.netlify.app",
            "X-Title": process.env.SITE_NAME || "NUTC-IR-Autopilot"
          },
          body: JSON.stringify(payload),
          signal: AbortSignal.timeout(35000)
        });

        if (orResp.ok) {
          const orData = await orResp.json();
          const choice = orData.choices?.[0];
          narrative = choice?.message?.content?.trim() || null;
          usedModel = orData.model || model;
          const r = choice?.message?.reasoning || choice?.message?.reasoning_details;
          if (Array.isArray(r)) {
            reasoning = r.map(x => (typeof x === "object" ? x.text : String(x))).join("\n");
          } else if (typeof r === "string") {
            reasoning = r;
          }

          if (narrative) {
            ground = checkGrounding(narrative, JSON.parse(slimDossier(d, structured.sections)), prompt);
          }
        } else {
          const errText = await orResp.text();
          ground = { ok: null, note: `模型服務暫時異常 (HTTP ${orResp.status})` };
          console.error("OpenRouter error:", orResp.status, errText);
        }
      } catch (callErr) {
        console.error("OpenRouter fetch error:", callErr);
        ground = { ok: null, note: `模型呼叫失敗：${callErr.message}` };
      }
    }

    if (narrative && isRefusalText(narrative)) {
      return new Response(JSON.stringify({
        intent: "out_of_scope",
        dept: { slug, name: meta.dept_name, school: meta.school_name },
        response: narrative,
        model: usedModel,
        reasoning,
        grounding: { ok: true, note: "模型判定超出範圍拒答，無引用數據" },
        source: "IR 邊界防護",
        data_time: meta.fetched_at || "2026-10-02"
      }), {
        status: 200,
        headers
      });
    }

    const respData = {
      intent,
      dept: { slug, name: meta.dept_name, school: meta.school_name },
      response: narrative || structured.fallback_text,
      model: usedModel,
      reasoning,
      grounding: ground,
      source: structured.source,
      drilldown_link: structured.drilldown_link || `${slug}/index.html`,
      data_time: meta.fetched_at || "2026-10-02"
    };

    if (structured.chart) respData.chart = structured.chart;
    if (structured.table) respData.table = structured.table;

    return new Response(JSON.stringify(respData), {
      status: 200,
      headers
    });
  } catch (err) {
    console.error("Handler error:", err);
    return new Response(JSON.stringify({ error: String(err), response: "後端伺服器處理錯誤" }), {
      status: 500,
      headers
    });
  }
};
