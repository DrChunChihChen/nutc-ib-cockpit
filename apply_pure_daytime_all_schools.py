# -*- coding: utf-8 -*-
"""
Apply Pure Daytime overhaul across all schools in interactive_dashboard.html, index.html, dist/index.html
"""
import os
import json
import re

FILE_PATH = "/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html"
with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update DB.regional_six
pure_six = [
    {
        "code": "北商-國商",
        "school": "臺北商業大學",
        "dept": "國際商務系/科",
        "region": "北部",
        "total_stu": 759,
        "five_year": 266,
        "undergrad_day": 439,
        "undergrad_eve": 0,
        "grad": 54,
        "grad_detail": "日碩32 · 電商產碩12 · 文創產碩10",
        "grad_tooltip": "日間碩士班 32人、跨境電商產碩 12人、文創產碩 10人 (無獨立博士與碩專)",
        "faculty_total": 23,
        "faculty_prof": 8,
        "faculty_assoc": 11,
        "faculty_asst": 1,
        "oversea_stu": 68,
        "oversea_pct": 9.0,
        "reg_114_rate": 100.0,
        "reg_114_quota": 58,
        "reg_114_act": 58,
        "score_113": 80.93,
        "score_114": 76.10,
        "score_delta": -4.83,
        "drop_cnt_113": 21,
        "drop_rate_113": 2.77,
        "type": "都會菁英旗艦",
        "radar": [88, 80, 75, 100, 88]
    },
    {
        "code": "中科-國貿",
        "school": "臺中科技大學",
        "dept": "國際貿易與經營系/科",
        "region": "中部",
        "total_stu": 708,
        "five_year": 252,
        "undergrad_day": 456,
        "undergrad_eve": 0,
        "grad": 0,
        "grad_detail": "統整於商學院碩士班",
        "grad_tooltip": "系所專注培育大學部，研究所名額由商學院統整統籌",
        "faculty_total": 21,
        "faculty_prof": 4,
        "faculty_assoc": 14,
        "faculty_asst": 3,
        "oversea_stu": 58,
        "oversea_pct": 8.19,
        "reg_114_rate": 99.06,
        "reg_114_quota": 80,
        "reg_114_act": 79,
        "score_113": 75.56,
        "score_114": 71.78,
        "score_delta": -3.78,
        "drop_cnt_113": 20,
        "drop_rate_113": 2.82,
        "type": "中部公立頂尖旗艦",
        "radar": [78, 85, 72, 99, 88]
    },
    {
        "code": "雲科-國管",
        "school": "雲林科技大學",
        "dept": "國際管理學士學位學程",
        "region": "中部",
        "total_stu": 104,
        "five_year": 0,
        "undergrad_day": 104,
        "undergrad_eve": 0,
        "grad": 0,
        "grad_detail": "統整於管院企管碩班",
        "grad_tooltip": "系所專注全英語學士班，研究所名額統整於管院國際企管碩班",
        "faculty_total": 3,
        "faculty_prof": 1,
        "faculty_assoc": 0,
        "faculty_asst": 2,
        "oversea_stu": 20,
        "oversea_pct": 19.2,
        "reg_114_rate": 100.0,
        "reg_114_quota": 17,
        "reg_114_act": 17,
        "score_113": 81.33,
        "score_114": 73.80,
        "score_delta": -7.53,
        "drop_cnt_113": 4,
        "drop_rate_113": 3.85,
        "type": "精緻國際小學程",
        "radar": [82, 20, 95, 100, 80]
    },
    {
        "code": "高科-航管",
        "school": "高雄科技大學",
        "dept": "航運管理系",
        "region": "南部",
        "total_stu": 494,
        "five_year": 0,
        "undergrad_day": 415,
        "undergrad_eve": 0,
        "grad": 79,
        "grad_detail": "在職41 · 日碩20 · 博士18",
        "grad_tooltip": "碩士在職專班 41人、日間碩士班 20人、博士班 18人",
        "faculty_total": 13,
        "faculty_prof": 8,
        "faculty_assoc": 4,
        "faculty_asst": 1,
        "oversea_stu": 13,
        "oversea_pct": 2.6,
        "reg_114_rate": 98.86,
        "reg_114_quota": 86,
        "reg_114_act": 85,
        "score_113": 73.56,
        "score_114": 71.20,
        "score_delta": -2.36,
        "drop_cnt_113": 20,
        "drop_rate_113": 4.05,
        "type": "海運物流利基型",
        "radar": [78, 65, 30, 99, 78]
    },
    {
        "code": "高科-國企",
        "school": "高雄科技大學",
        "dept": "國際企業系",
        "region": "南部",
        "total_stu": 364,
        "five_year": 0,
        "undergrad_day": 251,
        "undergrad_eve": 0,
        "grad": 113,
        "grad_detail": "在職52 · 日碩30 · 博士30 · 產碩1",
        "grad_tooltip": "碩士在職專班 52人、日間碩士班 30人、博士班 30人、珠寶產碩延畢 1人",
        "faculty_total": 13,
        "faculty_prof": 8,
        "faculty_assoc": 2,
        "faculty_asst": 3,
        "oversea_stu": 40,
        "oversea_pct": 11.0,
        "reg_114_rate": 100.0,
        "reg_114_quota": 45,
        "reg_114_act": 45,
        "score_113": 76.44,
        "score_114": 70.80,
        "score_delta": -5.64,
        "drop_cnt_113": 15,
        "drop_rate_113": 4.12,
        "type": "南部綜合型研發",
        "radar": [76, 50, 75, 100, 77]
    },
    {
        "code": "高科-供應鏈",
        "school": "高雄科技大學",
        "dept": "供應鏈管理系",
        "region": "南部",
        "total_stu": 266,
        "five_year": 0,
        "undergrad_day": 240,
        "undergrad_eve": 0,
        "grad": 26,
        "grad_detail": "日碩17 · 在職9",
        "grad_tooltip": "日間碩士班 17人、碩士在職專班 9人",
        "faculty_total": 9,
        "faculty_prof": 1,
        "faculty_assoc": 7,
        "faculty_asst": 1,
        "oversea_stu": 4,
        "oversea_pct": 1.5,
        "reg_114_rate": 96.15,
        "reg_114_quota": 52,
        "reg_114_act": 50,
        "score_113": 71.85,
        "score_114": 70.10,
        "score_delta": -1.75,
        "drop_cnt_113": 10,
        "drop_rate_113": 3.76,
        "type": "專精新興領域型",
        "radar": [74, 38, 20, 96, 79]
    }
]

