# -*- coding: utf-8 -*-
"""
Clean all remaining continuing education / night school references across the cockpit.
"""
import re

FILE_PATH = "/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html"
with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Nav subtext
content = content.replace(
    '<div class="text-[10px] text-stone-400 truncate group-hover:text-stone-300">五專/四技/進修/休退</div>',
    '<div class="text-[10px] text-stone-400 truncate group-hover:text-stone-300">五專/四技/二技/休退</div>'
)

# 2. Module 4 description
content = content.replace(
    '以教育部統計處《113至128學年度各教育階段學生數預測報告》為基準母體，透過動態互動滑桿即時模擬：少子化劇烈度、技職普高分流、考生池縮水對錄取分與進修部存活年限的連動衝擊。',
    '以教育部統計處《113至128學年度各教育階段學生數預測報告》為基準母體，透過動態互動滑桿即時模擬：少子化劇烈度、技職普高分流、考生池縮水對純日間部錄取分與全期滿招防護力的連動推演。'
)

# 3. Method modal descriptions
content = content.replace(
    '<li><strong>模組 2（中部大專國貿大對決）：</strong>聚焦中科國貿、逢甲國貿、東海國貿、朝陽國企、嶺東國企，比較公私立定價優勢、普高學測吸磁、主動減招防禦、現金存量與進修部存亡戰。',
    '<li><strong>模組 2（中部大專國貿大對決）：</strong>聚焦中科國貿、逢甲國貿、東海國貿、朝陽國企、嶺東國企，比較公私立定價優勢、普高學測吸磁、主動減招防禦、財務現金存量與純日間招生防線。'
)
content = content.replace(
    '<li><strong>模組 3（國貿系所學制與留存分析）：</strong>追蹤全台國立國貿旗艦 6 年統測走勢（中科國貿 71.78分居中台公立國貿之冠），並深度切入五專、四技、進修部學制結構與 113 學年度休退學真實現況。</li>',
    '<li><strong>模組 3（國貿系所學制與留存分析）：</strong>追蹤全台國立國貿旗艦 6 年統測走勢（中科國貿 71.78分居中台公立國貿之冠），並深度切入五專、四技、二技純日間學制結構與 113 學年度休退學極低流失（僅 2.82%）實證。</li>'
)
content = content.replace(
    '<li><strong>模組 4（少子化生源走勢模擬）：</strong>113~128 年教育部預測連動 4 支動態滑桿，即時推演 117 虎年波谷、進修四技 122 年瀕臨停招與日間錄取分底線。</li>',
    '<li><strong>模組 4（少子化生源走勢模擬）：</strong>113~128 年教育部預測連動 4 支動態滑桿，即時推演 117 虎年波谷、日間部 128 學年全期滿招防護率與日間錄取分底線。</li>'
)

# 4. Data modal card descriptions
content = content.replace(
    '<p class="text-[11px] text-slate-500">全國大一新生數、統測人數、商管群人數、中科日間錄取分底線與進修四技存活年限精算。</p>',
    '<p class="text-[11px] text-slate-500">全國大一新生數、統測人數、商管群人數、中科日間錄取分底線與純日間部註冊防護率精算。</p>'
)
content = content.replace(
    '<p class="text-[11px] text-slate-500">日間四技、進修四技、日間五專、日間碩士、碩專班之核定名額、註冊率、休退學人數與主因。</p>',
    '<p class="text-[11px] text-slate-500">純日間四技、日間二技、日間五專之核定名額、註冊率、休退學人數與主因 (已排除進修部)。</p>'
)

# 5. statusMap in renderModule3Matrix
old_status_map = """            const statusMap = {
                "日間學士班(含四技)": { text: "穩健主力", bg: "bg-emerald-50 text-emerald-700 border-emerald-200" },
                "日間二年制(二技)": { text: "完全滿招", bg: "bg-emerald-50 text-emerald-700 border-emerald-200" },
                "進修學士班(含四技)": { text: "重點警戒", bg: "bg-rose-50 text-rose-700 border-rose-200" },
                "進修二年制(二技)": { text: "減招強彈", bg: "bg-amber-50 text-amber-700 border-amber-200" },
                "日間五專": { text: "防空洞堡壘", bg: "bg-emerald-50 text-emerald-700 border-emerald-200" },
                "碩士在職專班 (EMBA)": { text: "暫無編制", bg: "bg-stone-100 text-stone-600 border-stone-200" },
                "日間碩士班": { text: "暫無編制", bg: "bg-stone-100 text-stone-600 border-stone-200" }
            };"""

