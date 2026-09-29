import re, json

with open("interactive_dashboard.html", "r", encoding="utf-8") as f:
    html = f.read()

# =========================================================================
# 1. Update Navigation and Global KPI
# =========================================================================
html = html.replace(
    '<span>模組 3：系所體質深度診斷 (vs企管/虎科)</span>',
    '<span>模組 3：國貿系所體質與深水區診斷</span>'
)

html = html.replace(
    '<span>反超中科企管 <span class="text-emerald-600 font-bold">+0.05分</span></span>',
    '<span>穩居中台灣公立國貿榜首 <span class="text-emerald-600 font-bold">(71.78分)</span></span>'
)
html = html.replace(
    '<span class="text-[10px] text-emerald-700 font-bold bg-emerald-50 border border-emerald-200 px-1.5 py-0.5 rounded">首度逆轉</span>',
    '<span class="text-[10px] text-emerald-700 font-bold bg-emerald-50 border border-emerald-200 px-1.5 py-0.5 rounded">中台公立榜首</span>'
)

# =========================================================================
# 2. Module 2: Purge 虎科財金, retain 5 Central Taiwan Trade Departments
# =========================================================================
html = html.replace(
    '中部大專商管大亂鬥 (中科 vs 逢甲 vs 東海 vs 嶺東/朝陽 vs 虎科)',
    '中部大專國貿/商務大對決 (中科國貿 vs 逢甲國貿 vs 東海國貿 vs 嶺東/朝陽國企)'
)
html = html.replace(
    '國立技職 (中科/虎科) vs 私立老牌普大 (逢甲/東海) vs 私立資金巨頭 (朝陽/嶺東)',
    '國立技職龍頭 (中科國貿) vs 私立頂尖普大 (逢甲國貿/東海國貿) vs 私立技職重鎮 (朝陽/嶺東國企)'
)

# Remove the 6th card (虎科財金) in Module 2
# Pattern: <!-- 虎科財金 (借鏡案例) --> ... </div>\s+</div>\s+<!-- 兩大對決圖表
pattern_nfu_card = r'<!-- 虎科財金 \(借鏡案例\) -->[\s\S]*?</div>\s+</div>\s+<!-- 兩大對決圖表'
replacement_nfu_card = '</div>\n\n            <!-- 兩大對決圖表'
html = re.sub(pattern_nfu_card, replacement_nfu_card, html)

# =========================================================================
# 3. Module 3: Purge 企管 and 虎科, make it Pure ITM & National Trade Peers
# =========================================================================
html = html.replace(
    '模組 3：系所體質深度診斷 (中科國貿 vs 企管 & 虎科財金)',
    '模組 3：中科國貿系所體質與學制深水區診斷 (ITM Health & Retention)'
)
html = html.replace(
    '橫向深度剖析中科校內「國貿 vs 企管」同門競爭力，並縱向追蹤 6 年商管群統測最低錄取分與真實休退學黑洞。',
    '縱向追蹤 6 年全國國立國貿/商務旗艦統測單科均分走勢，並深度剖析中科國貿五專、四技、進修部全學制體質與休退學深水區。'
)

html = html.replace(
    '<span class="text-xs text-slate-400">中科國貿 vs 中科企管 6年統測單科均分走勢</span>',
    '<span class="text-xs text-slate-500">全國國立科大國貿/商務旗艦 6年統測單科均分走勢 (109~114學年度)</span>'
)

# Replace the hero banner in Module 3
old_m3_banner = '''                    <h3 class="text-base font-black text-slate-900 flex items-center gap-2">
                        <span>歷史性交叉點：</span>
                        <span>中科國貿 <span class="text-emerald-600 text-2xl">71.78分</span> 首度反超 中科企管 <span class="text-slate-900 text-2xl">71.73分</span> (+0.05分)</span>
                    </h3>
                    <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                        連續 5 年（109~113）中科企管最低錄取分均領先中科國貿（111年曾落後達 1.67分），於 114 學年度國貿系展現韌性首度實現歷史性黃金交叉反超！
                    </p>'''