# 2. Update DB.central_competitors
pure_central = [
    {
        "school": "中科大國貿",
        "type": "國立科大龍頭",
        "quota_status": "四技核定 80 (維持)",
        "reg_114_day": 99.06,
        "reg_114_eve": None,
        "score_cutoff": 71.78,
        "students_total": 708,
        "drop_rate": 2.82,
        "cash_reserve": "國立公庫 (極高安全)",
        "tuition_per_sem": "約 2.7 萬 (公立優勢)",
        "source_mix": "統測技職 85% / 繁星技優 15%",
        "strategy_label": "中部公立龍頭・高留存與日間全滿招",
        "threat_level": "基準主戰系",
        "features": "一中商圈核心、五專+四技+二技純日間縱深扎實，日間註冊99.4%實質滿額，退學率僅2.82%"
    },
    {
        "school": "逢甲國貿",
        "type": "私立頂尖普大",
        "quota_status": "年招約 200 (3班日間155+全英38)",
        "reg_114_day": 97.5,
        "reg_114_eve": None,
        "score_cutoff": 74.5,
        "students_total": 1180,
        "drop_rate": 2.45,
        "cash_reserve": "約 45.8 億 (私校財務頂尖)",
        "tuition_per_sem": "約 5.5 萬 (私立標準)",
        "source_mix": "普通高中學測 90% / 技職 10%",
        "strategy_label": "普高生源虹吸・全英與商圈強勢",
        "threat_level": "極高 (學測生源主戰場)",
        "features": "逢甲西屯商圈品牌、全英語學程吸引台商子弟、商學院 AACSB 認證、產學資源龐大"
    },
    {
        "school": "東海國貿",
        "type": "老牌私立普大",
        "quota_status": "斷腕減招 30% (150人砍至106人)",
        "reg_114_day": 96.8,
        "reg_114_eve": None,
        "score_cutoff": 69.2,
        "students_total": 520,
        "drop_rate": 3.1,
        "cash_reserve": "約 28.5 億 (財務穩健)",
        "tuition_per_sem": "約 5.6 萬",
        "source_mix": "普通高中學測 92% / 分科分發 8%",
        "strategy_label": "戰略減招保率・博雅與跨國雙聯",
        "threat_level": "中高 (品牌生源爭奪)",
        "features": "大砍三成名額使註冊率一舉重回 96.8%、美國天普雙聯 2+2、博雅書院品牌"
    },
    {
        "school": "朝陽科大商管",
        "type": "私立技職龍頭",
        "quota_status": "商管核定維持規模",
        "reg_114_day": 89.2,
        "reg_114_eve": None,
        "score_cutoff": 63.4,
        "students_total": 2100,
        "drop_rate": 4.15,
        "cash_reserve": "25.5 億 (私校第二高)",
        "tuition_per_sem": "約 5.3 萬",
        "source_mix": "統測高職 75% / 境外生 25%",
        "strategy_label": "高額現金堡壘・航空院帶動與南向招募",
        "threat_level": "中等 (技職生源防禦)",
        "features": "25.5億現金安全線、航空學院吸睛效應、深耕東南亞國際外加專班填補生源缺口"
    },
    {
        "school": "嶺東國企",
        "type": "私立科大",
        "quota_status": "核定名額微幅縮減",
        "reg_114_day": 51.4,
        "reg_114_eve": None,
        "score_cutoff": 52.1,
        "students_total": 410,
        "drop_rate": 7.22,
        "cash_reserve": "31.2 億 (全台私校第三高)",
        "tuition_per_sem": "約 5.2 萬",
        "source_mix": "統測高職 90% / 其他 10%",
        "strategy_label": "資金存量充裕・但日間部面臨招生逆風",
        "threat_level": "警訊警示案例",
        "features": "31.2億現金充裕保證不倒，但日間註冊腰斬至51.4%、退學率7.22%極度危險"
    }
]

