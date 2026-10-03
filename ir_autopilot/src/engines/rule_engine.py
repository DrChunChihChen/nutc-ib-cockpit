"""
Rule Engine: YAML 宣告式規則與異常預警引擎
"""

import os
import yaml
from typing import Dict, List, Any

class RuleEngine:
    def __init__(self, rules_path: str = "ir_autopilot/configs/alert_rules.yaml"):
        self.rules_config = {}
        if os.path.exists(rules_path):
            with open(rules_path, "r", encoding="utf-8") as f:
                self.rules_config = yaml.safe_load(f)

    def evaluate_rules(self, kpis: Dict[str, Any], raw_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        比對 KPI 門檻，產出觸發的異常警報事件集
        """
        alerts = []
        rules = self.rules_config.get("rules", [])

        k01 = kpis.get("K01", {}).get("value", 100.0)
        k02 = kpis.get("K02", {}).get("value", 0.0)
        k03 = kpis.get("K03", {}).get("value", 5.0)
        k05 = kpis.get("K05", {}).get("value", 10.0)
        k06 = kpis.get("K06", {}).get("value", 30.0)
        k07 = kpis.get("K07", {}).get("value", 1.0)
        k10 = kpis.get("K10", {}).get("value", 0.0)
        k19 = kpis.get("K19", {}).get("value", 0.0)

        # R01: 註冊率下滑
        if k02 < -1.5:
            alerts.append({
                "id": "R01",
                "severity": "high",
                "title": "新生註冊率連續下滑預警",
                "message": f"日間部新生註冊率近三年變化斜率為 {k02:+.2f} 百分點/年，呈下滑趨勢。",
                "action": "建議強化高中職端宣傳，檢討招生管道配額。"
            })

        # R02: 學生流失率偏高
        if k05 > 15.0:
            alerts.append({
                "id": "R02",
                "severity": "medium",
                "title": "學生在學淨流失率偏高",
                "message": f"本學年退學率與休學率總和（淨流失率）達 {k05:.2f}%，學生就學穩定度需關注。",
                "action": "檢視大一基礎必修門檻與學生自請休退學原因分析。"
            })

        # R03: 少子化 117 海嘯缺口
        if k19 < -15.0:
            alerts.append({
                "id": "R03",
                "severity": "high",
                "title": "117 虎年海嘯生源赤字警報",
                "message": f"推估至 117 虎年海嘯谷底，大專生源供給缺口達 {k19:.1f}%，招生將面臨嚴峻考驗。",
                "action": "提早啟動跨學制調節（擴增五專或在職碩士班名額，健全防禦護城河）。"
            })

        # R04: 生師比逼近警戒線
        if k06 > 35.0:
            alerts.append({
                "id": "R04",
                "severity": "medium",
                "title": "專任教師生師比逼近警戒上限",
                "message": f"專任生師比達 {k06:.1f}，超出優質教學建議之 32:1 門檻。",
                "action": "爭取增聘專任師資或適度調降核定招生總額。"
            })

        # 若無高危警報，提供穩定優勢提示
        if not alerts:
            alerts.append({
                "id": "R00",
                "severity": "info",
                "title": "各項核心校務指標運行穩健",
                "message": f"純日間部新生註冊率達 {k01:.1f}%，各項流失與生師比均在安全範圍內。",
                "action": "持續維護現有優勢學制，並積極拓展跨領域微學程。"
            })

        return alerts
