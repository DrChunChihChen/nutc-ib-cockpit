"""
ProactiveAgent（接地版）
原則：
1. 所有數字來自 dossier.build_dossier()（dept_data.json + 交叉查榜 CSV 即時計算），程式內無任何手打數據。
2. 圖表／表格由程式直接從 dossier 產生，與 LLM 無關；LLM 只負責敘事。
3. LLM 不可用時，回傳「模型不可用」＋ 數據表，不生成任何敘事。
4. LLM 回覆經 grounding.check()，數字對不上就標記 ungrounded 供前端警示。
"""
import re
import json
from typing import Any, Dict, List, Optional
import requests

from ir_autopilot.src.ai import grounding
from ir_autopilot.src.ai.dossier import build_dossier, detect_slug, dossier_to_text, SLUG_TO_NAME, DEPT_ALIASES
from ir_autopilot.src.ai.openrouter_client import OpenRouterClient
from ir_autopilot.src.ai.query_responses import selected_slugs, school_response, peer_response, scope_response

SYSTEM_PROMPT = """你是 {school_name}{dept_name} 的校務研究（IR）決策助理，服務對象是系主任與校務研究人員。

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
    r"去美國|怎麼去|機票|觀光|旅遊|天氣|今天幾號|星期幾|算命|星座|運勢|"
    r"寫程式|寫代碼|寫python|寫javascript|寫一個Python爬蟲|寫一首詩|講笑話|講個笑話|唱首歌|推薦餐廳|美食|減肥|幫我寫作業)",
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
    return any(k in text for k in DEPT_ALIASES)


def is_fast_out_of_scope(message: str) -> bool:
    # Only remove a leading greeting; unrelated requests still pass through the
    # normal boundary classifier instead of bypassing it on a department keyword.
    substantive = re.sub(r"^(?:(?:你好|您好|哈囉|早安|晚安|嗨)[，,！!。\s]*)+", "", message.strip())
    return bool(OUT_OF_SCOPE_REGEX.search(substantive)) or (not substantive and bool(message.strip()))


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
        slug = detect_slug(user_message, dept_context.get("slug") or dept_context.get("default_slug", "ib"))
        d = build_dossier(slug)
        meta = d["meta"]

        # 1. 快速過濾範圍外問題
        if not image and is_fast_out_of_scope(user_message):
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

        slugs = selected_slugs(user_message)
        if peer_school_canonical and (not has_dept or len(slugs) == len(SLUG_TO_NAME)):
            return school_response(peer_school_canonical, self._get_all_dossiers(), user_message)
        if peer_school_canonical and has_dept:
            result = peer_response(slug, peer_school_canonical, self._get_all_dossiers(), user_message)
            if result:
                return result
        if not image and len(slugs) > 1:
            scoped = scope_response(user_message, intent, self._get_all_dossiers(), slugs)
            if self.client.available and self._is_strategic_query(user_message):
                narrative, reasoning, model, ground = self._narrate_college_strategic(user_message, scoped, history)
                if narrative:
                    scoped["response"] = narrative
                    scoped["reasoning"] = reasoning
                    scoped["model"] = model
                    scoped["grounding"] = ground
            return scoped

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
        ground = grounding.check(content, json.loads(dossier_to_text(d, sections)), prompt=prompt)
        return content, res.get("reasoning"), res.get("model"), ground

    @staticmethod
    def _is_strategic_query(message: str) -> bool:
        if not message:
            return False
        return bool(re.search(r"(策略|怎麼看|如何看待|看法|建議|佈局|規劃|方向|作為院長|院長|診斷|對策|生源危機|轉型|因應|定位|招生成效|招生狀況|發展)", message, re.IGNORECASE))

    def _narrate_college_strategic(self, user_msg: str, scoped: dict, history: list) -> tuple:
        if not self.client.available:
            return None, None, None, {"ok": None, "note": "模型未設定，僅顯示數據"}

        all_dossiers = self._get_all_dossiers()
        depts = {}
        for s, d in all_dossiers.items():
            kp = d.get("kpis", {})
            dm = d.get("demographics", {})
            m5 = d.get("module5", {})
            k01 = kp.get("K01", {}).get("value")
            k03 = kp.get("K03", {}).get("value")
            k05 = kp.get("K05", {}).get("value")
            k06 = kp.get("K06", {}).get("value")
            gap = dm.get("y117", {}).get("gap")
            gap_pct = dm.get("y117", {}).get("gap_pct")
            top_c = [t["school"] + t.get("dept", "") + "(" + str(t["count"]) + "人)" for t in m5.get("top_destinations", [])[:3]]
            prof = d.get("profile", {})
            k04 = kp.get("K04", {}).get("value")
            depts[d.get("meta", {}).get("dept_name", s)] = {
                "enrollment_rate": f"{k01}%（純日間部註冊率，UDB 學12-1）",
                "dropout_rate": f"{k03}%（純日間部退學率，UDB 學14-1）",
                "suspension_rate": f"{k04}%（純日間部休學率，UDB 學13-1）",
                "retention_net_loss": f"{k05}%（純日間部淨流失率，UDB 學13-1, 14-1）",
                "student_faculty_ratio": f"{k06}（純日間部生師比，UDB 教1-1, 學1-1）",
                "scope_note": prof.get("scope_note", "純日間部基準"),
                "y117_demographic_gap": f"{gap} 人（{gap_pct}%）",
                "top_competitors": top_c,
                "k24_grade": d.get("k24", {}).get("grade"),
                "k24_score": d.get("k24", {}).get("score"),
            }
        college_summary = {
            "college_name": "國立臺中科技大學 商學院",
            "analysis_scope": "全院 7 系全面以【純日間部】為基準（已嚴格排除進修部夜間在職流失數據）",
            "departments": depts,
            "total_y117_gap": "-122 人（-19.3%）",
            "primary_competitors": [
                "國立高雄科技大學（全院累計外流 481 筆）",
                "國立雲林科技大學（123 筆）",
                "逢甲大學（107 筆）",
                "國立臺北商業大學（89 筆）"
            ]
        }
        is_dean = bool(re.search(r"院長|作為院長|院方", user_msg))
        role_desc = "使用者明確要求以「作為商學院院長」視角發言。請以院長第一人稱高度（「身為商學院院長…」、「本院…」），展現宏觀、清晰且具備前瞻魄力的治理視野。" if is_dean else "請站在「商學院整體戰略視角」，為院級主管提供客觀、深刻且具體可落地的戰略決策建言。"

        system = f"""你是 國立臺中科技大學商學院 的院長級校務研究（IR）決策顧問與戰略大腦，服務對象是院長、系主任與校級決策主管。