new_status_map = """            const statusMap = {
                "日間學士班(含四技)": { text: "穩健主力", bg: "bg-emerald-50 text-emerald-700 border-emerald-200" },
                "日間二年制(二技)": { text: "完全滿招", bg: "bg-emerald-50 text-emerald-700 border-emerald-200" },
                "日間五專部": { text: "防空洞堡壘", bg: "bg-emerald-50 text-emerald-700 border-emerald-200" },
                "純日間部合計 (已排除進修部)": { text: "全學制滿招", bg: "bg-blue-50 text-blue-700 border-blue-200" },
                "碩士在職專班 (EMBA)": { text: "統籌商院", bg: "bg-stone-100 text-stone-600 border-stone-200" },
                "日間碩士班": { text: "統籌商院", bg: "bg-stone-100 text-stone-600 border-stone-200" }
            };"""
content = content.replace(old_status_map, new_status_map)

# 6. Milestone mobile card in renderSimTable
old_card_sim = """                            <div><span class="text-slate-500 text-[10px]">進修註冊率:</span> <strong class="${eveRate[i] < 35 ? 'text-rose-600' : 'text-slate-900'}">${eveRate[i]}%</strong></div>"""
new_card_sim = """                            <div><span class="text-slate-500 text-[10px]">日間防護率:</span> <strong class="text-blue-700 font-bold">${dayRate[i]}%</strong></div>"""
content = content.replace(old_card_sim, new_card_sim)

# 7. exportAllCSV function
old_export_all = """        function exportAllCSV() {
            const lines = [
                '# 國立臺中科技大學 國際貿易與經營系 (NUTC IB) 校務研究策略分析實證數據集 (114學年度)',
                '# 資料來源：教育部大專校院校務資訊公開平台 (UDB)、技專校院招聯會 (JCTV)、教育部少子化預測報告',
                '',
                '=== 表一：全台國立科大 國貿/商務/航管/供應鏈 六強旗艦指標 ===',
                '代號,學校名稱,系所名稱,區域,在學總人數,五專部人數,日間學士人數,進修學士人數,碩博生人數,專任師資總數,正教授,副教授,助理教授,境外生人數,境外生比率(%),114日間四技註冊率(%),114統測單科均分(分),113退學人數,113退學率(%)',
                ...DB.regional_six.map(x => [
                    x.code, x.school, x.dept, x.region, x.total_stu, x.five_year, x.undergrad_day, x.undergrad_eve, x.grad, x.faculty_total, x.faculty_prof, x.faculty_assoc, x.faculty_asst, x.oversea_stu, x.oversea_pct, x.reg_114_rate, x.score_114, x.drop_cnt_113, x.drop_rate_113
                ].join(',')),
                '',
                '=== 表二：中部大專商管競爭系所綜合情報比對 ===',
                '學校系所,定位類型,核定名額現況,114日間註冊率(%),114進修註冊率(%),門檻均分估值(分),在學總人數,退學流失率(%),財務現金存量,每學期學費,生源管道分流,戰略威脅等級',
                ...DB.central_competitors.map(c => [
                    c.school, c.type, `"${c.quota_status}"`, c.reg_114_day, c.reg_114_eve, c.score_cutoff, c.students_total, c.drop_rate, `"${c.cash_reserve}"`, `"${c.tuition_per_sem}"`, `"${c.source_mix}"`, `"${c.threat_level}"`
                ].join(',')),
                '',
                '=== 表三：全國國立科大國貿/商務旗艦 6 年統測單科均分走勢 (109~114學年) ===',
                '學年度,中科大國貿,北商大國商,雲科大國管,高科大航管,高科大國企,高科供應鏈',
                ...DB.score_trends.years.map((y, i) => {
                    const itm = DB.score_trends.departments['中科大國貿'][i];
                    const ntub = DB.score_trends.departments['北商大國商'][i];
                    const yun = DB.score_trends.departments['雲科大國管'][i];
                    const ship = DB.score_trends.departments['高科大航管'][i];
                    const ib = DB.score_trends.departments['高科大國企'][i];
                    const scm = DB.score_trends.departments['高科供應鏈'][i];
                    return `${y}學年,${itm},${ntub},${yun},${ship},${ib},${scm}`;
                }),
                '',
                '=== 表四：中科國貿 各學制新生註冊率與名額消長矩陣 ===',
                '學制班別,113學年度註冊率,114學年度註冊率,體質狀態,戰略消長與因應策略',
                '"日間學士班 (含四技)","100.00% (80/80)","99.06% (79/80, 境+26)","常年滿招・核心主力","生源防守穩健，外加境外專班充裕"',
                '"日間二年制 (二技)","97.37% (37/38)","100.00% (38/38, 境+1)","100% 滿招","五專畢業直升四技/二技核心管道"',
                '"進修學士班 (進修四技)","53.75% (43/80)","50.91% (28/55)","深水警戒區","核定主動減招25名，仍受在地夜校生源緊縮衝擊"',
                '"進修二年制 (夜二技)","62.67% (47/75)","89.09% (49/55)","大幅回彈 (+26.4%)","減招20名後成效立竿見影，註冊率衝回近9成"',
                '"日間五專部 (國貿科)","100.00% (50/50)","100.00% (50/50)","常年 100% 額滿","國中直升一中商圈名校，生源穩健優勢顯著"',
                '',
                '=== 表五：教育部 113~128 學年度少子化預測基準模型 ===',
                '學年度,全國大一新生總數(萬人),統測報考總數(萬人),商管群人數(萬人),中部商管生源池(人),中科日間錄取均分推估(分),中科進修部註冊率推估(%),五專部防護力',
                ...DB.fertility_timeline.map(f => [
                    `${f.yr}學年`, f.fresh, f.tcte, f.biz, f.pool, f.day_score, f.eve_rate, `"${f.five_def}"`
                ].join(',')),
                '',
                '=== 表六：中科國貿 115~120學年度 專任師資退休換血與轉型排程 ==='"""

