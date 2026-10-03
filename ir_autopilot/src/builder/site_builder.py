"""
Site Builder: 全自動靜態戰情室生成器
整合各計算引擎數據，透過 Jinja2 模板動態渲染產出符合 Impeccable 規範之 HTML 決策戰情室
"""

import os
import json
from jinja2 import Environment, FileSystemLoader
from ir_autopilot.src.collectors.udb_collector import UDBCollector
from ir_autopilot.src.engines.peer_engine import PeerEngine
from ir_autopilot.src.engines.demographic_engine import DemographicEngine
from ir_autopilot.src.engines.kpi_engine import KPIEngine
from ir_autopilot.src.engines.rule_engine import RuleEngine
from ir_autopilot.src.ai.partner_matcher import PartnerMatcher

class SiteBuilder:
    def __init__(self, templates_dir: str = "ir_autopilot/templates"):
        self.env = Environment(loader=FileSystemLoader(templates_dir))
        self.udb_collector = UDBCollector()
        self.peer_engine = PeerEngine(self.udb_collector)
        self.demo_engine = DemographicEngine()
        self.kpi_engine = KPIEngine()
        self.rule_engine = RuleEngine()
        self.partner_matcher = PartnerMatcher()

    def build_department_site(self, school_name: str, dept_name: str, dept_code: str = "", output_dir: str = "dist") -> Dict[str, str]:
        """
        為單一系所編譯出完整獨立的決策戰情室 (index.html + sources.html)
        """
        os.makedirs(output_dir, exist_ok=True)

        # 1. 採集基礎 UDB Profile
        profile = self.udb_collector.get_department_udb_profile(school_name, dept_name, dept_code)
        if not dept_code:
            dept_code = profile.get("dept_code", "04141020")

        # 2. 執行同儕匹配
        peers_data = self.peer_engine.get_peer_comparison(school_name, dept_name, dept_code)

        # 3. 執行少子化 16 年推估
        demo_data = self.demo_engine.simulate_department(
            current_capacity=profile.get("freshmen_capacity", 118),
            current_registered=profile.get("freshmen_registered", 117)
        )

        # 4. 計算 24 項 KPI 字典
        kpis = self.kpi_engine.compute_all_kpis(profile, peers_data, demo_data)

        # 5. 評估異常警報
        alerts = self.rule_engine.evaluate_rules(kpis, profile)

        # 6. 媒合產學廠商聚落
        partners = self.partner_matcher.match_partners_for_department(dept_name)

        # 7. 組裝渲染 Context
        context = {
            "school_name": school_name,
            "dept_name": dept_name,
            "dept_code": dept_code,
            "profile": profile,
            "peers": peers_data,
            "demo": demo_data,
            "kpis": kpis,
            "alerts": alerts,
            "partners": partners
        }

        # 8. 渲染主戰情室 (cockpit.html.j2 -> index.html)
        cockpit_tmpl = self.env.get_template("cockpit.html.j2")
        cockpit_html = cockpit_tmpl.render(context)
        index_path = os.path.join(output_dir, "index.html")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(cockpit_html)

        # 9. 渲染憑證查核頁 (sources.html.j2 -> sources.html)
        sources_tmpl = self.env.get_template("sources.html.j2")
        sources_html = sources_tmpl.render(context)
        sources_path = os.path.join(output_dir, "sources.html")
        with open(sources_path, "w", encoding="utf-8") as f:
            f.write(sources_html)

        # 10. 匯出 Gold context JSON (供 API 或離線審核)
        data_json_path = os.path.join(output_dir, "dept_data.json")
        with open(data_json_path, "w", encoding="utf-8") as f:
            json.dump(context, f, ensure_ascii=False, indent=2)

        return {
            "index_path": index_path,
            "sources_path": sources_path,
            "data_json_path": data_json_path
        }
