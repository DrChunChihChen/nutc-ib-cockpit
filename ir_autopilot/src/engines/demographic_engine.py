"""
Demographic Engine: 少子化 16 年 (113~128 學年度) 動態生源推估模型
基於內政部歷年出生統計與 18 年隊列推移 (Time-lagged Cohort Propagation)
"""

from typing import Dict, List, Any

# 內政部官方出生人數 (對應 113~128 學年度滿 18 歲大專生源)
# 85-110 年次出生人口 (單位：人)
BIRTH_COHORTS = {
    113: 205854,  # 民國 95 年次 (2006)
    114: 204414,  # 民國 96 年次 (2007)
    115: 198733,  # 民國 97 年次 (2008)
    116: 191310,  # 民國 98 年次 (2009)
    117: 166886,  # 民國 99 年次 (2010 虎年海嘯谷底)
    118: 196627,  # 民國 100 年次 (2011 兔年小反彈)
    119: 229481,  # 民國 101 年次 (2012 龍年高峰)
    120: 199113,  # 民國 102 年次 (2013)
    121: 210383,  # 民國 103 年次 (2014)
    122: 213598,  # 民國 104 年次 (2015)
    123: 208440,  # 民國 105 年次 (2016)
    124: 193844,  # 民國 106 年次 (2017)
    125: 181601,  # 民國 107 年次 (2018)
    126: 177767,  # 民國 108 年次 (2019)
    127: 165249,  # 民國 109 年次 (2020)
    128: 153820,  # 民國 110 年次 (2021 大斷崖)
}

class DemographicEngine:
    def __init__(self):
        pass

    def simulate_department(self, current_capacity: int, current_registered: int) -> Dict[str, Any]:
        """
        為系所執行 113~128 學年度 16 年生源壓力測試
        """
        if current_capacity <= 0:
            current_capacity = 100
        if current_registered <= 0:
            current_registered = current_capacity

        base_year = 113
        base_births = BIRTH_COHORTS[base_year]
        base_share = current_registered / base_births

        timeline = []
        for year in range(113, 129):
            births = BIRTH_COHORTS[year]
            cohort_ratio = births / base_births
            
            # 三情境推估
            est_baseline = round(current_registered * cohort_ratio)
            
            # 年減 2% 份額 (悲觀/區域邊緣化)
            decay_factor = (1.0 - 0.02) ** (year - base_year)
            est_severe = round(current_registered * cohort_ratio * decay_factor)
            
            # 年增 2% 份額 (積極/公立品牌集中)
            boost_factor = (1.0 + 0.02) ** (year - base_year)
            est_aggressive = round(current_registered * cohort_ratio * boost_factor)
            
            gap_baseline = est_baseline - current_capacity
            gap_pct = round((gap_baseline / current_capacity) * 100, 1)

            timeline.append({
                "year": year,
                "births": births,
                "cohort_ratio": round(cohort_ratio, 3),
                "est_baseline": est_baseline,
                "est_severe": est_severe,
                "est_aggressive": est_aggressive,
                "capacity": current_capacity,
                "gap": gap_baseline,
                "gap_pct": gap_pct
            })

        # 關鍵年份指標
        t117 = next(t for t in timeline if t["year"] == 117)
        t128 = next(t for t in timeline if t["year"] == 128)

        return {
            "base_capacity": current_capacity,
            "base_registered": current_registered,
            "timeline": timeline,
            "tiger_year_117": {
                "year": 117,
                "est_registered": t117["est_baseline"],
                "gap": t117["gap"],
                "gap_pct": t117["gap_pct"],
                "risk_level": "高風險" if t117["gap_pct"] < -15 else ("中風險" if t117["gap_pct"] < 0 else "低風險")
            },
            "cliff_year_128": {
                "year": 128,
                "est_registered": t128["est_baseline"],
                "gap": t128["gap"],
                "gap_pct": t128["gap_pct"],
                "risk_level": "高風險" if t128["gap_pct"] < -20 else "中風險"
            }
        }