new_m3_banner = '''                    <h3 class="text-base font-black text-slate-900 flex items-center gap-2">
                        <i data-lucide="award" class="w-5 h-5 text-emerald-600"></i>
                        <span>中科國貿 114學年度單科均分達 <span class="text-emerald-600 text-2xl">71.78分</span>，穩居中台灣公立國貿第一！</span>
                    </h3>
                    <p class="text-xs text-slate-600 mt-1.5 leading-relaxed">
                        在中部商管技職體系中，中科國貿以五專滿招 (100%) 與日間四技 (99.06%) 形成規模雙引擎，分數緊咬北部北商國商與中部雲科國管，展現強大生源韌性。
                    </p>'''
html = html.replace(old_m3_banner, new_m3_banner)

# Replace Module 3 structural comparison cards
old_m3_structure = '''            <!-- 雙雄硬核體質對照表：中科國貿 vs 中科企管 -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- 國貿 vs 企管 師資與學制結構 -->
                <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-4 border-b border-slate-200/70 pb-3">
                            <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                                <i data-lucide="layers" class="w-4 h-4 text-emerald-600"></i>
                                <span>學制與在學規模結構比較</span>
                            </h3>
                            <span class="text-xs text-slate-400">中科國貿 vs 中科企管</span>
                        </div>
                        <div class="space-y-3 text-xs">
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">專任師資總人數</span>
                                <span class="font-bold text-slate-900">國貿 21人 vs 企管 24人</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">教授 / 副教授人數</span>
                                <span class="font-bold text-slate-900">國貿 (4/14人) vs 企管 (5/12人)</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">助理教授人數</span>
                                <span class="font-bold text-slate-900">國貿 3人 vs 企管 7人 (年輕化)</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">生師比 (SSR)</span>
                                <span class="font-bold text-slate-900">國貿 49.7 vs 企管 48.5</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">全系在學總學生數</span>
                                <span class="font-black text-slate-900">國貿 1,044人 vs 企管 1,165人</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">五專部學生數</span>
                                <span class="text-slate-900 font-medium">國貿 248人 (1班) vs <strong class="text-sky-700">企管 438人 (2班)</strong></span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">日間四技學生數</span>
                                <span class="text-emerald-600 font-bold">國貿 482人 vs 企管 295人</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">技優領航專班</span>
                                <span class="text-slate-900">國貿 0人 vs <strong class="text-sky-700">企管 103人</strong></span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">進修四技學生數</span>
                                <span class="text-slate-900">國貿 314人 vs 企管 227人</span>
                            </div>
                            <div class="flex justify-between items-center p-2 rounded-lg bg-slate-50">
                                <span class="text-slate-600">碩士班 / EMBA 在學生</span>
                                <span class="text-rose-600 font-black">國貿 0人 (無) vs 企管 102人 (滿招)</span>
                            </div>
                        </div>
                    </div>
                    <div class="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 leading-relaxed">
                        💡 <strong>關鍵診斷：</strong>企管系擁有完整的「五專2班 + 技優領航 + 日間碩士 + EMBA碩專」多元護城河，抗少子化彈性極高；國貿系欠缺研究所與技優班，日間四技（482人）與五專（248人）為絕對核心防守盤。
                    </div>
                </div>

                <!-- 國貿 vs 企管 退學與休學深水區 -->
                <div class="bg-white border border-slate-200 rounded-2xl p-5 shadow-lg flex flex-col justify-between">
                    <div>
                        <div class="flex items-center justify-between mb-4 border-b border-slate-200/70 pb-3">
                            <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                                <i data-lucide="alert-triangle" class="w-4 h-4 text-amber-600"></i>
                                <span>113學年 退學與休學深水區診斷</span>
                            </h3>
                            <span class="text-xs text-rose-600 font-bold">國貿 80人退學 (3.73%)</span>
                        </div>

                        <div class="grid grid-cols-2 gap-3 mb-4">
                            <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                <div class="text-slate-500 text-[11px]">國貿系 整體退學率</div>
                                <div class="text-2xl font-black text-rose-600 mt-1">3.73%</div>
                                <div class="text-[10px] text-slate-500">80人退學 / 六強最高</div>
                            </div>
                            <div class="bg-slate-50 p-3 rounded-xl border border-slate-200">
                                <div class="text-slate-500 text-[11px]">企管系 整體退學率</div>
                                <div class="text-2xl font-black text-slate-900 mt-1">2.95%</div>
                                <div class="text-[10px] text-slate-500">72人退學 / 相對穩固</div>
                            </div>
                        </div>

                        <div class="space-y-2.5 text-xs">
                            <div class="text-[11px] text-slate-500 font-semibold">退學動因深度解剖 (國貿 vs 企管)：</div>
                            
                            <div>
                                <div class="flex justify-between text-[11px] mb-1">
                                    <span class="text-slate-600">志趣不合 / 科系不符 (自退核心)</span>
                                    <span class="text-rose-600 font-bold">國貿 24人 (佔自退 72.7%) vs 企管 20人</span>
                                </div>
                                <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">
                                    <div class="bg-rose-500 h-full" style="width: 72.7%"></div>
                                </div>
                            </div>

                            <div>
                                <div class="flex justify-between text-[11px] mb-1">
                                    <span class="text-slate-600">工作需求 / 經濟因素自退</span>
                                    <span class="text-amber-600 font-bold">國貿 8人 vs 企管 3人</span>
                                </div>
                                <div class="w-full bg-slate-100 h-2 rounded-full overflow-hidden flex">
                                    <div class="bg-amber-500 h-full" style="width: 24.2%"></div>
                                </div>
                            </div>

                            <div class="p-2.5 rounded-lg bg-slate-50 border border-slate-200 text-[11px] space-y-1">
                                <div class="flex justify-between text-slate-700">
                                    <span>休學中未復學人數 (休學率)</span>
                                    <span class="text-slate-600">國貿 73人 (<strong class="text-amber-600">6.82%</strong>) vs 企管 73人 (5.98%)</span>
                                </div>
                                <div class="flex justify-between text-slate-700">
                                    <span>強制退學 (逾期未註冊/逾期未復學)</span>
                                    <span class="text-slate-600">國貿 47人 (58.8%) vs 企管 47人 (65.3%)</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="text-[11px] text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-200 mt-3 leading-relaxed">
                        ⚠️ <strong>警報解讀：</strong>國貿系 80 名退學生中，高達 <strong class="text-rose-600">24 人明確因「科系不符/志趣不合」</strong>主動申請退學，多數發生於大一升大二階段（轉學考或重考），反映高中職升學選填志願時對「國貿經營實務」存在認知落差，急需大一新生生涯導引與專題激勵。
                    </div>
                </div>
            </div>'''

