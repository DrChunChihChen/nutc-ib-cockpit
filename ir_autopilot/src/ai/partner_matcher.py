"""
PartnerMatcher（相容層）：候選廠商清單已移入 output/{slug}/dept_data.json 的 partners 欄位，
商工登記核對結果由 gcis_client.verify_partners() 寫入 output/{slug}/partners_verified.json。
"""
from ir_autopilot.src.ai.dossier import build_dossier, DEPT_ALIASES, SLUG_TO_NAME


class PartnerMatcher:
    def match_partners_for_department(self, dept_name: str):
        slug = next((s for n, s in SLUG_TO_NAME.items() if n == dept_name), None)
        if slug is None:
            for alias, s in DEPT_ALIASES.items():
                if alias in dept_name:
                    slug = s
                    break
        return build_dossier(slug or "ib").get("partners", {})