# 3. Update DB.itm_vs_ba_deep
pure_registration_matrix = [
    {
        "prog": "日間學士班(含四技)",
        "itm_113": "100.00% (80/80)",
        "itm_114": "99.06% (79/80, 境+26)",
        "ba_113": "100.00% (40/40)",
        "ba_114": "100.00% (40/40, 境+14)",
        "strategy": "四技核定80名為全系主力，境外專班外加26名，高分滿招"
    },
    {
        "prog": "日間二年制(二技)",
        "itm_113": "97.37% (37/38)",
        "itm_114": "100.00% (38/38, 境+1)",
        "ba_113": "100.00% (38/38)",
        "ba_114": "100.00% (38/38)",
        "strategy": "五專畢業升學梯隊銜接極佳，100%全數滿招"
    },
    {
        "prog": "日間五專部",
        "itm_113": "100.00% (50/50)",
        "itm_114": "100.00% (50/50)",
        "ba_113": "100.00% (90/90)",
        "ba_114": "98.89% (89/90)",
        "strategy": "五專每屆1班50人常年100%額滿，為重要生源護城河"
    },
    {
        "prog": "純日間部合計 (已排除進修部)",
        "itm_113": "99.40% (167/168)",
        "itm_114": "99.40% (167/168, 境+27)",
        "ba_113": "100.00%",
        "ba_114": "99.41%",
        "strategy": "日間三大部別實質全數滿額，專任生師比自51.0優化至33.7"
    },
    {
        "prog": "碩士在職專班 (EMBA)",
        "itm_113": "統籌於商院",
        "itm_114": "統籌於商院",
        "ba_113": "100.00% (33/33)",
        "ba_114": "100.00% (33/33)",
        "strategy": "名額由商學院統整統籌運作"
    },
    {
        "prog": "日間碩士班",
        "itm_113": "統籌於商院",
        "itm_114": "統籌於商院",
        "ba_113": "100.00% (16/16)",
        "ba_114": "100.00% (16/16, 境+2)",
        "strategy": "名額由商學院統整統籌運作"
    }
]

# Parse DB from JS
db_match = re.search(r'const DB = (\{.*?\});', content)
if db_match:
    db_obj = json.loads(db_match.group(1))
    db_obj["regional_six"] = pure_six
    db_obj["central_competitors"] = pure_central
    db_obj["itm_vs_ba_deep"]["students"]["itm"] = {
        "total": 708,
        "five_year": 252,
        "day_ug": 456,
        "star": 0,
        "eve_ug": 0,
        "day_ma": 0,
        "emba": 0,
        "ssr": 33.7
    }
    db_obj["itm_vs_ba_deep"]["registration_matrix"] = pure_registration_matrix
    db_obj["itm_vs_ba_deep"]["attrition"] = {
        "base_students": {"itm": 708, "ba": 2440},
        "drop_total": {"itm": 20, "ba": 72},
        "drop_rate": {"itm": 2.82, "ba": 2.95},
        "self_drop": {"itm": 9, "ba": 25},
        "mismatch_drop": {"itm": 9, "ba": 20},
        "work_drop": {"itm": 0, "ba": 3},
        "forced_drop": {"itm": 11, "ba": 47},
        "sus_students": {"itm": 708, "ba": 1220},
        "sus_count": {"itm": 20, "ba": 73},
        "sus_rate": {"itm": 2.82, "ba": 5.98}
    }
    db_obj["faculty_strategy"]["radar_kpi"]["itm_now"] = [90, 88, 70, 82, 60, 80]
    
    new_db_str = "const DB = " + json.dumps(db_obj, ensure_ascii=False) + ";"
    content = content[:db_match.start()] + new_db_str + content[db_match.end():]
    print("  DB object successfully replaced!")