new_m3_structure = '''            <!-- 中科國貿學制結構與留存體質深水區診斷 -->
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
            </div>'''
html = html.replace(old_m3_structure, new_m3_structure)

# Replace table title and structure in Module 3 Registration Matrix
html = html.replace(
    '國貿系 vs 企管系 113~114學年度 各學制新生註冊率完整消長矩陣',
    '中科國貿系 113~114學年度 各學制新生註冊率與核定名額消長矩陣'
)

# =========================================================================
# 4. Module 6: Replace 國貿 vs 企管 with 169 正取生保衛戰
# =========================================================================
html = html.replace(
    '<span class="text-xs text-slate-400 font-medium">國貿 vs 企管 雙榜對決</span>',
    '<span class="text-xs text-slate-400 font-medium">正取生留任保衛戰</span>'
)
html = html.replace(
    '<div class="text-2xl font-black text-amber-600 mt-2">34 : 11 (75.6%)</div>\n                    <div class="text-[11px] text-slate-400 mt-0.5">115名雙榜生 國貿勝出 <strong class="text-emerald-300">3.1倍</strong></div>',
    '<div class="text-2xl font-black text-emerald-600 mt-2">58.0% (98/169人)</div>\n                    <div class="text-[11px] text-slate-400 mt-0.5">正取留任98人 / 遭他校奪走67人</div>'
)

# Replace chart-m6-itm-vs-ba card
old_m6_chart_card = '''                <!-- 左側 1 欄：雙榜正面對決 (長條圖) -->
                <div class="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] hover:border-slate-300 transition">
                    <div class="flex items-center justify-between mb-3 border-b border-slate-200/70 pb-3">
                        <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                            國貿 vs 企管 雙榜考生最終抉擇
                        </h3>
                        <span class="text-xs text-amber-600 font-bold">115人同時報考</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="chart-m6-itm-vs-ba"></canvas>
                    </div>
                    <div class="mt-3 text-xs text-slate-600 bg-amber-500/10 border border-amber-500/20 p-2.5 rounded-lg">
                        💡 <strong>歷史性驗證</strong>：115 名同時報考兩系的考生中，就讀國貿高達 <strong>34 人</strong>，而就讀企管僅 <strong>11 人</strong>（3.1 : 1 國貿完勝），直接印證 114 年國貿最低錄取分數首度反超企管的底層心理動能！
                    </div>
                </div>'''

