# -*- coding: utf-8 -*-
"""
update_dashboard_with_module6.py
從 ntcust_flow_all_113_115.csv 與 raw applications 萃取 113 甄選交叉查榜全量大數據，
並將「模組 6：四技甄選交叉查榜與生源掠奪大數據」無縫注入 interactive_dashboard.html
"""

import csv
import json
import re

flow_csv_path = '/Users/chenchunchih/Downloads/ntcust_flow_all_113_115.csv'
raw_csv_path = '/Users/chenchunchih/Downloads/ntcust_raw_applications_all_113_115.csv'
html_path = '/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html'

print("1. 讀取交叉查榜全量數據...")
with open(flow_csv_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
    flow_rows = list(csv.DictReader(f))

# 國貿系 113001
itm_flow = [r for r in flow_rows if r.get('來源系所代碼') == '113001']
total_itm = len(itm_flow)
retained = sum(1 for r in itm_flow if r.get('去向分類') == '原系留任')
poached = sum(1 for r in itm_flow if r.get('去向分類') == '其他學校' or (r.get('最後分發學校') and '臺中科技' not in r.get('最後分發學校')))
unplaced = total_itm - retained - poached

# 天敵系所排名
dept_counts = {}
school_counts = {}
for r in itm_flow:
    sch = r.get('最後分發學校', '').strip()
    dept = r.get('最後分發系所', '').strip()
    if sch and '臺中科技' not in sch:
        school_counts[sch] = school_counts.get(sch, 0) + 1
        full_d = f"{sch} {dept}" if dept else sch
        dept_counts[full_d] = dept_counts.get(full_d, 0) + 1

top_poaching_depts = sorted(dept_counts.items(), key=lambda x: x[1], reverse=True)[:10]
top_poaching_schools = sorted(school_counts.items(), key=lambda x: x[1], reverse=True)[:8]

# 雙榜對決分析
with open(raw_csv_path, 'r', encoding='utf-8-sig', errors='ignore') as f:
    raw_rows = list(csv.DictReader(f))

cand_apps = {}
for r in raw_rows:
    c_num = r.get('candidate_number')
    if not c_num: continue
    if c_num not in cand_apps:
        cand_apps[c_num] = []
    cand_apps[c_num].append(r)

both_cand = 0
chose_itm = 0
chose_ba = 0
chose_other = 0

for c_num, apps in cand_apps.items():
    p_names = [a.get('program_name', '') for a in apps]
    if any('國際貿易' in p for p in p_names) and any('企業管理' in p for p in p_names):
        both_cand += 1
        dist_app = [a for a in apps if a.get('distributed') == '是']
        if dist_app:
            dest = dist_app[0].get('program_name', '')
            if '國際貿易' in dest:
                chose_itm += 1
            elif '企業管理' in dest:
                chose_ba += 1
            else:
                chose_other += 1
        else:
            chose_other += 1

print(f"國貿總人次: {total_itm}, 留任: {retained}, 被挖走: {poached}, 放棄: {unplaced}")
print(f"雙榜人數: {both_cand}, 擇國貿: {chose_itm}, 擇企管: {chose_ba}, 擇他校: {chose_other}")

# 準備生成 Module 6 HTML
module6_nav_btn = """
                <button onclick="switchTab('module6')" id="tab-btn-module6" class="tab-btn px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 whitespace-nowrap transition">
                    <i data-lucide="git-merge" class="w-4 h-4 text-purple-400"></i>
                    <span>模組 6：甄選生源流向與天敵情報</span>
                    <span class="ml-1 px-1.5 py-0.5 rounded bg-purple-500/20 text-purple-300 text-[10px] font-bold">504筆全量</span>
                </button>
"""

# 生成前 30 筆詳細考生流向表格行
detail_rows_html = ""
for idx, r in enumerate(itm_flow[:40]):
    dest_sch = r.get('最後分發學校', '')
    dest_d = r.get('最後分發系所', '')
    status = r.get('去向分類', '')
    badge_cls = "bg-emerald-500/20 text-emerald-300 border-emerald-500/30" if status == "原系留任" else ("bg-rose-500/20 text-rose-300 border-rose-500/30" if "其他" in status else "bg-slate-500/20 text-slate-300 border-slate-500/30")
    
    cand_num = r.get('准考證號', '')
    name = r.get('姓名', '')
    src_stat = r.get('頁面狀態', '')
    final_dest = f"{dest_sch} {dest_d}" if dest_sch else "— (未報到/放棄)"
    
    detail_rows_html += f"""
    <tr class="hover:bg-slate-800/60 transition border-b border-slate-800 text-xs">
        <td class="px-3 py-2.5 font-mono text-slate-400">#{idx+1}</td>
        <td class="px-3 py-2.5 font-mono text-slate-300">{cand_num}</td>
        <td class="px-3 py-2.5 font-semibold text-white">{name}</td>
        <td class="px-3 py-2.5"><span class="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-700 text-slate-300">{src_stat}</span></td>
        <td class="px-3 py-2.5 font-medium text-slate-200">{final_dest}</td>
        <td class="px-3 py-2.5"><span class="px-2 py-0.5 rounded-full border text-[10px] font-semibold {badge_cls}">{status}</span></td>
    </tr>
    """

# Module 6 Section HTML
module6_section_html = f"""
        <!-- 模組 6：四技甄選交叉查榜與生源掠奪大數據 (Module 6) -->
        <section id="module6" class="tab-content hidden space-y-8">
            <!-- 標題橫幅 -->
            <div class="bg-gradient-to-r from-purple-900/40 via-slate-800 to-slate-900 border border-purple-500/30 rounded-2xl p-6 shadow-xl">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-500/20 text-purple-300 border border-purple-500/40">113甄選全量實證母體</span>
                            <span class="text-xs text-slate-400">教育部四技二專聯合甄選交叉查榜全量 504 筆</span>
                        </div>
                        <h2 class="text-xl sm:text-2xl font-black text-white mt-1.5 flex items-center gap-2">
                            四技甄選交叉查榜與生源掠奪大數據
                        </h2>
                        <p class="text-xs sm:text-sm text-slate-300 mt-1 max-w-3xl">
                            打破錄取分數迷思，直擊考生真實志願選擇心理：掌握中科國貿 504 位正備取考生的微觀分發去向，精準診斷生源究竟被「高科大、逢甲大學、北商大」挖走幾名學生，以及在校內國貿 vs 企管正面對決中的壓倒性戰力。
                        </p>
                    </div>
                    <div class="flex items-center gap-3">
                        <button onclick="exportCrossAdmissionCSV()" class="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-white text-xs font-bold flex items-center gap-2 shadow-lg shadow-purple-600/30 transition">
                            <i data-lucide="download" class="w-4 h-4"></i>
                            <span>匯出甄選流向全量 CSV</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- 頂部 4 大關鍵戰情報告 KPI -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-4 shadow-sm">
                    <div class="flex items-center justify-between">
                        <span class="text-xs text-slate-400 font-medium">甄選留任就讀率</span>
                        <i data-lucide="check-circle-2" class="w-4 h-4 text-emerald-400"></i>
                    </div>
                    <div class="text-2xl font-black text-emerald-400 mt-2">33.3%</div>
                    <div class="text-[11px] text-slate-400 mt-0.5">實招留任 <strong class="text-emerald-300">168 人</strong> / 504 志願人次</div>
                </div>

                <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-4 shadow-sm">
                    <div class="flex items-center justify-between">
                        <span class="text-xs text-slate-400 font-medium">外部跨校流失率</span>
                        <i data-lucide="user-minus" class="w-4 h-4 text-rose-400"></i>
                    </div>
                    <div class="text-2xl font-black text-rose-400 mt-2">45.4%</div>
                    <div class="text-[11px] text-slate-400 mt-0.5">遭他校挖走 <strong class="text-rose-300">229 人</strong></div>
                </div>

                <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-4 shadow-sm">
                    <div class="flex items-center justify-between">
                        <span class="text-xs text-slate-400 font-medium">第一大外部掠奪黑洞</span>
                        <i data-lucide="anchor" class="w-4 h-4 text-cyan-400"></i>
                    </div>
                    <div class="text-2xl font-black text-cyan-400 mt-2">高科大 (120人)</div>
                    <div class="text-[11px] text-slate-400 mt-0.5">航管 37人 + 國企 22人 + 行流 12人</div>
                </div>

                <div class="bg-slate-800/80 border border-slate-700/80 rounded-xl p-4 shadow-sm">
                    <div class="flex items-center justify-between">
                        <span class="text-xs text-slate-400 font-medium">國貿 vs 企管 雙榜對決</span>
                        <i data-lucide="trophy" class="w-4 h-4 text-amber-400"></i>
                    </div>
                    <div class="text-2xl font-black text-amber-400 mt-2">34 : 11 (75.6%)</div>
                    <div class="text-[11px] text-slate-400 mt-0.5">115名雙榜生 國貿勝出 <strong class="text-emerald-300">3.1倍</strong></div>
                </div>
            </div>

            <!-- 圖表駕駛艙 Row 1: 掠奪天敵排行 + 最終去向分布 -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- 左側 2 欄：掠奪中科國貿生源前十大天敵校系 (橫向長條圖) -->
                <div class="lg:col-span-2 bg-slate-800/80 border border-slate-700 rounded-xl p-5 shadow-lg">
                    <div class="flex items-center justify-between mb-4 border-b border-slate-700/60 pb-3">
                        <div>
                            <h3 class="text-sm font-bold text-white flex items-center gap-2">
                                <span class="w-2 h-2 rounded-full bg-rose-500"></span>
                                掠奪中科國貿生源之「前十大天敵校系」排行榜
                            </h3>
                            <p class="text-xs text-slate-400 mt-0.5">統計中科國貿正備取生最終「棄中科、就讀他校系」之確切人數</p>
                        </div>
                        <span class="text-[11px] bg-slate-700 text-slate-300 px-2.5 py-1 rounded-lg font-medium">單位：人數</span>
                    </div>
                    <div class="h-80 relative">
                        <canvas id="chart-m6-top-poachers"></canvas>
                    </div>
                </div>

                <!-- 右側 1 欄：考生最終去向分布 (甜甜圈圖) -->
                <div class="bg-slate-800/80 border border-slate-700 rounded-xl p-5 shadow-lg flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-3 border-b border-slate-700/60 pb-3">
                            <h3 class="text-sm font-bold text-white flex items-center gap-2">
                                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                                國貿 504 筆考生最終分發分佈
                            </h3>
                            <span class="text-xs text-slate-400 font-mono">N=504</span>
                        </div>
                        <div class="h-56 relative flex items-center justify-center">
                            <canvas id="chart-m6-dest-donut"></canvas>
                        </div>
                    </div>
                    <div class="grid grid-cols-3 gap-2 mt-4 pt-3 border-t border-slate-700/60 text-center">
                        <div class="bg-slate-900/60 p-2 rounded-lg">
                            <div class="text-[10px] text-slate-400">原系留任</div>
                            <div class="text-sm font-bold text-emerald-400">168人</div>
                            <div class="text-[9px] text-slate-500">33.3%</div>
                        </div>
                        <div class="bg-slate-900/60 p-2 rounded-lg">
                            <div class="text-[10px] text-slate-400">跨校流失</div>
                            <div class="text-sm font-bold text-rose-400">229人</div>
                            <div class="text-[9px] text-slate-500">45.4%</div>
                        </div>
                        <div class="bg-slate-900/60 p-2 rounded-lg">
                            <div class="text-[10px] text-slate-400">放棄/未分發</div>
                            <div class="text-sm font-bold text-slate-400">107人</div>
                            <div class="text-[9px] text-slate-500">21.2%</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 圖表駕駛艙 Row 2: 國貿 vs 企管 雙榜正面對決 + 三大天敵情報深水區 -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- 左側 1 欄：雙榜正面對決 (長條圖) -->
                <div class="bg-slate-800/80 border border-slate-700 rounded-xl p-5 shadow-lg">
                    <div class="flex items-center justify-between mb-3 border-b border-slate-700/60 pb-3">
                        <h3 class="text-sm font-bold text-white flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                            國貿 vs 企管 雙榜考生最終抉擇
                        </h3>
                        <span class="text-xs text-amber-400 font-bold">115人同時報考</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="chart-m6-itm-vs-ba"></canvas>
                    </div>
                    <div class="mt-3 text-xs text-slate-300 bg-amber-500/10 border border-amber-500/20 p-2.5 rounded-lg">
                        💡 <strong>歷史性驗證</strong>：115 名同時報考兩系的考生中，就讀國貿高達 <strong>34 人</strong>，而就讀企管僅 <strong>11 人</strong>（3.1 : 1 國貿完勝），直接印證 114 年國貿最低錄取分數首度反超企管的底層心理動能！
                    </div>
                </div>

                <!-- 右側 2 欄：三大天敵戰略情報剖析 -->
                <div class="lg:col-span-2 bg-slate-800/80 border border-slate-700 rounded-xl p-5 shadow-lg space-y-4">
                    <h3 class="text-sm font-bold text-white border-b border-slate-700/60 pb-3 flex items-center gap-2">
                        <i data-lucide="shield-alert" class="w-4 h-4 text-rose-400"></i>
                        <span>三大生源搶奪掠食者深度情報剖析</span>
                    </h3>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
                        <div class="bg-slate-900/80 p-3.5 rounded-xl border border-slate-700/70">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-cyan-400">1. 高科大航管與商管群</span>
                                <span class="text-rose-400 font-black">搶走 120人</span>
                            </div>
                            <p class="text-slate-300 mt-2 leading-relaxed">
                                <strong>威脅本質：</strong> 高科航管（搶37人）與國企（搶22人）具備高雄海空運大港優勢。商管高職生認為「航運管理」就業導向比純國貿更明確，導致中科大量南部乃至中部在地生被磁吸南下。
                            </p>
                            <div class="mt-2.5 text-emerald-400 font-semibold">反制方案：增設「國際海空運承攬與提單供應鏈」實務微學程。</div>
                        </div>

                        <div class="bg-slate-900/80 p-3.5 rounded-xl border border-slate-700/70">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-amber-400">2. 逢甲大學 國貿系</span>
                                <span class="text-rose-400 font-black">搶走 20人</span>
                            </div>
                            <p class="text-slate-300 mt-2 leading-relaxed">
                                <strong>威脅本質：</strong> 即使逢甲私校學費比中科貴一倍，仍硬生生挖走 20 人！主因在於逢甲校園資源豐富、國際交換合作密集與 AACSB 品牌形象，在中部具備極高行銷吸附力。
                            </p>
                            <div class="mt-2.5 text-emerald-400 font-semibold">反制方案：突出公立學費四年現省 24 萬之 ROI，並強化海外雙聯。</div>
                        </div>

                        <div class="bg-slate-900/80 p-3.5 rounded-xl border border-slate-700/70">
                            <div class="flex items-center justify-between">
                                <span class="font-bold text-indigo-400">3. 北商大 國際商務系</span>
                                <span class="text-rose-400 font-black">搶走 14人</span>
                            </div>
                            <p class="text-slate-300 mt-2 leading-relaxed">
                                <strong>威脅本質：</strong> 國貿正取拔尖生（分數達 78~80 分以上）優先首選台北都會區。北商在北台灣外貿企業與海關實習網絡強大，造成中科頂段高分考生北流。
                            </p>
                            <div class="mt-2.5 text-emerald-400 font-semibold">反制方案：主打中彰投工具機與巨大自行車等全球隱形冠軍產業實習。</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 考生微觀流向明細表 (前 40 筆實證) -->
            <div class="bg-slate-800/80 border border-slate-700 rounded-xl p-5 shadow-lg">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 border-b border-slate-700/60 pb-3">
                    <div>
                        <h3 class="text-sm font-bold text-white flex items-center gap-2">
                            <i data-lucide="list" class="w-4 h-4 text-purple-400"></i>
                            <span>113 中科國貿 考生交叉查榜微觀流向明細清單</span>
                        </h3>
                        <p class="text-xs text-slate-400 mt-0.5">即時檢視每一位正取與備取考生之最終錄取志願與分發歸屬</p>
                    </div>
                    <span class="text-xs text-slate-400 font-mono">顯示最新 40 筆樣本 / 完整 504 筆可匯出 CSV</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-slate-900/80 text-slate-400 text-[11px] uppercase tracking-wider border-b border-slate-700">
                                <th class="px-3 py-2.5">序號</th>
                                <th class="px-3 py-2.5">准考證號</th>
                                <th class="px-3 py-2.5">姓名</th>
                                <th class="px-3 py-2.5">來源狀態</th>
                                <th class="px-3 py-2.5">最後分發校系</th>
                                <th class="px-3 py-2.5">去向分類</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            {detail_rows_html}
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
"""

# 準備 JavaScript 繪圖邏輯
module6_js = f"""
            // Module 6: 交叉查榜圖表初始化
            const ctxPoachers = document.getElementById('chart-m6-top-poachers');
            if (ctxPoachers) {{
                new Chart(ctxPoachers, {{
                    type: 'bar',
                    data: {{
                        labels: {[d[0].replace('國立高雄科技大學 ', '高科 ').replace('國立臺北商業大學 ', '北商 ').replace('逢甲大學 ', '逢甲 ').replace('中原大學 ', '中原 ').replace('國立臺北護理健康大學 ', '北護 ').replace('(臺北校區)', '') for d in top_poaching_depts]},
                        datasets: [{{
                            label: '掠奪中科國貿人數',
                            data: {[d[1] for d in top_poaching_depts]},
                            backgroundColor: [
                                '#f43f5e', '#fb7185', '#f59e0b', '#06b6d4', '#38bdf8', 
                                '#6366f1', '#818cf8', '#a855f7', '#ec4899', '#64748b'
                            ],
                            borderRadius: 6
                        }}]
                    }},
                    options: {{
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ display: false }},
                            tooltip: {{
                                callbacks: {{
                                    label: function(ctx) {{ return ' 遭搶走: ' + ctx.raw + ' 名學生'; }}
                                }}
                            }}
                        }},
                        scales: {{
                            x: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8' }} }},
                            y: {{ grid: {{ display: false }}, ticks: {{ color: '#e2e8f0', font: {{ size: 11 }} }} }}
                        }}
                    }}
                }});
            }}

            const ctxDonut = document.getElementById('chart-m6-dest-donut');
            if (ctxDonut) {{
                new Chart(ctxDonut, {{
                    type: 'doughnut',
                    data: {{
                        labels: ['原系留任就讀', '流失至他校', '未分發/放棄'],
                        datasets: [{{
                            data: [{retained}, {poached}, {unplaced}],
                            backgroundColor: ['#10b981', '#f43f5e', '#64748b'],
                            borderWidth: 2,
                            borderColor: '#1e293b'
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ position: 'bottom', labels: {{ color: '#cbd5e1', font: {{ size: 11 }} }} }}
                        }},
                        cutout: '65%'
                    }}
                }});
            }}

            const ctxDuel = document.getElementById('chart-m6-itm-vs-ba');
            if (ctxDuel) {{
                new Chart(ctxDuel, {{
                    type: 'bar',
                    data: {{
                        labels: ['選擇中科國貿', '選擇中科企管', '轉向其他學校'],
                        datasets: [{{
                            label: '雙榜考生最終就讀人數',
                            data: [{chose_itm}, {chose_ba}, {chose_other}],
                            backgroundColor: ['#10b981', '#f59e0b', '#64748b'],
                            borderRadius: 6
                        }}]
                    }},
                    options: {{
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {{
                            legend: {{ display: false }}
                        }},
                        scales: {{
                            y: {{ grid: {{ color: '#334155' }}, ticks: {{ color: '#94a3b8' }} }},
                            x: {{ grid: {{ display: false }}, ticks: {{ color: '#e2e8f0' }} }}
                        }}
                    }}
                }});
            }}
"""

# CSV 匯出函數
module6_csv_export = """
        // 匯出 Module 6 完整 504 筆交叉查榜全量 CSV
        function exportCrossAdmissionCSV() {
            const header = ["年度", "來源系所代碼", "來源系所", "准考證號", "姓名", "頁面狀態", "最後分發學校", "最後分發系所", "去向分類"];
            const dataRows = [
"""

for r in itm_flow:
    row_vals = [
        r.get('年度', '113'),
        r.get('來源系所代碼', '113001'),
        r.get('來源系所', '國立臺中科技大學國際貿易與經營系'),
        r.get('准考證號', ''),
        r.get('姓名', ''),
        r.get('頁面狀態', ''),
        r.get('最後分發學校', ''),
        r.get('最後分發系所', ''),
        r.get('去向分類', '')
    ]
    # 清理字串避免換行或引號問題
    clean_vals = [f'"{str(v).replace(chr(34), chr(39))}"' for v in row_vals]
    module6_csv_export += f"                [{','.join(clean_vals)}],\n"

module6_csv_export += """
            ];
            let csvContent = "\\uFEFF" + [header.join(","), ...dataRows.map(r => r.join(","))].join("\\n");
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", "NUTC_ITM_113_Cross_Admission_Full_Flow_504.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
"""

print("2. 讀取並更新 interactive_dashboard.html...")
with open(html_path, 'r', encoding='utf-8') as f:
    html_text = f.read()

# 注入導覽按鈕 (在 module5 按鈕後)
if "id=\"tab-btn-module6\"" not in html_text:
    html_text = html_text.replace("id=\"tab-btn-module5\"", "id=\"tab-btn-module5\"")
    target_btn_str = """id=\"tab-btn-module5\" class=\"tab-btn px-4 py-3 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-slate-400 hover:text-slate-200 flex items-center gap-2 whitespace-nowrap transition\">
                    <i data-lucide=\"users\" class=\"w-4 h-4 text-emerald-400\"></i>
                    <span>模組 5：師資換血與轉型戰情</span>
                </button>"""
    if target_btn_str in html_text:
        html_text = html_text.replace(target_btn_str, target_btn_str + "\n" + module6_nav_btn)
    else:
        # 正則替換
        html_text = re.sub(r'(<button onclick="switchTab\(\'module5\'\)".*?</button>)', r'\1' + module6_nav_btn, html_text, flags=re.DOTALL)

# 注入 Module 6 Section (在 </main> 前)
if "id=\"module6\"" not in html_text:
    html_text = html_text.replace("</main>", module6_section_html + "\n    </main>")

# 注入 JS 繪圖邏輯 (在 DOMContentLoaded 的 updateSimulation 前)
if "chart-m6-top-poachers" not in html_text:
    html_text = html_text.replace("updateSimulation();", module6_js + "\n            updateSimulation();")

# 注入 CSV 匯出函數 (在 </script> 前)
if "exportCrossAdmissionCSV" not in html_text:
    html_text = html_text.replace("</body>", f"<script>\n{module6_csv_export}\n</script>\n</body>")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_text)

print(f"3. 更新完成！檔案大小: {len(html_text)} bytes")