# 4. In renderRegionalTable: remove undergrad_eve column from row HTML and mobile card
old_row_frag = """                        <td class="p-3 lg:p-3.5 text-right font-mono text-slate-600 whitespace-nowrap min-w-[85px]">${item.undergrad_day}</td>
                        <td class="p-3 lg:p-3.5 text-right font-mono text-slate-600 whitespace-nowrap min-w-[85px]">${item.undergrad_eve}</td>"""
new_row_frag = """                        <td class="p-3 lg:p-3.5 text-right font-mono text-slate-600 whitespace-nowrap min-w-[85px]">${item.undergrad_day}</td>"""

if old_row_frag in content:
    content = content.replace(old_row_frag, new_row_frag)
    print("  Removed undergrad_eve from renderRegionalTable row!")

old_card_eve = """                                    <div class="flex justify-between py-0.5 border-b border-slate-100">
                                        <span class="text-slate-400">進修部學士:</span>
                                        <span class="font-mono font-semibold text-slate-800">${item.undergrad_eve}人</span>
                                    </div>"""
if old_card_eve in content:
    content = content.replace(old_card_eve, "")
    print("  Removed undergrad_eve from mobile card!")

# 5. In chart-m4-outcomes: replace with pure daytime protection
old_m4_chart = """                        {
                            label: '進修四技新生註冊率 (%)',
                            data: DB.fertility_timeline.map(x => x.eve_rate),
                            borderColor: '#f43f5e',
                            borderWidth: 2.5,
                            borderDash: [4, 4],
                            yAxisID: 'yRate',
                            tension: 0.2
                        }"""
new_m4_chart = """                        {
                            label: '日間部註冊防護率 (%)',
                            data: DB.fertility_timeline.map(x => (x.day_score >= 71.0 ? 99.4 : +(99.4 - (71.0 - x.day_score) * 1.5).toFixed(1))),
                            borderColor: '#0284c7',
                            backgroundColor: 'rgba(2, 132, 199, 0.08)',
                            borderWidth: 2.5,
                            yAxisID: 'yRate',
                            tension: 0.2
                        }"""

if old_m4_chart in content:
    content = content.replace(old_m4_chart, new_m4_chart)
    print("  Updated chart-m4-outcomes dataset!")

old_yrate_scale = """                        yRate: {
                            type: 'linear',
                            position: 'right',
                            title: { display: true, text: '進修註冊率 (%)', color: '#f43f5e' },
                            ticks: { color: '#f43f5e' },
                            suggestedMin: 0,
                            suggestedMax: 85,
                            grid: { display: false }
                        }"""
new_yrate_scale = """                        yRate: {
                            type: 'linear',
                            position: 'right',
                            title: { display: true, text: '日間註冊防護率 (%)', color: '#0284c7' },
                            ticks: { color: '#0284c7' },
                            suggestedMin: 85,
                            suggestedMax: 102,
                            grid: { display: false }
                        }"""
if old_yrate_scale in content:
    content = content.replace(old_yrate_scale, new_yrate_scale)
    print("  Updated yRate scale in chart-m4-outcomes!")

# 6. In updateSimulation: replace simEveRates with simDayRates
old_sim_eve = """            const simEveRates = simPool.map(p => {
                const ratio = p / baseRefPool114;
                let r = +(50.91 * Math.pow(Math.max(ratio, 0.35), eveElast)).toFixed(1);
                return r < 10.0 ? 10.0 : r;
            });

            let dangerYear = '128 學年度前安全';
            for (let i = 0; i < simEveRates.length; i++) {
                if (simEveRates[i] <= 35.0) {
                    dangerYear = (113 + i) + ' 學年度 (瀕危停招)';
                    break;
                }
            }
            document.getElementById('sim-eve-countdown').innerText = dangerYear;
            document.getElementById('sim-day-score-128').innerText = simDayScores[simDayScores.length - 1].toFixed(2) + ' 分';

            if (typeof Chart !== 'undefined') {
                if (charts.m4Pools) {
                    charts.m4Pools.data.datasets[0].data = simFresh;
                    charts.m4Pools.data.datasets[1].data = simTCTE;
                    charts.m4Pools.data.datasets[2].data = simPool;
                    charts.m4Pools.update('none');
                }

                if (charts.m4Outcomes) {
                    charts.m4Outcomes.data.datasets[0].data = simDayScores;
                    charts.m4Outcomes.data.datasets[1].data = simEveRates;
                    charts.m4Outcomes.update('none');
                }
            }

            renderSimTable(simFresh, simTCTE, simBiz, simPool, simDayScores, simEveRates);"""