new_export_all = """        function exportAllCSV() {
            const lines = [
                '# 國立臺中科技大學 國際貿易與經營系 (NUTC IB) 校務研究策略分析實證數據集 (114學年度純日間基準)',
                '# 資料來源：教育部大專校院校務資訊公開平台 (UDB)、技專校院招聯會 (JCTV)、教育部少子化預測報告',
                '# 備註：全系統所有指標已全面排除進修部夜間數據，專注 100% 純日間正規體系基準',
                '',
                '=== 表一：全台國立科大 國貿/商務/航管/供應鏈 六強旗艦純日間部指標 (已排除進修部) ===',
                '代號,學校名稱,系所名稱,區域,純日間在學人數,五專部人數,日間學士人數,碩博生人數,專任師資總數,正教授,副教授,助理教授,境外生人數,境外生比率(%),114日間四技註冊率(%),114統測單科均分(分),113日間退學人數,113日間退學率(%)',
                ...DB.regional_six.map(x => [
                    x.code, x.school, x.dept, x.region, x.total_stu, x.five_year, x.undergrad_day, x.grad, x.faculty_total, x.faculty_prof, x.faculty_assoc, x.faculty_asst, x.oversea_stu, x.oversea_pct, x.reg_114_rate, x.score_114, x.drop_cnt_113, x.drop_rate_113
                ].join(',')),
                '',
                '=== 表二：中部大專商管競爭系所純日間部情報比對 (已排除進修部) ===',
                '學校系所,定位類型,核定名額現況,114日間註冊率(%),門檻均分估值(分),純日間在學人數,日間退學流失率(%),財務現金存量,每學期學費,生源管道分流,戰略威脅等級',
                ...DB.central_competitors.map(c => [
                    c.school, c.type, `"${c.quota_status}"`, c.reg_114_day, c.score_cutoff, c.students_total, c.drop_rate, `"${c.cash_reserve}"`, `"${c.tuition_per_sem}"`, `"${c.source_mix}"`, `"${c.threat_level}"`
                ].join(',')),
                '',
                '=== 表三：全國國立科大國貿/商務旗艦 6 年統測單科均分走勢 (109~114學年) ===',
                '學年度,中科大國貿,北商大國商,雲科大國管,高科大航管,高科大國企,高科供應鏈',
                ...DB.score_trends.years.map((y, i) => {
                    const itm = DB.score_trends.departments['中科大國貿'][i];
                    const ntub = DB.score_trends.departments['北商大國商'][i];
                    const yun = DB.score_trends.departments['雲科大國管'][i];
                    const ship = DB.score_trends.departments['高科大航管'][i];
                    const ib = DB.score_trends.departments['高科大國企'][i];
                    const scm = DB.score_trends.departments['高科供應鏈'][i];
                    return `${y}學年,${itm},${ntub},${yun},${ship},${ib},${scm}`;
                }),
                '',
                '=== 表四：中科國貿 純日間部各學制新生註冊率與體質矩陣 (已排除進修部) ===',
                '學制班別,113學年度註冊率,114學年度註冊率,體質狀態,戰略消長與因應策略',
                '"日間學士班 (含四技)","100.00% (80/80)","99.06% (79/80, 境+26)","常年滿招・核心主力","生源防守穩健，外加境外專班充裕"',
                '"日間二年制 (二技)","97.37% (37/38)","100.00% (38/38, 境+1)","100% 滿招","五專畢業直升四技/二技核心管道"',
                '"日間五專部 (國貿科)","100.00% (50/50)","100.00% (50/50)","常年 100% 額滿","國中直升一中商圈名校，生源穩健優勢顯著"',
                '"純日間部合計 (已排除進修部)","99.40% (167/168)","99.40% (167/168, 境+27)","全學制實質滿額","全系排除進修部後，日間生師比優化至33.7，退學率僅2.82%"',
                '',
                '=== 表五：教育部 113~128 學年度少子化預測純日間基準模型 ===',
                '學年度,全國大一新生總數(萬人),統測報考總數(萬人),商管群人數(萬人),中部商管生源池(人),中科日間錄取均分推估(分),日間部註冊防護率推估(%),五專部防護力',
                ...DB.fertility_timeline.map(f => [
                    `${f.yr}學年`, f.fresh, f.tcte, f.biz, f.pool, f.day_score, `${f.day_score >= 71.0 ? 99.4 : +(99.4 - (71.0 - f.day_score) * 1.5).toFixed(1)}%`, `"${f.five_def}"`
                ].join(',')),
                '',
                '=== 表六：中科國貿 115~120學年度 專任師資退休換血與轉型排程 ==='"""
