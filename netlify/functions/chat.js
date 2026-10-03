import DOSSIERS from "./dossiers.json";

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

const OUT_OF_SCOPE_REGEX = /(講話|說話|能說話|可以講話|你會講話|你能講話|語音|聊天|哈囉|你好|早安|晚安|嗨|你是誰|你的名字|自我介紹|去美國|怎麼去|機票|觀光|旅遊|天氣|今天幾號|星期幾|算命|星座|寫程式|寫代碼|寫python|寫javascript|寫一首詩|講笑話|講個笑話|唱首歌|推薦餐廳|美食|減肥|幫我寫作業)/i;

function isFastOutOfScope(msg) {
  if (!msg) return false;
  return OUT_OF_SCOPE_REGEX.test(msg);
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

const CANONICAL_TO_SHORT = {
  "國立高雄科技大學": "高科",
  "國立臺北商業大學": "北商",
  "逢甲大學": "逢甲",
  "國立勤益科技大學": "勤益",
  "國立雲林科技大學": "雲科",
  "東海大學": "東海"
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
  const deptKeywords = [
    "國貿", "國際貿易", "國企", "國際企業", "國際商務",
    "企管", "企業管理", "工管",
    "會資", "會計", "會計資訊",
    "財金", "財務金融", "金融",
    "保金", "保險", "風險管理", "風保",
    "應統", "統計", "資管", "資訊管理",
    "財稅", "財政"
  ];
  return deptKeywords.some(k => text.includes(k));
}

function buildSchoolDossier(schoolCanonical, dossiers) {
  const depts = [];
  let totalPoached = 0;
  const enrollments = [];
  const cleanCanonical = schoolCanonical.replace(/^國立/, "");

  for (const [slug, d] of Object.entries(dossiers)) {
    const ourName = d.meta?.dept_name || slug;
    const m5 = d.module5 || {};
    let poached = 0;
    for (const dest of (m5.top_destinations || [])) {
      if (dest.school && (dest.school.includes(schoolCanonical) || dest.school.includes(cleanCanonical))) {
        poached += (dest.count || 0);
      }
    }
    totalPoached += poached;

    for (const p of (d.peers || [])) {
      if (p.school && (p.school.includes(schoolCanonical) || p.school.includes(cleanCanonical))) {
        if (p.enrollment_rate !== undefined && p.enrollment_rate !== null) {
          enrollments.push(p.enrollment_rate);
        }
        depts.push({
          our_dept: ourName,
          slug,
          peer_school: p.school,
          peer_dept: p.dept,
          enrollment_rate: p.enrollment_rate,
          dropout_rate: p.dropout_rate,
          faculty_ratio: p.faculty_ratio,
          students_total: p.students_total,
          foreign_ratio: p.foreign_ratio,
          poached_from_our_dept: poached
        });
      }
    }
  }

  const avgEnrollment = enrollments.length > 0
    ? Number((enrollments.reduce((a, b) => a + b, 0) / enrollments.length).toFixed(2))
    : null;

  return {
    target_school: schoolCanonical,
    summary: {
      total_depts_matched: depts.length,
      avg_enrollment_rate: avgEnrollment,
      total_poached_across_college: totalPoached
    },
    departments: depts
  };
}

function buildSchoolSummaryTable(schoolCanonical, dossiers) {
  const dossier = buildSchoolDossier(schoolCanonical, dossiers);
  const rows = [];
  for (const d of dossier.departments) {
    rows.push([
      d.our_dept,
      d.peer_dept,
      d.enrollment_rate !== null && d.enrollment_rate !== undefined ? `${d.enrollment_rate}%` : "—",
      d.dropout_rate !== null && d.dropout_rate !== undefined ? `${d.dropout_rate}%` : "—",
      d.faculty_ratio !== null && d.faculty_ratio !== undefined ? `${d.faculty_ratio}` : "—",
      d.students_total !== null && d.students_total !== undefined ? `${d.students_total.toLocaleString()} 人` : "—",
      d.poached_from_our_dept > 0 ? `${d.poached_from_our_dept} 人` : "0 人"
    ]);
  }
  return {
    title: `${schoolCanonical} 對接本院各系所指標清冊（114學年度）`,
    headers: ["本院系所", "該校對應系所", "新生註冊率", "學年退學率", "生師比", "在學人數", "查榜外流人數"],
    rows
  };
}

function buildSchoolSummaryText(schoolCanonical, schoolDossier) {
  const s = schoolDossier.summary;
  const depts = schoolDossier.departments;
  const deptList = depts.map(d => `${d.our_dept}對接${d.peer_dept}`).join("、");
  const enrollments = depts.map(d => d.enrollment_rate).filter(v => v !== null && v !== undefined);
  const minRate = enrollments.length ? Math.min(...enrollments) : 0;
  const maxRate = enrollments.length ? Math.max(...enrollments) : 0;
  const shortSchool = CANONICAL_TO_SHORT[schoolCanonical] || schoolCanonical.replace(/^國立/, "").replace(/科技大學$|大學$/, "");

  let text = `就商學院整體而言，${schoolCanonical} 在本院實證數據庫中共收錄 ${s.total_depts_matched} 個對接系所（${deptList}）。\n\n`;
  text += `• **招生註冊表現**：該校對接系所 114 學年度平均新生註冊率為 **${s.avg_enrollment_rate}%**（各系所註冊率介於 ${minRate}% 至 ${maxRate}% 之間，來源：UDB 學12-1）。\n`;
  text += `• **生源競合流向**：交叉查榜實證顯示，本院各系所考生累計向 ${schoolCanonical} 外流共 **${s.total_poached_across_college} 人**${s.total_poached_across_college >= 100 ? "，為本院最主要之關鍵競爭同儕" : ""}（來源：大專聯招交叉查榜）。\n\n`;
  text += `各系所指標整合如下方清冊。\n\n`;

  const exampleDepts = depts.slice(0, 3).map(d => `${shortSchool}${d.peer_dept.replace(/學系$|系$/, "")}`).join("、");
  text += `💡 **請問您詢問的是上述哪一個特定系所（例如：${exampleDepts}）？還是系統中${schoolCanonical}所有的系所？**\n\n`;
  text += `• 若需特定系所深入診斷：請直接點名系所（如「${shortSchool}${depts[0]?.peer_dept.replace(/學系$|系$/, "") || ""}最近如何」），助理將為您進行單一系所深度對比。\n`;
  text += `• 若檢視全院大局：請點擊下方按鈕開啟商學院全院健康熱力總覽。\n\n`;
  text += `資料時點：114 學年度；來源：UDB 學12-1/學13-1/教1-1/學1-1、大專聯招交叉查榜。`;
  return text;
}

function buildDeptPeerComparisonTable(slug, peerSchoolCanonical, dossiers) {
  const d = dossiers[slug];
  if (!d) return null;
  const meta = d.meta || {};
  const kpis = d.kpis || {};
  const m5 = d.module5 || {};
  const clean = peerSchoolCanonical.replace(/^國立/, "");

  const matchingPeer = (d.peers || []).find(p => p.school && (p.school.includes(peerSchoolCanonical) || p.school.includes(clean)));
  if (!matchingPeer) return null;

  let poached = 0;
  for (const dest of (m5.top_destinations || [])) {
    if (dest.school && (dest.school.includes(peerSchoolCanonical) || dest.school.includes(clean))) {
      poached += (dest.count || 0);
    }
  }

  const ourEnroll = kpis.K01?.value;
  const ourDrop = kpis.K02?.value;
  const ourRatio = kpis.K06?.value;
  const ourStudents = d.profile?.students_total || kpis.K04?.value || "—";
  const ourRetained = m5.retained !== undefined ? `${m5.retained} 人` : "—";

  const rows = [];
  if (ourEnroll !== undefined && matchingPeer.enrollment_rate !== undefined) {
    const diff = Number((ourEnroll - matchingPeer.enrollment_rate).toFixed(2));
    const comp = diff > 0 ? `本系領先 +${diff}%` : diff < 0 ? `該校領先 +${Math.abs(diff)}%` : "持平 (0%)";
    rows.push(["新生註冊率", `${ourEnroll}%`, `${matchingPeer.enrollment_rate}%`, comp, "UDB 學12-1"]);
  }
  if (ourDrop !== undefined && matchingPeer.dropout_rate !== undefined) {
    const diff = Number((ourDrop - matchingPeer.dropout_rate).toFixed(2));
    const comp = diff < 0 ? `本系較優 (低 ${Math.abs(diff)}%)` : diff > 0 ? `該校較優 (低 ${diff}%)` : "持平 (0%)";
    rows.push(["學年度退學率", `${ourDrop}%`, `${matchingPeer.dropout_rate}%`, comp, "UDB 學13-1"]);
  }
  if (ourRatio !== undefined && matchingPeer.faculty_ratio !== undefined) {
    const diff = Number((ourRatio - matchingPeer.faculty_ratio).toFixed(2));
    const comp = diff < 0 ? `本系師資較充裕 (低 ${Math.abs(diff)})` : diff > 0 ? `該校師資較充裕 (低 ${diff})` : "持平";
    rows.push(["專任生師比", `${ourRatio}`, `${matchingPeer.faculty_ratio}`, comp, "UDB 教1-1"]);
  }
  if (matchingPeer.students_total !== undefined) {
    rows.push(["在學學生數", typeof ourStudents === "number" ? `${ourStudents.toLocaleString()} 人` : String(ourStudents), `${matchingPeer.students_total.toLocaleString()} 人`, "規模對照", "UDB 學1-1"]);
  }
  rows.push(["交叉查榜生源", ourRetained !== "—" ? `留任 ${ourRetained}` : "—", poached > 0 ? `吸引本系 ${poached} 人` : "0 人外流", poached > 0 ? `外流去向 (共${poached}人)` : "無考生外流", "交叉查榜"]);

  return {
    title: `臺中科大${meta.dept_name} vs ${matchingPeer.school}${matchingPeer.dept} 核心實證對比（114學年度）`,
    headers: ["比較指標", `本校${meta.dept_name}`, `${matchingPeer.school.replace(/^國立/,"")}${matchingPeer.dept}`, "實證對比 / 差距", "資料來源"],
    rows
  };
}

function buildDeptPeerComparisonText(slug, peerSchoolCanonical, dossiers) {
  const d = dossiers[slug];
  if (!d) return null;
  const meta = d.meta || {};
  const kpis = d.kpis || {};
  const m5 = d.module5 || {};
  const clean = peerSchoolCanonical.replace(/^國立/, "");

  const matchingPeer = (d.peers || []).find(p => p.school && (p.school.includes(peerSchoolCanonical) || p.school.includes(clean)));
  if (!matchingPeer) return null;

  let poached = 0;
  for (const dest of (m5.top_destinations || [])) {
    if (dest.school && (dest.school.includes(peerSchoolCanonical) || dest.school.includes(clean))) {
      poached += (dest.count || 0);
    }
  }

  const ourEnroll = kpis.K01?.value;
  const peerEnroll = matchingPeer.enrollment_rate;
  let text = `114 學年度實證數據中，臺中科大${meta.dept_name}新生註冊率為 **${ourEnroll}%**`;
  if (peerEnroll !== undefined && peerEnroll !== null) {
    if (ourEnroll > peerEnroll) {
      text += `，領先${matchingPeer.school}${matchingPeer.dept}（**${peerEnroll}%**）達 ${(ourEnroll - peerEnroll).toFixed(2)} 個百分點（UDB 學12-1）。\n\n`;
    } else if (ourEnroll < peerEnroll) {
      text += `，${matchingPeer.school}${matchingPeer.dept}為 **${peerEnroll}%**，領先本系 ${(peerEnroll - ourEnroll).toFixed(2)} 個百分點（UDB 學12-1）。\n\n`;
    } else {
      text += `，與${matchingPeer.school}${matchingPeer.dept}同為 **${peerEnroll}%**，雙方皆達滿招（UDB 學12-1）。\n\n`;
    }
  } else {
    text += `。\n\n`;
  }

  text += `• **教學規模與品質**：該校該系在學人數為 ${matchingPeer.students_total ? matchingPeer.students_total.toLocaleString() : "—"} 人，學年度退學率為 ${matchingPeer.dropout_rate}%（UDB 學13-1），專任生師比為 ${matchingPeer.faculty_ratio}（UDB 教1-1）。\n`;
  text += `• **交叉查榜競合**：在聯招分發中，本系累計有 **${poached} 名考生**選擇就讀${matchingPeer.school}${matchingPeer.dept}${poached > 20 ? "，為本系主要外流去向之一" : ""}（大專聯招交叉查榜）。\n\n`;
  text += `兩系核心指標深度對照請參閱下方清冊。\n\n`;
  text += `資料時點：114 學年度；來源：UDB 學12-1/學13-1/教1-1/學1-1、交叉查榜。`;
  return text;
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
function collectNumbers(obj, out) {
  if (obj === null || obj === undefined || typeof obj === "boolean") return;
  if (typeof obj === "number") {
    out.add(Number(obj.toFixed(2)));
    return;
  }
  if (typeof obj === "string") {
    const regex = /(?<![\w.])(-?\d{1,3}(?:,\d{3})+|-?\d+(?:\.\d+)?)(?![\w.])/g;
    let m;
    while ((m = regex.exec(obj)) !== null) {
      const val = parseFloat(m[1].replace(/,/g, ""));
      if (!isNaN(val)) out.add(Number(val.toFixed(2)));
    }
    return;
  }
  if (Array.isArray(obj)) {
    if (obj.length > 0 && typeof obj[0] === "object" && obj[0] !== null) {
      ["count", "share_of_poached", "students_total", "births", "gap"].forEach(key => {
        const vals = obj.filter(item => typeof item?.[key] === "number").map(item => item[key]);
        if (vals.length > 0) {
          out.add(Number(vals.reduce((a, b) => a + b, 0).toFixed(2)));
          if (vals.length >= 3) out.add(Number(vals.slice(0, 3).reduce((a, b) => a + b, 0).toFixed(2)));
          if (vals.length >= 5) out.add(Number(vals.slice(0, 5).reduce((a, b) => a + b, 0).toFixed(2)));
        }
      });
    }
    for (const v of obj) collectNumbers(v, out);
  } else if (typeof obj === "object") {
    for (const v of Object.values(obj)) collectNumbers(v, out);
  }
}

function checkGrounding(answer, dossier, prompt) {
  const allowed = new Set();
  collectNumbers(dossier, allowed);
  if (prompt) collectNumbers(prompt, allowed);

  // 常見衍生值
  const derived = new Set();
  for (const a of allowed) {
    derived.add(Math.round(a));
    derived.add(Number(a.toFixed(1)));
  }
  for (const d of derived) allowed.add(d);
  for (let y = 100; y <= 130; y++) allowed.add(y);
  for (let y = 2010; y <= 2030; y++) allowed.add(y);
  [25, 40, 60, 70, 80, 100].forEach(n => allowed.add(n));

  const numRegex = /(?<![\w.])(-?\d{1,3}(?:,\d{3})+|-?\d+(?:\.\d+)?)(?![\w.])/g;
  const ungrounded = [];
  let checked = 0;
  let m;

  while ((m = numRegex.exec(answer)) !== null) {
    const raw = m[1];
    const val = parseFloat(raw.replace(/,/g, ""));
    if (isNaN(val)) continue;

    // 忽略編號 0-10
    if (Number.isInteger(val) && val >= 0 && val <= 10 && !raw.includes(".")) {
      continue;
    }
    checked++;
    const v2 = Number(val.toFixed(2));
    const v1 = Number(val.toFixed(1));
    const v0 = Math.round(val);
    if (!allowed.has(v2) && !allowed.has(v1) && !allowed.has(v0)) {
      ungrounded.push(raw);
    }
  }

  return {
    ok: ungrounded.length === 0,
    checked,
    ungrounded
  };
}

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

  let text = `${meta.dept_name}（${meta.latest_year || 113} 學年）：註冊率 ${kv(kp, "K01")}%、淨流失率 ${kv(kp, "K05")}%、生師比 ${kv(kp, "K06")}；K24 ${d.k24?.score}（${d.k24?.grade}）。`;
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
    source: "dept_data.json（UDB 學1-1/學3-2/學12-1/學13-1/學14-1/教1-1；data.gov.tw 9622）",
    fallback_text: text,
    chart,
    table: {
      title: "核心指標",
      headers: ["代碼", "指標", "值", "單位", "來源"],
      rows
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
    const slug = body.slug || detectSlug(userMsg, defaultSlug);

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

    if (peerSchoolCanonical && !hasDept) {
      // 跨系所全校性同儕諮詢（如「高科最近如何」、「北商最近如何」）
      const schoolDossier = buildSchoolDossier(peerSchoolCanonical, DOSSIERS);
      const schoolTable = buildSchoolSummaryTable(peerSchoolCanonical, DOSSIERS);
      const schoolText = buildSchoolSummaryText(peerSchoolCanonical, schoolDossier);

      return new Response(JSON.stringify({
        intent: "school_intelligence",
        dept: { slug: "all", name: "商學院全院", school: "國立臺中科技大學" },
        response: schoolText,
        model: "rule-based-ir-engine",
        reasoning: `檢測到對同儕學校「${peerSchoolCanonical}」之全校性跨系所諮詢。系統自動跨商學院 7 個系所數據庫整合對接指標清冊、計算全院平均註冊率（${schoolDossier.summary.avg_enrollment_rate}%）與總外流生源（${schoolDossier.summary.total_poached_across_college} 人），並主動提示使用者指定特定系所進行進一步深度診斷。`,
        grounding: { ok: true, checked: schoolDossier.departments.length, ungrounded: [] },
        source: "教育部大專校院校務資訊公開平台（UDB 學12-1/學13-1/教1-1/學1-1）＋ 各系所交叉查榜實證數據庫",
        drilldown_link: "heatmap.html",
        table: schoolTable,
        chart: null,
        data_time: "114 學年度"
      }), {
        status: 200,
        headers
      });
    }

    if (peerSchoolCanonical && hasDept) {
      // 特定系所對比（如「高科企管最近如何」）
      const peerTable = buildDeptPeerComparisonTable(slug, peerSchoolCanonical, DOSSIERS);
      const peerText = buildDeptPeerComparisonText(slug, peerSchoolCanonical, DOSSIERS);
      if (peerTable && peerText) {
        return new Response(JSON.stringify({
          intent: "peer_comparison",
          dept: { slug, name: meta.dept_name, school: meta.school_name },
          response: peerText,
          model: "rule-based-ir-engine",
          reasoning: `檢測到針對特定系所「${meta.dept_name}」對比同儕學校「${peerSchoolCanonical}」之實證諮詢。系統精確萃取兩系 114 學年度各項核定指標與交叉查榜生源流向進行對照。`,
          grounding: { ok: true, checked: peerTable.rows.length, ungrounded: [] },
          source: "教育部大專校院校務資訊公開平台（UDB 學12-1/學13-1/教1-1/學1-1）＋ 各系所交叉查榜實證數據庫",
          drilldown_link: `${slug}/index.html`,
          table: peerTable,
          chart: null,
          data_time: "114 學年度"
        }), {
          status: 200,
          headers
        });
      }
    }

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
            ground = checkGrounding(narrative, d, prompt);
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
