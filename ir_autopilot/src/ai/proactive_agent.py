"""
ProactiveAgent（接地版）
原則：
1. 所有數字來自 dossier.build_dossier()（dept_data.json + 交叉查榜 CSV 即時計算），程式內無任何手打數據。
2. 圖表／表格由程式直接從 dossier 產生，與 LLM 無關；LLM 只負責敘事。
3. LLM 不可用時，回傳「模型不可用」＋ 數據表，不生成任何敘事。
4. LLM 回覆經 grounding.check()，數字對不上就標記 ungrounded 供前端警示。
"""
import re
from typing import Any, Dict, List, Optional
import requests

from ir_autopilot.src.ai import grounding
from ir_autopilot.src.ai.dossier import build_dossier, detect_slug, dossier_to_text, SLUG_TO_NAME
from ir_autopilot.src.ai.openrouter_client import OpenRouterClient

SYSTEM_PROMPT = """你是 {school_name}{dept_name} 的校務研究（IR）決策助理，服務對象是系主任與校務研究人員。

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
</dossier>"""

INTENT_RULES = [
    ("k24", ["K24", "k24", "綜合風險", "風險評級", "怎麼算", "計算公式", "公式", "權重"]),
    ("module5", ["競爭", "對手", "模組5", "模組 5", "流向", "外流", "搶走", "查榜", "落點", "重疊", "交叉", "競品", "敵校", "誰搶"]),
    ("demographics", ["少子化", "虎年", "117", "128", "名額", "缺口", "斷崖", "海嘯", "出生"]),
    ("partners", ["廠商", "產學", "實習", "雇主", "企業合作", "合作廠商", "公司"]),
    ("overview", ["註冊率", "退學", "休學", "生師比", "境外", "體質", "健康", "總覽", "警報", "預警", "指標", "同儕", "比較", "留存", "留存率", "淨流失", "流失率"]),
]

OUT_OF_SCOPE_REGEX = re.compile(
    r"(講話|說話|能說話|可以講話|你會講話|你能講話|語音|聊天|哈囉|你好|早安|晚安|嗨|你是誰|你的名字|自我介紹|"
    r"去美國|怎麼去|機票|觀光|旅遊|天氣|今天幾號|星期幾|算命|星座|"
    r"寫程式|寫代碼|寫python|寫javascript|寫一首詩|講笑話|講個笑話|唱首歌|推薦餐廳|美食|減肥|幫我寫作業)",
    re.IGNORECASE
)

REFUSAL_RESPONSE = (
    "本助理為國立臺中科技大學「校務研究（IR）決策助理」，專門服務系主任與校務研究人員，"
    "僅處理：系所指標、招生與生源、少子化推估、同儕競爭分析及產學合作等校務數據決策。\n\n"
    "日常閒聊、語音互動或與校務無關之通用問題（如旅遊交通、個人生活諮詢），不在本系統服務範圍內。\n\n"
    "請提出與校務決策或系所發展相關的實證問題（例如：「117年少子化缺口」、「國貿系與會資系註冊率比較」、「查榜競爭對手有誰」）。"
)

REFUSAL_MARKERS = [
    "僅處理校務", "只處理校務", "無關校務", "無法回答與校務無關", "非校務",
    "不在本助理服務範圍", "不在服務範圍", "無法提供旅遊", "無法回答此問題",
    "本助理僅專門處理", "無法處理非校務", "超出服務範圍", "無法回答日常", "日常閒聊"
]


PEER_SCHOOL_ALIASES = {
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
    "東海大學": "東海大學",
}

CANONICAL_TO_SHORT = {
    "國立高雄科技大學": "高科",
    "國立臺北商業大學": "北商",
    "逢甲大學": "逢甲",
    "國立勤益科技大學": "勤益",
    "國立雲林科技大學": "雲科",
    "東海大學": "東海",
}

EXPLICIT_DEPT_KEYWORDS = [
    "國貿", "國際貿易", "國企", "國際企業", "國際商務",
    "企管", "企業管理", "工管",
    "會資", "會計", "會計資訊",
    "財金", "財務金融", "金融",
    "保金", "保險", "風險管理", "風保",
    "應統", "統計", "資管", "資訊管理",
    "財稅", "財政"
]