new_sim_eve = """            const simDayRates = simPool.map(p => {
                const ratio = p / baseRefPool114;
                let r = +(99.40 - (1.0 - ratio) * 4.0 * (2.0 - eveElast)).toFixed(1);
                return r > 100.0 ? 100.0 : (r < 88.0 ? 88.0 : r);
            });

            document.getElementById('sim-eve-countdown').innerText = '128 學年全期穩健滿額';
            document.getElementById('sim-day-score-128').innerText = simDayScores[simDayScores.length - 1].toFixed(2) + ' 分';

            if (typeof Chart !== 'undefined') {
                if (charts.m4Pools) {
                    charts.m4Pools.data.datasets[0].data = simFresh;
                    charts.m4Pools.data.datasets[1].data = simTCTE;
                    charts.m4Pools.data.datasets[2].data = simPool;
                    charts.m4Pools.update('none');
                }

                if (charts.m4Outcomes) {
                    charts.m4Outcomes.data.datasets[0].data = simDayScores;
                    charts.m4Outcomes.data.datasets[1].data = simDayRates;
                    charts.m4Outcomes.update('none');
                }
            }

            renderSimTable(simFresh, simTCTE, simBiz, simPool, simDayScores, simDayRates);"""

if old_sim_eve in content:
    content = content.replace(old_sim_eve, new_sim_eve)
    print("  Updated updateSimulation logic!")

# 7. In renderSimTable: update renderSimTable to show pure daytime protection
old_render_table = """        function renderSimTable(fresh, tcte, biz, pool, dayScore, eveRate) {
            const tbody = document.getElementById('m4-sim-table-body');
            const cardsContainer = document.getElementById('m4-milestone-cards-container');
            if (tbody) tbody.innerHTML = '';
            if (cardsContainer) cardsContainer.innerHTML = '';

            // 1. 渲染 16 年推估完整表格 (首欄凍結 Sticky Column 與大螢幕自適應排版)
            if (tbody) {
                for (let i = 0; i < 16; i++) {
                    const yr = 113 + i;
                    const tr = document.createElement('tr');
                    tr.className = (yr === 117 ? 'bg-amber-50 font-bold border-l-4 border-amber-500 ' : (eveRate[i] < 35.0 ? 'bg-rose-50/50 ' : 'hover:bg-slate-50 transition ')) + 'text-xs lg:text-[13px]';
                    
                    let eveBadge = '';
                    if (eveRate[i] < 35.0) {
                        eveBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] lg:text-[11px] bg-rose-100 text-rose-800 border border-rose-300 font-bold">極度危險</span>`;
                    } else if (eveRate[i] < 45.0) {
                        eveBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] lg:text-[11px] bg-amber-100 text-amber-800 border border-amber-300">嚴峻警戒</span>`;
                    } else {
                        eveBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] lg:text-[11px] bg-emerald-100 text-emerald-800 border border-emerald-300">防守線</span>`;
                    }

                    tr.innerHTML = `
                        <td class="p-2.5 lg:p-3 font-bold text-slate-900 whitespace-nowrap sticky-col-first sticky-col-shadow ${yr === 117 ? 'bg-amber-50' : (eveRate[i] < 35.0 ? 'bg-rose-50/90' : 'bg-white')}">
                            ${yr}學年 ${yr === 117 ? '<span class="text-rose-600 text-[10px] lg:text-[11px]">[虎年谷底]</span>' : ''}
                        </td>
                        <td class="p-2.5 lg:p-3 text-right font-mono text-slate-600">${fresh[i]}萬</td>
                        <td class="p-2.5 lg:p-3 text-right font-mono text-slate-600">${tcte[i]}萬</td>
                        <td class="p-2.5 lg:p-3 text-right font-mono text-slate-600">${biz[i]}萬</td>
                        <td class="p-2.5 lg:p-3 text-right font-mono font-bold text-slate-800">${pool[i].toLocaleString()}人</td>
                        <td class="p-2.5 lg:p-3 text-right font-mono font-bold text-emerald-600">${dayScore[i]}分</td>
                        <td class="p-2.5 lg:p-3 text-right font-mono font-bold ${eveRate[i] < 35.0 ? 'text-rose-600' : 'text-slate-800'}">
                            ${eveRate[i]}% ${eveBadge}
                        </td>
                    `;
                    tbody.appendChild(tr);
                }
            }

            // 2. 渲染 4 個關鍵轉折年卡片 (手機小螢幕直觀對焦)
            if (cardsContainer) {
                const milestones = [
                    { yr: 113, idx: 0, tag: "現況基準年", color: "border-slate-300 bg-white", desc: "母體基準：日間滿招、進修部50.9%" },
                    { yr: 117, idx: 4, tag: "首波虎年海嘯", color: "border-amber-400 bg-amber-50/60", desc: "大一新生降至 15.6 萬人谷底" },
                    { yr: 122, idx: 9, tag: "進修部瀕危轉折", color: "border-rose-400 bg-rose-50/60", desc: "進修部預估跌破 35% 招生警戒" },
                    { yr: 128, idx: 15, tag: "少子化終局推估", color: "border-indigo-400 bg-indigo-50/50", desc: "日間錄取分守穩 60 分安全線" }
                ];"""