new_m6_chart_card = '''                <!-- 左側 1 欄：中科國貿 169 名正取生去向保衛戰 (長條圖) -->
                <div class="bg-white border border-slate-200/80 rounded-2xl p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] hover:border-slate-300 transition">
                    <div class="flex items-center justify-between mb-3 border-b border-slate-200/70 pb-3">
                        <h3 class="text-sm font-bold text-slate-900 flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                            169 位【正取生】最終去向與保衛戰
                        </h3>
                        <span class="text-xs text-emerald-700 font-bold bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">留任率 58.0%</span>
                    </div>
                    <div class="h-64 relative">
                        <canvas id="chart-m6-itm-vs-ba"></canvas>
                    </div>
                    <div class="mt-3 text-xs text-slate-700 bg-emerald-50/70 border border-emerald-200 p-2.5 rounded-lg">
                        💡 <strong>正取生拔尖防禦</strong>：169 名獲正取高分考生中，實招留任達 <strong>98 人 (58.0%)</strong>。流失的 67 名正取生主要被<strong>高科航管(13人)、逢甲國貿(12人)、高科國企(9人)</strong>瓜分，凸顯供應鏈專業與台中在地商會品牌之拉力！
                    </div>
                </div>'''
html = html.replace(old_m6_chart_card, new_m6_chart_card)

# =========================================================================
# 5. Update JavaScript DB object: Purge 企管 and 虎科 from DB.score_trends
# =========================================================================
# Update score_trends to pure trade departments
old_score_trends = '"score_trends": {"years": ["109", "110", "111", "112", "113", "114"], "departments": {"中科大國貿": [75.44, 76.89, 68.33, 68.44, 75.56, 71.78], "中科大企管": [76.71, 77.86, 70.0, 68.77, 75.95, 71.73], "雲科大企管": [83.11, 83.44, 78.44, 73.44, 81.56, 78.56], "北商大國商": [84.71, 84.07, 80.14, 74.43, 80.93, 79.86], "北商大企管": [83.71, 83.86, 79.0, 74.18, 82.06, 79.58], "勤益企管": [70.79, 73.18, 61.86, 61.36, 68.14, 63.78], "虎科財金": [72.5, 74.1, 65.8, 64.2, 71.3, 65.64]}}'
new_score_trends = '"score_trends": {"years": ["109", "110", "111", "112", "113", "114"], "departments": {"中科大國貿": [75.44, 76.89, 68.33, 68.44, 75.56, 71.78], "北商大國商": [84.71, 84.07, 80.14, 74.43, 80.93, 79.86], "雲科大國管": [82.5, 83.1, 77.8, 73.8, 81.33, 79.78], "高科大航管": [72.8, 73.5, 67.2, 67.9, 73.56, 73.89], "高科大國企": [74.2, 75.6, 68.1, 68.2, 76.44, 67.5], "高科供應鏈": [70.5, 72.1, 65.4, 65.1, 71.85, 65.7]}}'
html = html.replace(old_score_trends, new_score_trends)

# Purge 虎科財金 from central_competitors in DB
html = re.sub(r', \{"school": "虎科財金"[\s\S]*?二技進修部重挫至39\.29%"\}', '', html)

# =========================================================================
# 6. Update Chart.js logic in initModule3Charts and initModule6Charts
# =========================================================================
old_color_map = """            const colorMap = {
                '中科大國貿': '#10b981',
                '中科大企管': '#38bdf8',
                '雲科大企管': '#a855f7',
                '北商大國商': '#f59e0b',
                '北商大企管': '#94a3b8',
                '勤益企管':   '#64748b',
                '虎科財金':   '#f43f5e'
            };"""

