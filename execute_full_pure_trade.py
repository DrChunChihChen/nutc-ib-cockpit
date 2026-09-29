import re

with open("interactive_dashboard.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Navigation & Headers
html = html.replace(
    '<span>模組 3：系所體質深度診斷 (vs企管/虎科)</span>',
    '<span>模組 3：國貿系所體質與深水區診斷</span>'
)
html = html.replace(
    '<span>反超中科企管 <span class="text-emerald-600 font-bold">+0.05分</span></span>',
    '<span>穩居中台灣公立國貿榜首 <span class="text-emerald-600 font-bold">(71.78分)</span></span>'
)
html = html.replace(
    '中部大專商管大亂鬥 (中科 vs 逢甲 vs 東海 vs 嶺東/朝陽 vs 虎科)',
    '中部大專國貿/商務大對決 (中科國貿 vs 逢甲國貿 vs 東海國貿 vs 嶺東/朝陽國企)'
)
html = html.replace(
    '國立技職 (中科/虎科) vs 私立老牌普大 (逢甲/東海) vs 私立資金巨頭 (朝陽/嶺東)',
    '國立技職龍頭 (中科國貿) vs 私立頂尖普大 (逢甲國貿/東海國貿) vs 私立技職重鎮 (朝陽/嶺東國企)'
)

# 2. Module 2: Remove 虎科 card (lines 504~523)
card_pattern = r'<!-- 虎科財金 \(借鏡案例\) -->[\s\S]*?直接借鏡：[\s\S]*?</div>\s+</div>'
html = re.sub(card_pattern, '</div>', html)

# 3. Module 3: Update Header & Hero Card
html = html.replace(
    '模組 3：系所體質深度診斷 (中科國貿 vs 企管 & 虎科財金)',
    '模組 3：中科國貿系所體質與學制深水區診斷 (ITM Health & Retention)'
)
html = html.replace(
    '橫向深度剖析中科校內「國貿 vs 企管」同門競爭力，並縱向追蹤 6 年商管群統測最低錄取分與真實休退學黑洞。',
    '縱向追蹤 6 年全國國立國貿/商務旗艦統測單科均分走勢，並深度剖析中科國貿五專、四技、進修部全學制體質與休退學深水區。'
)

# Replace the hero banner
hero_pattern = r'<div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">\s+<div>\s+<div class="flex items-center gap-2">[\s\S]*?109年 -1\.27 → 114年 \+0\.05</div>\s+</div>\s+</div>'
new_hero = '''<div class="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="bg-emerald-600 text-white font-black text-xs px-2.5 py-0.5 rounded uppercase tracking-wider">Top in Central Taiwan</span>
                            <span class="text-xs font-semibold text-emerald-700">114學年度 統測商管群最低單科錄取均分</span>
                        </div>
                        <h2 class="text-xl font-extrabold text-slate-900 mt-1 flex items-baseline gap-2">
                            中科國貿 <span class="text-emerald-600 text-2xl">71.78分</span> 穩居中台灣公立國貿系所第一！
                        </h2>
                        <p class="text-xs text-slate-600 mt-1 max-w-3xl leading-relaxed">
                            在中部商管技職體系中，中科國貿以五專部 100% 滿招與日間四技 99.06% 形成堅實護城河，分數緊咬北部北商國商與雲科國管，展現高度生源競爭力。
                        </p>
                    </div>
                    <div class="bg-white/90 border border-emerald-500/40 rounded-xl p-3 text-center self-stretch md:self-auto min-w-[160px]">
                        <div class="text-[11px] text-slate-500 font-medium">114統測單科均分</div>
                        <div class="text-lg font-black text-emerald-600 mt-0.5">71.78分</div>
                        <div class="text-[10px] text-slate-500">中台灣公立國貿榜首</div>
                    </div>
                </div>'''
html = re.sub(hero_pattern, new_hero, html)

# Module 3 Score Trend Title
html = html.replace(
    '近 6 年（109~114學年度）統測商管群最低錄取單科均分趨勢',
    '全台國立科大國貿/商務/航運旗艦 6 年統測最低錄取均分走勢 (109~114學年度)'
)
html = html.replace(
    '官方技專招聯會登記分發最低總分折合單科權重平均（點擊下方按鈕可自訂顯示/隱藏特定校系）',
    '聚焦中科國貿、北商國商、雲科國管、高科航管、高科國企、高科供應鏈 6 大純國貿/商務旗艦之單科均分消長'
)

# 4. Replace Module 3 comparison block (lines 608~763) with Pure ITM diagnostics
structure_pattern = r'<!-- 雙雄硬核體質對照表：中科國貿 vs 中科企管 -->[\s\S]*?<!-- 113 vs 114 學制新生註冊率詳細矩陣對比表 -->[\s\S]*?</tbody>\s+</table>\s+</div>\s+</div>'

new_structure = '''<!-- 中科國貿學制結構與留存體質深水區診斷 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- 國貿系學制與在學規模深度剖析 -->
                <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-4 border-b border-slate-200/70 pb-3">
                            <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                                <i data-lucide="layers" class="w-4 h-4 text-emerald-600"></i>
                                <span>中科國貿 各學制規模與師資結構</span>
                            </h3>
                            <span class="text-xs text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">在學總計 1,044人</span>
                        </div>
                        <div class="space-y-3 text-xs">
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">專任師資規模與生師比</span>
                                <span class="font-bold text-slate-900">21人 (教授4 / 副教授14 / 助理教授3) | 生師比 49.7</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">日間部五專 (5個年級)</span>
                                <span class="font-bold text-slate-900">248人 (每屆1班50人，常年 100% 滿招)</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">日間部四技 (4個年級)</span>
                                <span class="font-bold text-emerald-700">482人 (全系核心主力，114 註冊率 99.06%)</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">進修部四技 (夜間部)</span>
                                <span class="font-bold text-rose-600">314人 (核定降至55名，114 註冊率 50.91%)</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">日間二年制 / 進修二技</span>
                                <span class="font-bold text-slate-900">日間 38人 (滿招) / 進修 49人 (減招後反彈至 89.1%)</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">境外學位生 (國際化)</span>
                                <span class="font-bold text-sky-700">58人 (佔全系在學 5.6%，以港澳及東南亞為主)</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">研究所編制現況</span>
                                <span class="font-bold text-slate-500">目前尚無碩士班與碩專班 (專注大學部培育)</span>
                            </div>
                        </div>
                    </div>
                    <div class="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 leading-relaxed">
                        💡 <strong>學制結構診斷：</strong>中科國貿以「日間四技 (482人) + 五專部 (248人)」為堅實防守核心，五專直升四技升學梯隊穩固。唯一需高度警戒為進修部四技（314人），在少子化浪潮下進修部生源首當其衝。
                    </div>
                </div>

                <!-- 國貿系退學與休學深水區解剖 -->
                <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-4 border-b border-slate-200/70 pb-3">
                            <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                                <i data-lucide="alert-triangle" class="w-4 h-4 text-amber-600"></i>
                                <span>113學年度 國貿系退學與休學深水區剖析</span>
                            </h3>
                            <span class="text-xs text-rose-600 font-bold">全期退學 80人 (3.73%)</span>
                        </div>

                        <div class="grid grid-cols-2 gap-3 mb-4">
                            <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                <div class="text-slate-500 text-[11px]">國貿系 整體退學率</div>
                                <div class="text-2xl font-black text-rose-600 mt-1">3.73%</div>
                                <div class="text-[10px] text-slate-500">80人退學 / 六強國貿最高</div>
                            </div>
                            <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                <div class="text-slate-500 text-[11px]">國貿系 休學中人數</div>
                                <div class="text-2xl font-black text-amber-600 mt-1">6.82%</div>
                                <div class="text-[10px] text-slate-500">73人休學未復學</div>
                            </div>
                        </div>

                        <div class="space-y-2.5 text-xs">
                            <div class="text-[11px] text-slate-700 font-semibold">退學 80 人深層動因剖析：</div>
                            
                            <div>
                                <div class="flex justify-between text-[11px] mb-1">
                                    <span class="text-slate-600">志趣不合 / 科系不符 (自退核心)</span>
                                    <span class="text-rose-600 font-bold">24人 (佔自退 72.7%)</span>
                                </div>
                                <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">
                                    <div class="bg-rose-500 h-full" style="width: 72.7%"></div>
                                </div>
                            </div>

                            <div>
                                <div class="flex justify-between text-[11px] mb-1">
                                    <span class="text-slate-600">逾期未註冊 / 逾期未復學 (失聯強制退學)</span>
                                    <span class="text-slate-700 font-bold">47人 (佔整體退學 58.8%)</span>
                                </div>
                                <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">
                                    <div class="bg-slate-400 h-full" style="width: 58.8%"></div>
                                </div>
                            </div>

                            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 text-[11px] space-y-1">
                                <div class="flex justify-between text-slate-700">
                                    <span>工作需求 / 經濟因素自願退學</span>
                                    <span class="text-amber-700 font-semibold">8人 (多集中於進修部)</span>
                                </div>
                                <div class="flex justify-between text-slate-700">
                                    <span>學業成績因素退學</span>
                                    <span class="text-emerald-700 font-semibold">1人 (學科淘汰率極低)</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="text-[11px] text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-200 mt-3 leading-relaxed">
                        ⚠️ <strong>警報解讀：</strong>國貿系 80 名退學生中，高達 <strong class="text-rose-600">24 人明確因「科系不符/志趣不合」</strong>主動申請退學，多數發生於大一升大二階段（轉學考或重考），反映高中職升學選填志願時對「國際貿易經營實務」存在想像落差，急需大一新生生涯導引、雙軌產業實習與專題激勵。
                    </div>
                </div>
            </div>

            <!-- 113 vs 114 學制新生註冊率詳細矩陣對比表 -->
            <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-lg">
                <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2 mb-3">
                    <i data-lucide="table" class="w-4 h-4 text-emerald-600"></i>
                    中科國貿系 113~114學年度 各學制新生註冊率與核定名額消長矩陣
                </h3>
                <div class="overflow-x-auto rounded-xl border border-slate-200">
                    <table class="w-full text-left text-xs border-collapse">
                        <thead class="bg-slate-50 text-slate-700 uppercase font-semibold border-b border-slate-200">
                            <tr>
                                <th class="p-3">學制班別</th>
                                <th class="p-3">113學年度註冊率 (實招/核定)</th>
                                <th class="p-3">114學年度註冊率 (實招/核定)</th>
                                <th class="p-3">體質狀態</th>
                                <th class="p-3">戰略消長與因應策略</th>
                            </tr>
                        </thead>
                        <tbody id="m3-reg-matrix-body" class="divide-y divide-slate-100 bg-white">
                            <!-- 動態填入 -->
                        </tbody>
                    </table>
                </div>
            </div>'''
html = re.sub(structure_pattern, new_structure, html)

# 5. Update Module 6: Purge 國貿 vs 企管, Replace with 正取生保衛戰
html = html.replace(
    '<!-- 圖表駕駛艙 Row 2: 國貿 vs 企管 雙榜正面對決 + 三大天敵情報深水區 -->',
    '<!-- 圖表駕駛艙 Row 2: 中科國貿 169 位正取生去向保衛戰 + 三大天敵情報深水區 -->'
)

# 6. Update DB JSON object
# Remove 虎科財金 from central_competitors in DB
html = re.sub(r', \{"school": "虎科財金"[^}]+features": "[^"]+"\}', '', html)

# Update score_trends in DB
new_trends_json = '"score_trends": {"years": ["109", "110", "111", "112", "113", "114"], "departments": {"中科大國貿": [75.44, 76.89, 68.33, 68.44, 75.56, 71.78], "北商大國商": [84.71, 84.07, 80.14, 74.43, 80.93, 79.86], "雲科大國管": [82.5, 83.1, 77.8, 73.8, 81.33, 79.78], "高科大航管": [72.8, 73.5, 67.2, 67.9, 73.56, 73.89], "高科大國企": [74.2, 75.6, 68.1, 68.2, 76.44, 67.5], "高科供應鏈": [70.5, 72.1, 65.4, 65.1, 71.85, 65.7]}}'
html = re.sub(r'"score_trends":\s*\{"years":\s*\["109",[^}]+departments":\s*\{[^}]+\}\}', new_trends_json, html)

# 7. Update initModule3Charts and colors
m3_init_pattern = r'function initModule3Charts\(\)[\s\S]*?charts\.m3Trend = new Chart\(ctxTrend, \{'
new_m3_init = '''function initModule3Charts() {
            const trends = DB.score_trends;
            const ctxTrend = document.getElementById('chart-m3-score-trend').getContext('2d');

            const colors = {
                '中科大國貿': '#10b981',
                '北商大國商': '#0284c7',
                '雲科大國管': '#6366f1',
                '高科大航管': '#f59e0b',
                '高科大國企': '#ec4899',
                '高科供應鏈': '#64748b'
            };

            const datasets = Object.keys(trends.departments).map((dept, idx) => {
                const isITM = dept === '中科大國貿';
                return {
                    label: dept,
                    data: trends.departments[dept],
                    borderColor: colors[dept] || '#cbd5e1',
                    backgroundColor: colors[dept] || '#cbd5e1',
                    borderWidth: isITM ? 3.5 : 2,
                    pointRadius: isITM ? 6 : 4,
                    pointHoverRadius: 8,
                    borderDash: isITM ? [] : [4, 4],
                    tension: 0.25,
                    hidden: false
                };
            });

            charts.m3Trend = new Chart(ctxTrend, {'''
html = re.sub(m3_init_pattern, new_m3_init, html)

# Update modal description text
html = html.replace(
    '<li><strong>模組 2（中部大專商管大亂鬥）：</strong>對壘逢甲、東海、嶺東、朝陽、虎科，比較公私立定價優勢、普高學測吸磁、主動減招防禦、現金存量與進修部存亡戰。',
    '<li><strong>模組 2（中部大專國貿大對決）：</strong>聚焦中科國貿、逢甲國貿、東海國貿、朝陽國企、嶺東國企，比較公私立定價優勢、普高學測吸磁、主動減招防禦、現金存量與進修部存亡戰。'
)
html = html.replace(
    '<li><strong>模組 3（系所體質深度診斷）：</strong>中科國貿 vs 中科企管 6年統測走勢（114年國貿以 71.78分首度反超企管 71.73分），並切入 80人退學（科系不符24人）與進修部50.91%深水區。',
    '<li><strong>模組 3（國貿系所體質診斷）：</strong>聚焦全台國立國貿旗艦 6 年統測走勢（中科國貿 71.78分居中台灣公立第一），並深度切入五專、四技、進修部學制結構與 80人退學深水區。'
)

with open("interactive_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Executed full pure trade conversion!")