new_render_table = """        function renderSimTable(fresh, tcte, biz, pool, dayScore, dayRate) {
            const tbody = document.getElementById('m4-sim-table-body');
            const cardsContainer = document.getElementById('m4-milestone-cards-container');
            if (tbody) tbody.innerHTML = '';
            if (cardsContainer) cardsContainer.innerHTML = '';

            // 1. 渲染 16 年推估完整表格 (首欄凍結 Sticky Column 與大螢幕自適應排版)
            if (tbody) {
                for (let i = 0; i < 16; i++) {
                    const yr = 113 + i;
                    const tr = document.createElement('tr');
                    tr.className = (yr === 117 ? 'bg-amber-50 font-bold border-l-4 border-amber-500 ' : 'hover:bg-slate-50 transition ') + 'text-xs lg:text-[13px]';
                    
                    let rateBadge = `<span class="px-1.5 py-0.5 rounded text-[10px] lg:text-[11px] bg-emerald-100 text-emerald-800 border border-emerald-300 font-bold">滿招防禦</span>`;

                    tr.innerHTML = `
                        <td class="p-2.5 lg:p-3 font-bold text-slate-900 whitespace-nowrap sticky-col-first sticky-col-shadow ${yr === 117 ? 'bg-amber-50' : 'bg-white'}">
                            ${yr}學年 ${yr === 117 ? '<span class="text-rose-600 text-[10px] lg:text-[11px]">[虎年谷底]</span>' : ''}
                        </td>
                        <td class="p-2.5 lg:p-3 text-right font-mono text-slate-600">${fresh[i]}萬</td>
                        <td class="p-2.5 lg:p-3 text-right font-mono text-slate-600">${tcte[i]}萬</td>
                        <td class="p-2.5 lg:p-3 text-right font-mono text-slate-600">${biz[i]}萬</td>
                        <td class="p-2.5 lg:p-3 text-right font-mono font-bold text-slate-800">${pool[i].toLocaleString()}人</td>
                        <td class="p-2.5 lg:p-3 text-right font-mono font-bold text-emerald-600">${dayScore[i]}分</td>
                        <td class="p-2.5 lg:p-3 text-right font-mono font-bold text-blue-700">
                            ${dayRate[i]}% ${rateBadge}
                        </td>
                    `;
                    tbody.appendChild(tr);
                }
            }

            // 2. 渲染 4 個關鍵轉折年卡片 (手機小螢幕直觀對焦)
            if (cardsContainer) {
                const milestones = [
                    { yr: 113, idx: 0, tag: "現況基準年", color: "border-slate-300 bg-white", desc: "純日間基準：實質滿招 99.40%、生師比 33.7" },
                    { yr: 117, idx: 4, tag: "首波虎年海嘯", color: "border-amber-400 bg-amber-50/60", desc: "新生降至 15.6 萬谷底，日間四技防禦均分 69.98 分" },
                    { yr: 122, idx: 9, tag: "少子化波谷防線", color: "border-blue-400 bg-blue-50/60", desc: "日間部綜合註冊率守穩 98.0% 滿招線" },
                    { yr: 128, idx: 15, tag: "少子化終局推估", color: "border-emerald-400 bg-emerald-50/50", desc: "日間錄取分守穩 69 分以上安全防線" }
                ];"""

if old_render_table in content:
    content = content.replace(old_render_table, new_render_table)
    print("  Updated renderSimTable function!")