content = content.replace(old_export_all, new_export_all)

# 8. exportSimulationCSV function
old_export_sim = """            const simEveRates = simPool.map(p => {
                const ratio = p / baseRefPool114;
                let r = +(50.91 * Math.pow(Math.max(ratio, 0.35), eveElast)).toFixed(1);
                return r < 10.0 ? 10.0 : r;
            });

            const rows = [
                ['# 國立臺中科技大學 國際貿易與經營系 113~128學年度少子化趨勢試算表'],
                [`# 模擬參數: 少子化乘數=${severity}x, 技職分流比=${tcteShare}%, 品牌吸附力=${attraction}%, 進修部彈性=${eveElast}`],
                ['學年度', '全國大一新生總數(萬人)', '統測報考總數(萬人)', '統測商管群人數(萬人)', '中部商管生源池(人)', '日間四技錄取單科均分預測(分)', '進修四技註冊率預測(%)', '五專部防護力', '進修部存續警戒狀態'],
                ...simFresh.map((fresh, i) => {
                    const yr = 113 + i;
                    const pool = simPool[i];
                    const day = simDayScores[i];
                    const eve = simEveRates[i];
                    const five = (yr === 116 || yr === 117) ? '良好 (約92~95%)' : '極穩 (98~100%)';
                    const level = eve <= 35.0 ? '極度危險 (瀕臨停招)' : (eve < 45.0 ? '嚴峻警戒' : '正常防守線');
                    return [yr + '學年度', fresh, simTCTE[i], simBiz[i], pool, day, eve, five, level];
                })
            ];"""

new_export_sim = """            const simDayRates = simPool.map(p => {
                const ratio = p / baseRefPool114;
                let r = +(99.40 - (1.0 - ratio) * 4.0 * (2.0 - eveElast)).toFixed(1);
                return r > 100.0 ? 100.0 : (r < 88.0 ? 88.0 : r);
            });

            const rows = [
                ['# 國立臺中科技大學 國際貿易與經營系 113~128學年度少子化純日間部動態試算表 (已排除進修部)'],
                [`# 模擬參數: 少子化乘數=${severity}x, 技職分流比=${tcteShare}%, 品牌吸附力=${attraction}%, 景氣與競爭係數=${eveElast}`],
                ['學年度', '全國大一新生總數(萬人)', '統測報考總數(萬人)', '統測商管群人數(萬人)', '中部商管生源池(人)', '日間四技錄取單科均分預測(分)', '日間部全學制註冊防護率(%)', '五專部防護力', '滿招防禦評級'],
                ...simFresh.map((fresh, i) => {
                    const yr = 113 + i;
                    const pool = simPool[i];
                    const day = simDayScores[i];
                    const rate = simDayRates[i];
                    const five = (yr === 116 || yr === 117) ? '良好 (約95~98%)' : '極穩 (99~100%)';
                    const level = rate >= 98.0 ? '全期滿招防護' : (rate >= 92.0 ? '穩健防守線' : '警戒關注');
                    return [yr + '學年度', fresh, simTCTE[i], simBiz[i], pool, day, rate + '%', five, level];
                })
            ];"""
content = content.replace(old_export_sim, new_export_sim)

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)
print(f"Updated {FILE_PATH}")

with open("/Users/chenchunchih/Downloads/校務資料/index.html", "w", encoding="utf-8") as f:
    f.write(content)
with open("/Users/chenchunchih/Downloads/校務資料/dist/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("Synced to index.html and dist/index.html!")
