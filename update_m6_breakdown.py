import re

with open("interactive_dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update header badge and explanation
content = content.replace(
    '<span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-50 text-purple-700 border border-purple-200 border border-purple-500/40">113甄選全量實證母體</span>',
    '<span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-purple-50 text-purple-700 border border-purple-200">113~115 三學年度甄選累計母體</span>'
)

content = content.replace(
    '<span class="text-xs text-slate-400">教育部四技二專聯合甄選交叉查榜全量 504 筆</span>',
    '<span class="text-xs text-slate-500 font-medium">教育部四技二專甄選交叉查榜三年累計 504 筆 (每年約165~172人次，實招約56人/年)</span>'
)

content = content.replace(
    '掌握中科國貿 504 位正備取考生的微觀分發去向，精準診斷生源究竟被「高科大、逢甲大學、北商大」挖走幾名學生',
    '掌握中科國貿 113~115 三學年度共 504 位正備取考生的微觀分發去向（113年163人、114年172人、115年169人），精準診斷生源究竟被「高科大、逢甲大學、北商大」挖走幾名學生（含三年累計與單年拆解）'
)

# 2. Update Poachers Chart Header
content = content.replace(
    '掠奪中科國貿生源之「前十大天敵校系」排行榜',
    '掠奪中科國貿生源之「前十大天敵校系」排行榜 (3年累計)'
)

content = content.replace(
    '<p class="text-xs text-slate-400 mt-0.5">統計中科國貿正備取生最終「棄中科、就讀他校系」之確切人數</p>',
    '<p class="text-xs text-slate-500 mt-0.5">統計 113~115 三學年度正備取生最終棄中科就讀他校總人次（高科航管年均約12人、高科國企年均約7人、逢甲年均約7人）</p>'
)

# 3. Add Breakdown Table right below the poachers chart inside the same card
breakdown_table_html = '''
                    <!-- 天敵跨年度拆解明細表 (Yearly Breakdown) -->
                    <div class="mt-4 pt-3 border-t border-slate-100">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                                <i data-lucide="table" class="w-3.5 h-3.5 text-slate-500"></i>
                                前十大天敵跨年度 (113~115) 逐年拆解與錄取身分剖析
                            </span>
                            <span class="text-[11px] text-slate-500">單位：人次</span>
                        </div>
                        <div class="overflow-x-auto rounded-lg border border-slate-200">
                            <table class="w-full text-left text-xs border-collapse">
                                <thead class="bg-slate-50 text-slate-700 font-semibold border-b border-slate-200">
                                    <tr>
                                        <th class="p-2">排名</th>
                                        <th class="p-2">天敵校系全名</th>
                                        <th class="p-2 text-right">3年累計</th>
                                        <th class="p-2 text-right">113年</th>
                                        <th class="p-2 text-right">114年</th>
                                        <th class="p-2 text-right">115年</th>
                                        <th class="p-2 text-right">正取被奪</th>
                                        <th class="p-2 text-right">備取被奪</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-slate-100 text-slate-700">
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2 font-bold text-rose-600">#1</td>
                                        <td class="p-2 font-medium text-slate-900">國立高雄科技大學 航運管理系</td>
                                        <td class="p-2 text-right font-black text-rose-600">37</td>
                                        <td class="p-2 text-right font-mono">11</td>
                                        <td class="p-2 text-right font-mono">15</td>
                                        <td class="p-2 text-right font-mono">11</td>
                                        <td class="p-2 text-right font-mono font-semibold text-amber-700">13</td>
                                        <td class="p-2 text-right font-mono text-slate-500">4</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2 font-bold text-rose-600">#2</td>
                                        <td class="p-2 font-medium text-slate-900">國立高雄科技大學 國際企業系</td>
                                        <td class="p-2 text-right font-black text-rose-600">22</td>
                                        <td class="p-2 text-right font-mono">9</td>
                                        <td class="p-2 text-right font-mono">7</td>
                                        <td class="p-2 text-right font-mono">6</td>
                                        <td class="p-2 text-right font-mono font-semibold text-amber-700">9</td>
                                        <td class="p-2 text-right font-mono text-slate-500">3</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2 font-bold text-amber-600">#3</td>
                                        <td class="p-2 font-medium text-slate-900">逢甲大學 國際經營與貿易學系</td>
                                        <td class="p-2 text-right font-black text-amber-600">20</td>
                                        <td class="p-2 text-right font-mono">6</td>
                                        <td class="p-2 text-right font-mono">7</td>
                                        <td class="p-2 text-right font-mono">7</td>
                                        <td class="p-2 text-right font-mono font-semibold text-rose-700 font-bold">12 (60%)</td>
                                        <td class="p-2 text-right font-mono text-slate-500">4</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2 font-bold text-slate-500">#4</td>
                                        <td class="p-2 font-medium text-slate-900">國立高雄科技大學 行銷與流通管理系</td>
                                        <td class="p-2 text-right font-bold">12</td>
                                        <td class="p-2 text-right font-mono">7</td>
                                        <td class="p-2 text-right font-mono">4</td>
                                        <td class="p-2 text-right font-mono">1</td>
                                        <td class="p-2 text-right font-mono text-amber-700">5</td>
                                        <td class="p-2 text-right font-mono text-slate-500">4</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2 font-bold text-slate-500">#5</td>
                                        <td class="p-2 font-medium text-slate-900">國立高雄科技大學 運籌管理系</td>
                                        <td class="p-2 text-right font-bold">12</td>
                                        <td class="p-2 text-right font-mono">4</td>
                                        <td class="p-2 text-right font-mono">4</td>
                                        <td class="p-2 text-right font-mono">4</td>
                                        <td class="p-2 text-right font-mono text-amber-700">1</td>
                                        <td class="p-2 text-right font-mono text-slate-500">5</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2 font-bold text-slate-500">#6</td>
                                        <td class="p-2 font-medium text-slate-900">國立臺北商業大學 國際商務系</td>
                                        <td class="p-2 text-right font-bold">10</td>
                                        <td class="p-2 text-right font-mono">5</td>
                                        <td class="p-2 text-right font-mono">2</td>
                                        <td class="p-2 text-right font-mono">3</td>
                                        <td class="p-2 text-right font-mono font-semibold text-amber-700">5 (50%)</td>
                                        <td class="p-2 text-right font-mono text-slate-500">0</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2 font-bold text-slate-500">#7</td>
                                        <td class="p-2 font-medium text-slate-900">中原大學 國際經營與貿易學系</td>
                                        <td class="p-2 text-right font-bold">9</td>
                                        <td class="p-2 text-right font-mono">5</td>
                                        <td class="p-2 text-right font-mono">2</td>
                                        <td class="p-2 text-right font-mono">2</td>
                                        <td class="p-2 text-right font-mono text-amber-700">3</td>
                                        <td class="p-2 text-right font-mono text-slate-500">1</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2 font-bold text-slate-500">#8</td>
                                        <td class="p-2 font-medium text-slate-900">國立臺北護理健康大學 健康事業管理系</td>
                                        <td class="p-2 text-right font-bold">6</td>
                                        <td class="p-2 text-right font-mono">3</td>
                                        <td class="p-2 text-right font-mono">2</td>
                                        <td class="p-2 text-right font-mono">1</td>
                                        <td class="p-2 text-right font-mono text-amber-700">2</td>
                                        <td class="p-2 text-right font-mono text-slate-500">3</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2 font-bold text-slate-500">#9</td>
                                        <td class="p-2 font-medium text-slate-900">銘傳大學 國際企業學系(台北)</td>
                                        <td class="p-2 text-right font-bold">6</td>
                                        <td class="p-2 text-right font-mono">1</td>
                                        <td class="p-2 text-right font-mono">3</td>
                                        <td class="p-2 text-right font-mono">2</td>
                                        <td class="p-2 text-right font-mono text-slate-500">0</td>
                                        <td class="p-2 text-right font-mono text-slate-500">3</td>
                                    </tr>
                                    <tr class="hover:bg-slate-50">
                                        <td class="p-2 font-bold text-slate-500">#10</td>
                                        <td class="p-2 font-medium text-slate-900">國立高雄科技大學 金融系</td>
                                        <td class="p-2 text-right font-bold">6</td>
                                        <td class="p-2 text-right font-mono">1</td>
                                        <td class="p-2 text-right font-mono">3</td>
                                        <td class="p-2 text-right font-mono">2</td>
                                        <td class="p-2 text-right font-mono text-slate-500">0</td>
                                        <td class="p-2 text-right font-mono text-slate-500">1</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
'''

content = content.replace('                    <div class="h-80 relative">\n                        <canvas id="chart-m6-top-poachers"></canvas>\n                    </div>\n                </div>',
                          '                    <div class="h-80 relative">\n                        <canvas id="chart-m6-top-poachers"></canvas>\n                    </div>' + breakdown_table_html + '\n                </div>')

with open("interactive_dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated Module 6 with explicit 113~115 breakdown table and updated titles!")