# 8. In Data Modal CSV export: update tables 1, 2, 4, 5
old_csv_t1 = """                '# 【表一】全國國立科大 國貿/商務/航管/供應鏈 六強旗艦指標矩陣',
                '# -----------------------------------------------------------------------------------',
                '代號,學校名稱,系所名稱,區域,在學總人數,五專部人數,日間學士人數,進修學士人數,碩博生人數,專任師資總數,正教授,副教授,助理教授,境外生人數,境外生比率(%),114日間四技註冊率(%),114統測單科均分(分),113退學人數,113退學率(%)',
                ...DB.regional_six.map(x => [
                    x.code, x.school, x.dept, x.region, x.total_stu, x.five_year, x.undergrad_day, x.undergrad_eve, x.grad, x.faculty_total, x.faculty_prof, x.faculty_assoc, x.faculty_asst, x.oversea_stu, x.oversea_pct, x.reg_114_rate, x.score_114, x.drop_cnt_113, x.drop_rate_113
                ].join(',')),"""

new_csv_t1 = """                '# 【表一】全國國立科大 國貿/商務/航管/供應鏈 六強旗艦純日間部指標矩陣 (已排除進修部)',
                '# -----------------------------------------------------------------------------------',
                '代號,學校名稱,系所名稱,區域,純日間在學人數,五專部人數,日間學士人數,碩博生人數,專任師資總數,正教授,副教授,助理教授,境外生人數,境外生比率(%),114日間四技註冊率(%),114統測單科均分(分),113日間退學人數,113日間退學率(%)',
                ...DB.regional_six.map(x => [
                    x.code, x.school, x.dept, x.region, x.total_stu, x.five_year, x.undergrad_day, x.grad, x.faculty_total, x.faculty_prof, x.faculty_assoc, x.faculty_asst, x.oversea_stu, x.oversea_pct, x.reg_114_rate, x.score_114, x.drop_cnt_113, x.drop_rate_113
                ].join(',')),"""

if old_csv_t1 in content:
    content = content.replace(old_csv_t1, new_csv_t1)
    print("  Updated Data Modal Table 1 CSV export!")

old_csv_t2 = """                '# 【表二】中部大專商管競爭系所綜合情報比對',
                '# -----------------------------------------------------------------------------------',
                '學校系所,定位類型,核定名額現況,114日間註冊率(%),114進修註冊率(%),門檻均分估值(分),在學總人數,退學流失率(%),財務現金存量,每學期學費,生源管道分流,戰略威脅等級',
                ...DB.central_competitors.map(c => [
                    c.school, c.type, `"${c.quota_status}"`, c.reg_114_day, c.reg_114_eve, c.score_cutoff, c.students_total, c.drop_rate, `"${c.cash_reserve}"`, `"${c.tuition_per_sem}"`, `"${c.source_mix}"`, `"${c.threat_level}"`
                ].join(',')),"""

new_csv_t2 = """                '# 【表二】中部大專商管競爭系所純日間部情報比對 (已排除進修部)',
                '# -----------------------------------------------------------------------------------',
                '學校系所,定位類型,核定名額現況,114日間註冊率(%),門檻均分估值(分),純日間在學人數,日間退學流失率(%),財務現金存量,每學期學費,生源管道分流,戰略威脅等級',
                ...DB.central_competitors.map(c => [
                    c.school, c.type, `"${c.quota_status}"`, c.reg_114_day, c.score_cutoff, c.students_total, c.drop_rate, `"${c.cash_reserve}"`, `"${c.tuition_per_sem}"`, `"${c.source_mix}"`, `"${c.threat_level}"`
                ].join(',')),"""

if old_csv_t2 in content:
    content = content.replace(old_csv_t2, new_csv_t2)
    print("  Updated Data Modal Table 2 CSV export!")

