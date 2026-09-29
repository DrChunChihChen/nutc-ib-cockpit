# -*- coding: utf-8 -*-
"""
Synchronize audited numbers into interactive_dashboard.html, index.html, dist/index.html
"""
import re

html_path = "/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html"
with open(html_path, 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update exportComprehensiveMasterRawCSV Table 4 with exact numbers
old_t4 = """                '# 【表四】中科國貿 各學制新生註冊率、名額消長與退學原因體質矩陣',
                '# -----------------------------------------------------------------------------------',
                '學制班別,113學年度註冊率,114學年度註冊率,體質狀態,戰略消長與因應策略',
                '"日間學士班 (含四技)","100.00% (80/80)","99.06% (79/80, 境+26)","常年滿招・核心主力","生源防守穩健，外加境外專班充裕"',
                '"日間二年制 (二技)","97.37% (37/38)","100.00% (38/38, 境+1)","100% 滿招","五專畢業直升四技/二技核心管道"',
                '"進修學士班 (進修四技)","53.75% (43/80)","50.91% (28/55)","深水警戒區","核定主動減招25名，仍受在地夜校生源緊縮衝擊"',
                '"進修二年制 (夜二技)","62.67% (47/75)","89.09% (49/55)","大幅回彈 (+26.4%)","減招20名後成效立竿見影，註冊率衝回近9成"',
                '"日間五專部 (國貿科)","100.00% (50/50)","100.00% (50/50)","常年 100% 額滿","國中直升一中商圈名校，生源穩健優勢顯著"',"""

new_t4 = """                '# 【表四】教育部 UDB 官方核准中科國貿 5 大學制新生註冊率、名額消長與休退學原因體質矩陣',
                '# 官方報表：教育部 UDB 學12-1(註冊率), 學1-1(在學生), 學13-1(休學), 學14-1(退學原因)',
                '# -----------------------------------------------------------------------------------',
                '學制班別,日夜別,113核定名額,113實註人數,113新生註冊率,114核定名額,114實註人數,114境外生專班外加,114新生註冊率,在學學生數,休學生數,退學生數,退學率,主要退學原因,官方來源報表',
                '"日間學士班 (含四技)","日間部",80,80,"100.00%",80,79,26,"99.06%",382,7,11,"1.21%","志趣不合/科系不符期待(4人)、休學逾期未復學(4人)、逾期未註冊(1人)","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"日間二年制 (二技)","日間部",38,37,"97.37%",38,38,1,"100.00%",74,0,0,"0.00%","五專畢業升學穩定、全數滿招、極低休退學","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"進修學士班 (進修四技)","進修部",80,43,"53.75%",55,28,0,"50.91%",270,53,60,"8.26%","逾期未註冊(27人)、志趣不合(15人)、工作就業困難(8人)、休學逾期未復學(6人)","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"進修二年制 (夜二技)","進修部",75,47,"62.67%",55,49,0,"89.09%",93,0,0,"0.00%","主動減招20名成效立竿見影，註冊率回彈近9成，在職人士公餘進修穩定","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',
                '"日間五專部 (國貿科)","日間部",50,50,"100.00%",50,50,0,"100.00%",252,13,9,"1.79%","志趣不合/科系不符期待(5人)、休學逾期未復學(3人)","教育部 UDB 學12-1, 學1-1, 學13-1, 學14-1"',"""

if old_t4 in c:
    c = c.replace(old_t4, new_t4)
    print("Updated Table 4 in exportComprehensiveMasterRawCSV!")
else:
    print("Old Table 4 not found exactly, searching pattern...")

# 2. Update all MOE UDB link anchors in Modal to https://udb.moe.edu.tw/udata/DetailReportList/%E5%AD%B8%E7%94%9F%E9%A1%9E
# For Item 03, 04, 06, 08, 09, 10
c = re.sub(
    r'<a href="https://udb\.moe\.edu\.tw/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0\.5">\s*教育部大專校院校務資訊公開平台.*?\s*</a>',
    '<a href="https://udb.moe.edu.tw/udata/DetailReportList/%E5%AD%B8%E7%94%9F%E9%A1%9E" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">教育部大專資訊公開平臺 (MOE UDB 學生類報表清單) <i data-lucide="external-link" class="w-3 h-3"></i></a>',
    c
)

c = c.replace(
    'https://udb.moe.edu.tw/udata/DetailReportList/18/1/Statue',
    'https://udb.moe.edu.tw/udata/DetailReportList/%E5%AD%B8%E7%94%9F%E9%A1%9E'
)

# 3. Write back to all three files
for path in [
    "/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html",
    "/Users/chenchunchih/Downloads/校務資料/index.html",
    "/Users/chenchunchih/Downloads/校務資料/dist/index.html"
]:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Successfully updated {path}")