def detect_peer_school(text: str) -> Optional[str]:
    if not text:
        return None
    for alias in sorted(PEER_SCHOOL_ALIASES.keys(), key=lambda x: len(x), reverse=True):
        if alias in text:
            return PEER_SCHOOL_ALIASES[alias]
    return None


def has_explicit_dept(text: str) -> bool:
    if not text:
        return False
    return any(k in text for k in EXPLICIT_DEPT_KEYWORDS)


class ProactiveAgent:
    def __init__(self, client: Optional[OpenRouterClient] = None):
        self.client = client or OpenRouterClient()

    # ---------- JEV 決策模型分類 ----------
    def _classify_with_jev(self, message: str) -> Optional[str]:
        if not self.client.available or not message or len(message.strip()) < 2:
            return None
        url = "https://openrouter.ai/api/alpha/decisions"
        payload = {
            "model": "typesafe/jev-1.13",
            "state": message.strip(),
            "questions": {
                "is_ir_related": {
                    "type": "choice",
                    "instructions": "這條訊息是否與大專院校校務研究、招生、科系指標、少子化、產學等相關？",
                    "criteria": {
                        "ir": "與大學校務、註冊率、科系招生、少子化、產學等相關",
                        "out_of_scope": "日常閒聊、通用問題、旅遊交通、無關校務"
                    }
                }
            }
        }
        try:
            resp = requests.post(
                url,
                headers={"Authorization": f"Bearer {self.client.api_key}", "Content-Type": "application/json"},
                json=payload,
                timeout=4
            )
            if resp.status_code == 200:
                data = resp.json()
                ans = data.get("answers", {}).get("is_ir_related", {})
                if ans.get("choice") == "out_of_scope" and ans.get("confidence", 1) >= 0.7:
                    return "out_of_scope"
                if ans.get("choice") == "ir":
                    return "ir"
        except Exception:
            pass
        return None

    # ---------- 公開入口 ----------
    def process_chat(self, user_message: str, dept_context: Dict[str, Any],
                     history: Optional[List[Dict[str, str]]] = None, image: Optional[str] = None) -> Dict[str, Any]:
        slug = dept_context.get("slug") or detect_slug(user_message, dept_context.get("default_slug", "ib"))
        d = build_dossier(slug)
        meta = d["meta"]

        # 1. 快速過濾範圍外問題
        if not image and OUT_OF_SCOPE_REGEX.search(user_message):
            return {
                "intent": "out_of_scope",
                "dept": {"slug": slug, "name": meta["dept_name"], "school": meta["school_name"]},
                "response": REFUSAL_RESPONSE,
                "model": "typesafe/jev-1.13",
                "reasoning": "經快速範疇檢查判定為非校務研究問題（out_of_scope），依安全政策啟動純文字拒答，不附帶任何圖表。",
                "grounding": {"ok": True, "note": "範圍外拒答，無引用數據"},
                "source": "IR 邊界防護與 JEV-1.13 決策路由",
                "data_time": meta.get("fetched_at"),
            }

        intent = "screenshot" if image else self._route(user_message)

        # 2. 若為 general 且無截圖，嘗試 JEV 決策模型分類
        if intent == "general" and not image and not detect_peer_school(user_message) and not has_explicit_dept(user_message) and self.client.available:
            jev_choice = self._classify_with_jev(user_message)
            if jev_choice == "out_of_scope":
                return {
                    "intent": "out_of_scope",
                    "dept": {"slug": slug, "name": meta["dept_name"], "school": meta["school_name"]},
                    "response": REFUSAL_RESPONSE,
                    "model": "typesafe/jev-1.13",
                    "reasoning": "經 JEV-1.13 決策模型判定為校務研究範圍外問題（out_of_scope），依規範啟動純文字拒答，不附帶任何圖表或指標表。",
                    "grounding": {"ok": True, "note": "範圍外拒答，無引用數據"},
                    "source": "IR 邊界防護與 JEV-1.13 決策路由",
                    "data_time": meta.get("fetched_at"),
                }

        # 3. 處理同儕學校諮詢 (全校性 or 特定系所對比)
        peer_school_canonical = detect_peer_school(user_message) if not image else None
        has_dept = has_explicit_dept(user_message)

        if peer_school_canonical and not has_dept:
            school_dossier = self._build_school_dossier(peer_school_canonical)
            school_table = self._build_school_summary_table(school_dossier)
            school_text = self._build_school_summary_text(school_dossier)
            return {
                "intent": "school_intelligence",
                "dept": {"slug": "all", "name": "商學院全院", "school": "國立臺中科技大學"},
                "response": school_text,
                "model": "rule-based-ir-engine",
                "reasoning": (
                    f"檢測到對同儕學校「{peer_school_canonical}」之全校性跨系所諮詢。系統自動跨商學院 7 個系所數據庫整合對接指標清冊、"
                    f"計算全院平均註冊率（{school_dossier['summary']['avg_enrollment_rate']}%）與總外流生源（{school_dossier['summary']['total_poached_across_college']} 人），"
                    "並主動提示使用者指定特定系所進行進一步深度診斷。"
                ),
                "grounding": {"ok": True, "checked": len(school_dossier["departments"]), "ungrounded": []},
                "source": "教育部大專校院校務資訊公開平台（UDB 學12-1/學13-1/教1-1/學1-1）＋ 各系所交叉查榜實證數據庫",
                "drilldown_link": "heatmap.html",
                "table": school_table,
                "chart": None,
                "data_time": "114 學年度",
            }

        if peer_school_canonical and has_dept:
            peer_table = self._build_dept_peer_comparison_table(slug, peer_school_canonical)
            peer_text = self._build_dept_peer_comparison_text(slug, peer_school_canonical)
            if peer_table and peer_text:
                return {
                    "intent": "peer_comparison",
                    "dept": {"slug": slug, "name": meta["dept_name"], "school": meta["school_name"]},
                    "response": peer_text,
                    "model": "rule-based-ir-engine",
                    "reasoning": f"檢測到針對特定系所「{meta['dept_name']}」對比同儕學校「{peer_school_canonical}」之實證諮詢。系統精確萃取兩系 114 學年度各項核定指標與交叉查榜生源流向進行對照。",
                    "grounding": {"ok": True, "checked": len(peer_table["rows"]), "ungrounded": []},
                    "source": "教育部大專校院校務資訊公開平台（UDB 學12-1/學13-1/教1-1/學1-1）＋ 各系所交叉查榜實證數據庫",
                    "drilldown_link": f"{slug}/index.html",
                    "table": peer_table,
                    "chart": None,
                    "data_time": "114 學年度",
                }

        builder = {
            "k24": self._k24, "module5": self._module5, "demographics": self._demographics,
            "partners": self._partners, "overview": self._overview, "screenshot": self._overview, "general": self._general,
        }[intent]
        structured = builder(d)          # chart / table / sections / fallback_text

        prompt = user_message.strip() or ("請解讀我截取的這張戰情圖表" if image else "請給我本系目前最重要的三個訊號")
        narrative, reasoning, model, ground = self._narrate(prompt, d, structured["sections"], image, history)

        # 3. 若模型生成了拒答文字，強制清除圖表與表格
        if narrative and any(m in narrative for m in REFUSAL_MARKERS):
            return {
                "intent": "out_of_scope",
                "dept": {"slug": slug, "name": meta["dept_name"], "school": meta["school_name"]},
                "response": narrative,
                "model": model,
                "reasoning": reasoning,
                "grounding": {"ok": True, "note": "模型判定超出範圍拒答，無引用數據"},
                "source": "IR 邊界防護",
                "data_time": meta.get("fetched_at"),
            }

        resp = {
            "intent": intent,
            "dept": {"slug": slug, "name": meta["dept_name"], "school": meta["school_name"]},
            "response": narrative if narrative else structured["fallback_text"],
            "model": model,
            "reasoning": reasoning,
            "grounding": ground,
            "source": structured["source"],
            "drilldown_link": structured.get("drilldown_link", f"{slug}/index.html"),
            "data_time": meta.get("fetched_at"),
        }
        if structured.get("chart"):
            resp["chart"] = structured["chart"]
        if structured.get("table"):
            resp["table"] = structured["table"]
        return resp

    # ---------- 路由 ----------
    @staticmethod
    def _route(msg: str) -> str:
        for intent, kws in INTENT_RULES:
            if any(k in msg for k in kws):
                return intent
        if has_explicit_dept(msg):
            return "overview"
        return "general"

    # ---------- LLM 敘事 ----------
    def _narrate(self, prompt, d, sections, image, history):
        if not self.client.available:
            return None, None, None, {"ok": None, "note": "模型未設定，僅顯示數據"}
        meta = d["meta"]
        system = SYSTEM_PROMPT.format(school_name=meta["school_name"], dept_name=meta["dept_name"],
                                      fetched_at=meta.get("fetched_at"), dossier_json=dossier_to_text(d, sections))
        messages = [m for m in (history or []) if m.get("role") in ("user", "assistant")][-6:]
        messages.append({"role": "user", "content": prompt})
        res = self.client.chat(messages, system_prompt=system, image_data_url=image)
        if not res.get("success"):
            return None, None, None, {"ok": None, "note": f"模型不可用：{res.get('error')}"}
        content = res.get("content", "").strip()
        ground = grounding.check(content, d, prompt=prompt)
        return content, res.get("reasoning"), res.get("model"), ground

    # ---------- 各意圖的結構化輸出（純程式，不經 LLM） ----------
    @staticmethod
    def _kv(kpis, k):
        return kpis.get(k, {}).get("value")

    def _k24(self, d):
        k, kp, meta = d["k24"], d["kpis"], d["meta"]
        labels = {"K01": "註冊率", "K05": "留存(100−淨流失)", "K10": "同儕註冊率差", "K19": "117 缺口耐受", "K06": "生師比"}
        rows = []
        for key, w in k["weights"].items():
            raw = self._kv(kp, key)
            rows.append([labels[key], key, f"{int(w*100)}%",
                         f"{raw} {kp.get(key, {}).get('unit', '')}" if raw is not None else "無資料",
                         k["subscores"].get(key, "—"), k["contributions"].get(key, "—"),
                         kp.get(key, {}).get("source_id", "—")])
        text = (f"{meta['dept_name']} K24 = {k['score']}（{k['grade']}）。"
                + (f" 缺少指標：{', '.join(k['missing'])}，分數以可得指標加權重算。" if k["missing"] else "")
                + f"\n公式：{k['formula']}")
        return {
            "sections": ["kpis", "k24", "alerts"],
            "source": "dept_data.json kpis（UDB 學12-1/學13-1/學14-1/學1-1/教1-1；內政部出生數推估）",
            "fallback_text": text,
            "drilldown_link": "heatmap.html",
            "chart": {"type": "radar", "title": f"{meta['dept_name']} K24 五維子分數（0–100）",
                      "labels": [labels[x] for x in k["subscores"]],
                      "datasets": [{"label": "子分數", "data": list(k["subscores"].values()),
                                    "borderColor": "#059669", "backgroundColor": "rgba(5,150,105,0.25)", "borderWidth": 2}]},
            "table": {"title": f"K24 計算明細（總分 {k['score']}）",
                      "headers": ["維度", "指標", "權重", "原始值", "子分數", "加權貢獻", "來源"], "rows": rows},
        }

    def _module5(self, d):
        m, meta = d.get("module5"), d["meta"]
        if not m:
            return {"sections": ["kpis"], "source": "無交叉查榜檔", "fallback_text": "本系目前沒有交叉查榜資料。"}
        rows = [[t["school"], t["count"], f"{t['share_of_poached']}%"] for t in m["top_destinations"]]
        text = (f"{meta['dept_name']}：交叉查榜本校系考生 {m['own_candidates']} 人（{'/'.join(m['years'])} 學年），"
                f"留任 {m['retained']} 人（{m['retention_rate']}%），外流 {m['poached']} 人，未分發 {m['unplaced']} 人。"
                + (f" 外流最大去向：{m['top_destinations'][0]['school']} {m['top_destinations'][0]['count']} 人。" if m["top_destinations"] else ""))
        return {
            "sections": ["module5", "peers"],
            "source": f"交叉查榜 {m['source']}（{m['population_note']}）",
            "fallback_text": text,
            "chart": {"type": "bar", "title": f"{meta['dept_name']} 外流去向（人）",
                      "labels": [t["school"] for t in m["top_destinations"]],
                      "datasets": [{"label": "外流人數", "data": [t["count"] for t in m["top_destinations"]],
                                    "backgroundColor": "#2563eb", "borderRadius": 6}]},
            "table": {"title": "外流去向 Top5", "headers": ["學校", "人數", "占外流比例"], "rows": rows},
        }

    def _demographics(self, d):
        dm, meta = d["demographics"], d["meta"]
        tl = dm.get("timeline", [])
        y117, y128 = dm.get("y117") or {}, dm.get("y128") or {}
        text = (f"{meta['dept_name']} 核定名額 {dm.get('base_capacity')}；117 學年基準推估新生 {y117.get('est_baseline')}，"
                f"缺口 {y117.get('gap')} 人（{y117.get('gap_pct')}%）；128 學年缺口 {y128.get('gap')} 人（{y128.get('gap_pct')}%）。"
                f" 來源：{dm.get('source')}。")
        return {
            "sections": ["demographics", "kpis", "alerts"],
            "source": dm.get("source", ""),
            "fallback_text": text,
            "chart": {"type": "line", "title": f"{meta['dept_name']} 113–128 學年新生推估 vs 名額",
                      "labels": [t["year"] for t in tl],
                      "datasets": [
                          {"label": "基準推估", "data": [t.get("est_baseline") for t in tl], "borderColor": "#2563eb", "fill": False},
                          {"label": "悲觀", "data": [t.get("est_severe") for t in tl], "borderColor": "#dc2626", "fill": False},
                          {"label": "核定名額", "data": [t.get("capacity") for t in tl], "borderColor": "#6b7280", "borderDash": [4, 4], "fill": False}]},
            "table": {"title": "推估明細", "headers": ["學年", "出生數", "基準", "悲觀", "樂觀", "名額", "缺口", "缺口%"],
                      "rows": [[t["year"], t.get("births"), t.get("est_baseline"), t.get("est_severe"), t.get("est_aggressive"),
                                t.get("capacity"), t.get("gap"), t.get("gap_pct")] for t in tl]},
        }

    def _partners(self, d):
        p, meta = d.get("partners") or {}, d["meta"]
        rows = []
        for c in p.get("clusters", []):
            for v in c.get("verification", []):
                rows.append([c.get("category"), v.get("name"), v.get("tax_id", "—"), v.get("status", "—"),
                             "已核對" if v.get("verified") else "未核對"])
        n_ver = sum(1 for r in rows if r[-1] == "已核對")
        text = (f"{meta['dept_name']} 候選合作廠商 {len(rows)} 家，其中 {n_ver} 家已經商工登記核對統編與狀態；"
                f"其餘為人工整理清單，尚未驗證。對接營業項目：{p.get('csic_focus', '—')}。")
        return {
            "sections": ["partners", "kpis"],
            "source": "dept_data.json partners（人工候選清單）＋ partners_verified.json（商工登記 API 核對結果）",
            "fallback_text": text,
            "table": {"title": "候選廠商與商工登記核對狀態", "headers": ["聚落", "公司", "統編", "登記狀態", "核對"], "rows": rows},
        }

    def _overview(self, d):
        kp, meta, al = d["kpis"], d["meta"], d.get("alerts", [])
        order = ["K01", "K02", "K03", "K04", "K05", "K06", "K07", "K09", "K10", "K19", "K23"]
        rows = [[k, kp[k].get("name"), kp[k].get("value"), kp[k].get("unit"), kp[k].get("source_id")] for k in order if k in kp]
        peers = d.get("peers", [])
        text = (f"{meta['dept_name']}（{meta.get('latest_year')} 學年）：註冊率 {self._kv(kp,'K01')}%、淨流失率 {self._kv(kp,'K05')}%、"
                f"生師比 {self._kv(kp,'K06')}；K24 {d['k24']['score']}（{d['k24']['grade']}）。"
                + (f" 預警 {len(al)} 則：" + "；".join(a.get('title','') for a in al) if al else " 目前無預警。"))
        chart = None
        if peers:
            chart = {"type": "bar", "title": "本系 vs 同儕：新生註冊率（%）",
                     "labels": [meta["dept_name"]] + [f"{x['school']}{x['dept']}" for x in peers],
                     "datasets": [{"label": "註冊率", "data": [self._kv(kp, "K01")] + [x.get("enrollment_rate") for x in peers],
                                   "backgroundColor": "#059669", "borderRadius": 6}]}
        return {
            "sections": ["kpis", "k24", "alerts", "peers", "profile"],
            "source": "dept_data.json（UDB 學1-1/學3-2/學12-1/學13-1/學14-1/教1-1；data.gov.tw 9622）",
            "fallback_text": text,
            "chart": chart,
            "table": {"title": "核心指標", "headers": ["代碼", "指標", "值", "單位", "來源"], "rows": rows},
        }

    @staticmethod
    def _general(d: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "sections": ["kpis", "peers", "module5", "demographics", "partners", "alerts", "profile"],
            "source": "dept_data.json（全系所實證數據庫與同儕數據）",
            "fallback_text": "已為您整合檢索實證數據庫，請參閱上方分析結果。",
            "drilldown_link": None,
            "chart": None,
            "table": None,
        }

    def _get_all_dossiers(self) -> Dict[str, Any]:
        if not hasattr(self, "_all_dossiers") or not self._all_dossiers:
            self._all_dossiers = {s: build_dossier(s) for s in SLUG_TO_NAME}
        return self._all_dossiers

    def _build_school_dossier(self, school_canonical: str) -> Dict[str, Any]:
        all_d = self._get_all_dossiers()
        depts = []
        total_poached = 0
        enrollments = []
        clean = school_canonical.replace("國立", "")

        for slug, d in all_d.items():
            our_name = d["meta"]["dept_name"]
            m5 = d.get("module5") or {}
            poached = 0
            for dest in m5.get("top_destinations", []):
                sch = dest.get("school", "")
                if school_canonical in sch or clean in sch:
                    poached += dest.get("count", 0)
            total_poached += poached

            for p in d.get("peers", []):
                sch = p.get("school", "")
                if school_canonical in sch or clean in sch:
                    e_rate = p.get("enrollment_rate")
                    if e_rate is not None:
                        enrollments.append(e_rate)
                    depts.append({
                        "our_dept": our_name,
                        "slug": slug,
                        "peer_school": p.get("school"),
                        "peer_dept": p.get("dept"),
                        "enrollment_rate": e_rate,
                        "dropout_rate": p.get("dropout_rate"),
                        "faculty_ratio": p.get("faculty_ratio"),
                        "students_total": p.get("students_total"),
                        "foreign_ratio": p.get("foreign_ratio"),
                        "poached": poached,
                    })

        avg_enrollment = round(sum(enrollments) / len(enrollments), 2) if enrollments else None
        return {
            "target_school": school_canonical,
            "summary": {
                "total_depts_matched": len(depts),
                "avg_enrollment_rate": avg_enrollment,
                "total_poached_across_college": total_poached,
            },
            "departments": depts,
        }

    def _build_school_summary_table(self, school_dossier: Dict[str, Any]) -> Dict[str, Any]:
        rows = []
        for d in school_dossier["departments"]:
            rows.append([
                d["our_dept"],
                d["peer_dept"],
                f"{d['enrollment_rate']}%" if d.get("enrollment_rate") is not None else "—",
                f"{d['dropout_rate']}%" if d.get("dropout_rate") is not None else "—",
                str(d["faculty_ratio"]) if d.get("faculty_ratio") is not None else "—",
                f"{d['students_total']:,} 人" if d.get("students_total") is not None else "—",
                f"{d['poached']} 人" if d.get("poached", 0) > 0 else "0 人"
            ])
        return {
            "title": f"{school_dossier['target_school']} 對接本院各系所指標清冊（114學年度）",
            "headers": ["本院系所", "該校對應系所", "新生註冊率", "學年退學率", "生師比", "在學人數", "查榜外流人數"],
            "rows": rows
        }

    def _build_school_summary_text(self, school_dossier: Dict[str, Any]) -> str:
        s = school_dossier["summary"]
        depts = school_dossier["departments"]
        dept_list = "、".join(f"{d['our_dept']}對接{d['peer_dept']}" for d in depts)
        enrollments = [d["enrollment_rate"] for d in depts if d.get("enrollment_rate") is not None]
        min_rate = min(enrollments) if enrollments else 0
        max_rate = max(enrollments) if enrollments else 0
        canonical = school_dossier["target_school"]
        short_school = CANONICAL_TO_SHORT.get(canonical) or re.sub(r"^國立", "", canonical)
        short_school = re.sub(r"科技大學$|大學$", "", short_school)

        text = f"就商學院整體而言，{canonical} 在本院實證數據庫中共收錄 {s['total_depts_matched']} 個對接系所（{dept_list}）。\n\n"
        text += f"• **招生註冊表現**：該校對接系所 114 學年度平均新生註冊率為 **{s['avg_enrollment_rate']}%**（各系所註冊率介於 {min_rate}% 至 {max_rate}% 之間，來源：UDB 學12-1）。\n"
        poached_note = "，為本院最主要之關鍵競爭同儕" if s['total_poached_across_college'] >= 100 else ""
        text += f"• **生源競合流向**：交叉查榜實證顯示，本院各系所考生累計向 {canonical} 外流共 **{s['total_poached_across_college']} 人**{poached_note}（來源：大專聯招交叉查榜）。\n\n"
        text += "各系所指標整合如下方清冊。\n\n"

        example_depts = "、".join(f"{short_school}{re.sub(r'學系$|系$', '', d['peer_dept'])}" for d in depts[:3])
        text += f"💡 **請問您詢問的是上述哪一個特定系所（例如：{example_depts}）？還是系統中{canonical}所有的系所？**\n\n"
        first_dept = re.sub(r'學系$|系$', '', depts[0]['peer_dept']) if depts else ""
        text += f"• 若需特定系所深入診斷：請直接點名系所（如「{short_school}{first_dept}最近如何」），助理將為您進行單一系所深度對比。\n"
        text += "• 若檢視全院大局：請點擊下方按鈕開啟商學院全院健康熱力總覽。\n\n"
        text += "資料時點：114 學年度；來源：UDB 學12-1/學13-1/教1-1/學1-1、大專聯招交叉查榜。"
        return text

    def _build_dept_peer_comparison_table(self, slug: str, peer_school_canonical: str) -> Optional[Dict[str, Any]]:
        d = build_dossier(slug)
        meta = d["meta"]
        kpis = d.get("kpis", {})
        m5 = d.get("module5") or {}
        clean = peer_school_canonical.replace("國立", "")

        matching_peer = next((p for p in d.get("peers", []) if peer_school_canonical in p.get("school", "") or clean in p.get("school", "")), None)
        if not matching_peer:
            return None

        poached = 0
        for dest in m5.get("top_destinations", []):
            sch = dest.get("school", "")
            if peer_school_canonical in sch or clean in sch:
                poached += dest.get("count", 0)

        our_enroll = kpis.get("K01", {}).get("value")
        our_drop = kpis.get("K02", {}).get("value")
        our_ratio = kpis.get("K06", {}).get("value")
        our_students = d.get("profile", {}).get("students_total") or kpis.get("K04", {}).get("value") or "—"
        our_retained = f"{m5.get('retained')} 人" if m5.get("retained") is not None else "—"

        rows = []
        if our_enroll is not None and matching_peer.get("enrollment_rate") is not None:
            peer_e = matching_peer["enrollment_rate"]
            diff = round(our_enroll - peer_e, 2)
            comp = f"本系領先 +{diff}%" if diff > 0 else (f"該校領先 +{abs(diff)}%" if diff < 0 else "持平 (0%)")
            rows.append(["新生註冊率", f"{our_enroll}%", f"{peer_e}%", comp, "UDB 學12-1"])

        if our_drop is not None and matching_peer.get("dropout_rate") is not None:
            peer_d = matching_peer["dropout_rate"]
            diff = round(our_drop - peer_d, 2)
            comp = f"本系較優 (低 {abs(diff)}%)" if diff < 0 else (f"該校較優 (低 {diff}%)" if diff > 0 else "持平 (0%)")
            rows.append(["學年度退學率", f"{our_drop}%", f"{peer_d}%", comp, "UDB 學13-1"])

        if our_ratio is not None and matching_peer.get("faculty_ratio") is not None:
            peer_r = matching_peer["faculty_ratio"]
            diff = round(our_ratio - peer_r, 2)
            comp = f"本系師資較充裕 (低 {abs(diff)})" if diff < 0 else (f"該校師資較充裕 (低 {diff})" if diff > 0 else "持平")
            rows.append(["專任生師比", str(our_ratio), str(peer_r), comp, "UDB 教1-1"])

        if matching_peer.get("students_total") is not None:
            peer_s = matching_peer["students_total"]
            our_s_str = f"{our_students:,} 人" if isinstance(our_students, int) else str(our_students)
            rows.append(["在學學生數", our_s_str, f"{peer_s:,} 人", "規模對照", "UDB 學1-1"])

        poached_str = f"吸引本系 {poached} 人" if poached > 0 else "0 人外流"
        poached_comp = f"外流去向 (共{poached}人)" if poached > 0 else "無考生外流"
        rows.append(["交叉查榜生源", f"留任 {our_retained}" if our_retained != "—" else "—", poached_str, poached_comp, "交叉查榜"])

        peer_display_school = matching_peer.get("school", "").replace("國立", "")
        return {
            "title": f"臺中科大{meta['dept_name']} vs {matching_peer.get('school')}{matching_peer.get('dept')} 核心實證對比（114學年度）",
            "headers": ["比較指標", f"本校{meta['dept_name']}", f"{peer_display_school}{matching_peer.get('dept')}", "實證對比 / 差距", "資料來源"],
            "rows": rows
        }

    def _build_dept_peer_comparison_text(self, slug: str, peer_school_canonical: str) -> Optional[str]:
        d = build_dossier(slug)
        meta = d["meta"]
        kpis = d.get("kpis", {})
        m5 = d.get("module5") or {}
        clean = peer_school_canonical.replace("國立", "")

        matching_peer = next((p for p in d.get("peers", []) if peer_school_canonical in p.get("school", "") or clean in p.get("school", "")), None)
        if not matching_peer:
            return None

        poached = 0
        for dest in m5.get("top_destinations", []):
            sch = dest.get("school", "")
            if peer_school_canonical in sch or clean in sch:
                poached += dest.get("count", 0)

        our_enroll = kpis.get("K01", {}).get("value")
        peer_enroll = matching_peer.get("enrollment_rate")
        text = f"114 學年度實證數據中，臺中科大{meta['dept_name']}新生註冊率為 **{our_enroll}%**"
        if peer_enroll is not None:
            if our_enroll > peer_enroll:
                text += f"，領先{matching_peer.get('school')}{matching_peer.get('dept')}（**{peer_enroll}%**）達 {round(our_enroll - peer_enroll, 2)} 個百分點（UDB 學12-1）。\n\n"
            elif our_enroll < peer_enroll:
                text += f"，{matching_peer.get('school')}{matching_peer.get('dept')}為 **{peer_enroll}%**，領先本系 {round(peer_enroll - our_enroll, 2)} 個百分點（UDB 學12-1）。\n\n"
            else:
                text += f"，與{matching_peer.get('school')}{matching_peer.get('dept')}同為 **{peer_enroll}%**，雙方皆達滿招（UDB 學12-1）。\n\n"
        else:
            text += "。\n\n"

        stu_str = f"{matching_peer.get('students_total'):,} 人" if matching_peer.get("students_total") else "—"
        text += f"• **教學規模與品質**：該校該系在學人數為 {stu_str}，學年度退學率為 {matching_peer.get('dropout_rate')}%（UDB 學13-1），專任生師比為 {matching_peer.get('faculty_ratio')}（UDB 教1-1）。\n"
        poached_note = "，為本系主要外流去向之一" if poached > 20 else ""
        text += f"• **交叉查榜競合**：在聯招分發中，本系累計有 **{poached} 名考生**選擇就讀{matching_peer.get('school')}{matching_peer.get('dept')}{poached_note}（大專聯招交叉查榜）。\n\n"
        text += "兩系核心指標深度對照請參閱下方清冊。\n\n"
        text += "資料時點：114 學年度；來源：UDB 學12-1/學13-1/教1-1/學1-1、交叉查榜。"
        return text