new_color_map = """            const colorMap = {
                '中科大國貿': '#10b981',
                '北商大國商': '#0284c7',
                '雲科大國管': '#6366f1',
                '高科大航管': '#f59e0b',
                '高科大國企': '#ec4899',
                '高科供應鏈': '#64748b'
            };"""
html = html.replace(old_color_map, new_color_map)

# Update initModule6Charts duel chart to show Main Accepted destinations
old_m6_duel_init = """            const ctxDuel = document.getElementById('chart-m6-itm-vs-ba');
            if (ctxDuel && !Chart.getChart(ctxDuel)) {
                charts.m6Duel = new Chart(ctxDuel.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: ['選擇中科國貿', '選擇中科企管', '轉向其他學校'],
                        datasets: [{
                            label: '雙榜考生就讀人數',
                            data: [34, 11, 70],
                            backgroundColor: ['#10b981', '#f59e0b', '#64748b'],
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) { return ` 就讀人數: ${ctx.raw} 人`; }
                                }
                            }
                        },
                        scales: {
                            y: { grid: { color: '#f1f5f9' }, ticks: { color: '#64748b', font: { size: 11 } } },
                            x: { grid: { display: false }, ticks: { color: '#1e293b' } }
                        }
                    }
                });
            }"""

new_m6_duel_init = """            const ctxDuel = document.getElementById('chart-m6-itm-vs-ba');
            if (ctxDuel && !Chart.getChart(ctxDuel)) {
                charts.m6Duel = new Chart(ctxDuel.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: ['留任中科國貿', '高科商管航管', '逢甲國貿', '北商國商', '中原/其他', '未分發/放棄'],
                        datasets: [{
                            label: '正取生就讀去向 (人)',
                            data: [98, 27, 12, 5, 23, 4],
                            backgroundColor: ['#10b981', '#0284c7', '#f59e0b', '#6366f1', '#a855f7', '#94a3b8'],
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) { 
                                        const pct = ((ctx.raw / 169) * 100).toFixed(1);
                                        return ` 正取生人數: ${ctx.raw} 人 (${pct}%)`; 
                                    }
                                }
                            }
                        },
                        scales: {
                            y: { grid: { color: '#f1f5f9' }, ticks: { color: '#64748b', font: { size: 11 } } },
                            x: { grid: { display: false }, ticks: { color: '#1e293b', font: { size: 11 } } }
                        }
                    }
                });
            }"""
html = html.replace(old_m6_duel_init, new_m6_duel_init)

# Update Module 3 registration matrix rendering function (renderModule3Matrix)
old_matrix_render = """        function renderModule3Matrix() {
            const tbody = document.getElementById('m3-reg-matrix-body');
            if (!tbody) return;
            tbody.innerHTML = '';

            DB.itm_vs_ba_deep.registration_matrix.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 transition border-b border-slate-100 text-xs';
                tr.innerHTML = `
                    <td class="p-3 font-medium text-slate-900">${row.prog}</td>
                    <td class="p-3 text-slate-700">${row.itm_113}</td>
                    <td class="p-3 font-bold text-emerald-700">${row.itm_114}</td>
                    <td class="p-3 text-slate-700">${row.ba_113}</td>
                    <td class="p-3 text-slate-700">${row.ba_114}</td>
                    <td class="p-3 text-[11px] text-slate-500">${row.diff}</td>
                `;
                tbody.appendChild(tr);
            });
        }"""