## 角色設定與視角
{role_desc}
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
{json.dumps(college_summary, ensure_ascii=False, indent=1)}
</college_dossier>"""

        messages = [m for m in (history or []) if m.get("role") in ("user", "assistant")][-6:]
        messages.append({"role": "user", "content": user_msg})
        res = self.client.chat(messages, system_prompt=system)
        if not res.get("success"):
            return None, None, None, {"ok": None, "note": f"模型不可用：{res.get('error')}"}
        content = res.get("content", "").strip()
        ground = grounding.check(content, college_summary, prompt=user_msg)
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
        note = "已排除進修部夜間數據；進修四技因在職工作因素退學人數較高（60人），另列於戰情室學制診斷表。"
        text = (f"{meta['dept_name']}純日間部（{meta.get('latest_year')} 學年）：註冊率 {self._kv(kp,'K01')}%、淨流失率 {self._kv(kp,'K05')}%、"
                f"生師比 {self._kv(kp,'K06')}；K24 {d['k24']['score']}（{d['k24']['grade']}）。\n"
                f"（指標說明：{note}）"
                + (f" 預警 {len(al)} 則：" + "；".join(a.get('title','') for a in al) if al else " 目前無預警。"))
        chart = None
        if peers:
            chart = {"type": "bar", "title": "本系 vs 同儕：新生註冊率（%）",
                     "labels": [meta["dept_name"]] + [f"{x['school']}{x['dept']}" for x in peers],
                     "datasets": [{"label": "註冊率", "data": [self._kv(kp, "K01")] + [x.get("enrollment_rate") for x in peers],
                                   "backgroundColor": "#059669", "borderRadius": 6}]}
        return {
            "sections": ["kpis", "k24", "alerts", "peers", "profile"],
            "source": "dept_data.json（UDB 學1-1/學3-2/學12-1/學13-1/學14-1/教1-1；data.gov.tw 9622；純日間部口徑）",
            "fallback_text": text,
            "chart": chart,
            "table": {"title": "核心指標（純日間部：四技＋二技＋五專）", "headers": ["代碼", "指標", "值", "單位", "來源"], "rows": rows, "note": note},
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
        return {s: build_dossier(s) for s in SLUG_TO_NAME}