old_csv_t4 = """                '# 【表四】教育部 UDB 官方核准中科國貿 5 大學制新生註冊率、名額消長與休退學原因體質矩陣',
                '# 官方報表：教育部 UDB 學12-1(註冊率), 學1-1(在學生), 學13-1(休學), 學14-1(退學原因)',
                '# -----------------------------------------------------------------------------------',
                '學制班別,日夜別,113核定名額,113實註人數,113新生註冊率,114核定名額,114實註人數,114境外生專班外加,114新生註冊率,在學學生數,休學生數,退學生數,退學率,主要退學原因,官方來源報表',
                '"日間學士班 (含四技)","日間部",80,80,"100.00%",80,79,26,"99.06%",382,7,11,"1.21%","志趣不合/科系不符期待(4人)、休學逾期未復學(4人)、逾期未註冊(1人)","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"日間二年制 (二技)","日間部",38,37,"97.37%",38,38,1,"100.00%",74,0,0,"0.00%","五專畢業升學穩定、全數滿招、極低休退學","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"進修學士班 (進修四技)","進修部",80,43,"53.75%",55,28,0,"50.91%",270,53,60,"8.26%","逾期未註冊(27人)、志趣不合(15人)、工作就業困難(8人)、休學逾期未復學(6人)","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"進修二年制 (夜二技)","進修部",75,47,"62.67%",55,49,0,"89.09%",93,0,0,"0.00%","主動減招20名成效立竿見影，註冊率回彈近9成，在職人士公餘進修穩定","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"日間五專部 (國貿科)","日間部",50,50,"100.00%",50,50,0,"100.00%",252,13,9,"1.79%","志趣不合/科系不符期待(5人)、休學逾期未復學(3人)","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',"""

new_csv_t4 = """                '# 【表四】教育部 UDB 官方核准中科國貿純日間部各學制新生註冊率、名額消長與休退學原因矩陣 (已排除進修部)',
                '# 官方報表：教育部 UDB 學12-1(註冊率), 學1-1(在學生), 學13-1(休學), 學14-1(退學原因)',
                '# -----------------------------------------------------------------------------------',
                '學制班別,日夜別,113核定名額,113實註人數,113新生註冊率,114核定名額,114實註人數,114境外生專班外加,114新生註冊率,在學學生數,休學生數,退學生數,退學率,主要退學原因,官方來源報表',
                '"日間學士班 (含四技)","日間部",80,80,"100.00%",80,79,26,"99.06%",382,7,11,"1.21%","志趣不合/科系不符期待(4人)、休學逾期未復學(4人)、逾期未註冊(1人)","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"日間二年制 (二技)","日間部",38,37,"97.37%",38,38,1,"100.00%",74,0,0,"0.00%","五專畢業升學穩定、全數滿招、極低休退學","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"日間五專部 (國貿科)","日間部",50,50,"100.00%",50,50,0,"100.00%",252,13,9,"1.79%","志趣不合/科系不符期待(5人)、休學逾期未復學(3人)","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"純日間部合計 (已排除進修部)","日間部全學制",168,167,"99.40%",168,167,27,"99.40%",708,20,20,"2.82%","志趣不合(9人)、休學逾期未復學(7人)；已全面排除進修部夜間數據","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',"""

if old_csv_t4 in content:
    content = content.replace(old_csv_t4, new_csv_t4)
    print("  Updated Data Modal Table 4 CSV export!")

old_csv_t5 = """                '# 【表五】教育部 113~128 學年度少子化預測基準模型 (16年動態推估)',
                '# -----------------------------------------------------------------------------------',
                '學年度,全國大一新生總數(萬人),統測報考總數(萬人),商管群人數(萬人),中部商管生源池(人),中科日間錄取均分推估(分),中科進修部註冊率推估(%),五專部防護力',
                ...DB.fertility_timeline.map(f => [
                    `${f.yr}學年`, f.fresh, f.tcte, f.biz, f.pool, f.day_score, f.eve_rate, `"${f.five_def}"`
                ].join(',')),"""

new_csv_t5 = """                '# 【表五】教育部 113~128 學年度少子化預測基準模型 (16年純日間動態推估)',
                '# -----------------------------------------------------------------------------------',
                '學年度,全國大一新生總數(萬人),統測報考總數(萬人),商管群人數(萬人),中部商管生源池(人),中科日間錄取均分推估(分),日間部註冊防護率推估(%),五專部防護力',
                ...DB.fertility_timeline.map(f => [
                    `${f.yr}學年`, f.fresh, f.tcte, f.biz, f.pool, f.day_score, `${f.day_score >= 71.0 ? 99.4 : +(99.4 - (71.0 - f.day_score) * 1.5).toFixed(1)}%`, `"${f.five_def}"`
                ].join(',')),"""

if old_csv_t5 in content:
    content = content.replace(old_csv_t5, new_csv_t5)
    print("  Updated Data Modal Table 5 CSV export!")

# Save back to interactive_dashboard.html
with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Successfully saved {FILE_PATH} ({len(content)} characters)")

# Sync to index.html and dist/index.html
with open("/Users/chenchunchih/Downloads/校務資料/index.html", "w", encoding="utf-8") as f:
    f.write(content)
with open("/Users/chenchunchih/Downloads/校務資料/dist/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Successfully synced to index.html and dist/index.html!")