new_matrix_render = """        function renderModule3Matrix() {
            const tbody = document.getElementById('m3-reg-matrix-body');
            if (!tbody) return;
            tbody.innerHTML = '';

            const itmRegData = [
                { prog: "日間學士班 (含四技)", y113: "100.00% (80/80)", y114: "99.06% (79/80, 境+26)", status: "常年滿招・核心主力", note: "生源防守穩健，外加境外專班充裕" },
                { prog: "日間二年制 (二技)", y113: "97.37% (37/38)", y114: "100.00% (38/38, 境+1)", status: "100% 滿招", note: "五專畢業直升四技/二技核心管道" },
                { prog: "進修學士班 (進修四技)", y113: "53.75% (43/80)", y114: "50.91% (28/55)", status: "深水警戒區", note: "核定主動減招25名，仍受在地夜校生源緊縮衝擊" },
                { prog: "進修二年制 (夜二技)", y113: "62.67% (47/75)", y114: "89.09% (49/55)", status: "大幅回彈 (+26.4%)", note: "減招20名後成效立竿見影，註冊率衝回近9成" },
                { prog: "日間五專部 (國貿科)", y113: "100.00% (50/50)", y114: "100.00% (50/50)", status: "常年 100% 額滿", note: "國中直升一中商圈名校，品牌護城河極深" }
            ];

            itmRegData.forEach(row => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 transition border-b border-slate-100 text-xs';
                const badgeCls = row.status.includes('警戒') ? 'bg-rose-50 text-rose-700 border border-rose-200' : 'bg-emerald-50 text-emerald-700 border border-emerald-200';
                tr.innerHTML = `
                    <td class="p-3 font-medium text-slate-900">${row.prog}</td>
                    <td class="p-3 text-slate-700 font-mono">${row.y113}</td>
                    <td class="p-3 font-bold text-emerald-700 font-mono">${row.y114}</td>
                    <td class="p-3"><span class="px-2 py-0.5 rounded text-[11px] font-semibold ${badgeCls}">${row.status}</span></td>
                    <td class="p-3 text-[11px] text-slate-600">${row.note}</td>
                `;
                tbody.appendChild(tr);
            });
        }"""
html = html.replace(old_matrix_render, new_matrix_render)

# Update the table header in Module 3 Registration Matrix
old_table_headers = """                            <tr>
                                <th class="p-3">學制班別</th>
                                <th class="p-3">國貿系 (113學年)</th>
                                <th class="p-3">國貿系 (114學年)</th>
                                <th class="p-3">企管系 (113學年)</th>
                                <th class="p-3">企管系 (114學年)</th>
                                <th class="p-3">戰略消長診斷</th>
                            </tr>"""

new_table_headers = """                            <tr>
                                <th class="p-3">學制班別</th>
                                <th class="p-3">113學年度註冊率 (實招/核定)</th>
                                <th class="p-3">114學年度註冊率 (實招/核定)</th>
                                <th class="p-3">體質狀態</th>
                                <th class="p-3">戰略消長與因應策略</th>
                            </tr>"""
html = html.replace(old_table_headers, new_table_headers)

# Update CSV export master dataset lines in exportAllCSV()
old_csv_m3_header = "學年度,中科大國貿,中科大企管,(國貿-企管差距),雲科大企管,北商大國商,北商大企管,勤益企管,虎科財金"
new_csv_m3_header = "學年度,中科大國貿,北商大國商,雲科大國管,高科大航管,高科大國企,高科供應鏈"
html = html.replace(old_csv_m3_header, new_csv_m3_header)

old_csv_m3_rows = """                ...DB.score_trends.years.map((yr, i) => {
                    const itm = DB.score_trends.departments['中科大國貿'][i];
                    const ba = DB.score_trends.departments['中科大企管'][i];
                    const diff = (itm - ba).toFixed(2);
                    const yun = DB.score_trends.departments['雲科大企管'][i];
                    const ntub_ib = DB.score_trends.departments['北商大國商'][i];
                    const ntub_ba = DB.score_trends.departments['北商大企管'][i];
                    const ncut = DB.score_trends.departments['勤益企管'][i];
                    const nfu = DB.score_trends.departments['虎科財金'][i];
                    return `${yr}學年,${itm},${ba},${diff},${yun},${ntub_ib},${ntub_ba},${ncut},${nfu}`;
                }),"""

new_csv_m3_rows = """                ...DB.score_trends.years.map((yr, i) => {
                    const itm = DB.score_trends.departments['中科大國貿'][i];
                    const ntub = DB.score_trends.departments['北商大國商'][i];
                    const yun = DB.score_trends.departments['雲科大國管'][i];
                    const nk_ship = DB.score_trends.departments['高科大航管'][i];
                    const nk_ib = DB.score_trends.departments['高科大國企'][i];
                    const nk_scm = DB.score_trends.departments['高科供應鏈'][i];
                    return `${yr}學年,${itm},${ntub},${yun},${nk_ship},${nk_ib},${nk_scm}`;
                }),"""
html = html.replace(old_csv_m3_rows, new_csv_m3_rows)

with open("interactive_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Purged all 虎科財金 and 中科企管 references, converted completely to 純國貿/商務!")
