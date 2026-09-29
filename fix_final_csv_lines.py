with open("interactive_dashboard.html", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Replace line 1800
for idx, l in enumerate(lines):
    if "模組 3（系所體質深度診斷）：" in l:
        lines[idx] = '                <li><strong>模組 3（國貿系所體質診斷）：</strong>追蹤全台國立國貿旗艦 6 年統測走勢（中科國貿 71.78分居中台公立國貿之冠），並深度切入五專、四技、進修部學制結構與 80人退學深水區。</li>\n'

# Find lines 2818 to 2840 for Table 3 and Table 4 in exportAllCSV
start_t3 = None
end_t4 = None
for idx, l in enumerate(lines):
    if "=== 表三：近6年" in l:
        start_t3 = idx
    if "=== 表五：教育部" in l:
        end_t4 = idx
        break

if start_t3 is not None and end_t4 is not None:
    new_tables_code = [
        "                '=== 表三：全國國立科大國貿/商務旗艦 6 年統測單科均分走勢 (109~114學年) ===',\n",
        "                '學年度,中科大國貿,北商大國商,雲科大國管,高科大航管,高科大國企,高科供應鏈',\n",
        "                ...DB.score_trends.years.map((y, i) => {\n",
        "                    const itm = DB.score_trends.departments['中科大國貿'][i];\n",
        "                    const ntub = DB.score_trends.departments['北商大國商'][i];\n",
        "                    const yun = DB.score_trends.departments['雲科大國管'][i];\n",
        "                    const ship = DB.score_trends.departments['高科大航管'][i];\n",
        "                    const ib = DB.score_trends.departments['高科大國企'][i];\n",
        "                    const scm = DB.score_trends.departments['高科供應鏈'][i];\n",
        "                    return `${y}學年,${itm},${ntub},${yun},${ship},${ib},${scm}`;\n",
        "                }),\n",
        "                '',\n",
        "                '=== 表四：中科國貿 各學制新生註冊率與名額消長矩陣 ===',\n",
        "                '學制班別,113學年度註冊率,114學年度註冊率,體質狀態,戰略消長與因應策略',\n",
        "                '\"日間學士班 (含四技)\",\"100.00% (80/80)\",\"99.06% (79/80, 境+26)\",\"常年滿招・核心主力\",\"生源防守穩健，外加境外專班充裕\"',\n",
        "                '\"日間二年制 (二技)\",\"97.37% (37/38)\",\"100.00% (38/38, 境+1)\",\"100% 滿招\",\"五專畢業直升四技/二技核心管道\"',\n",
        "                '\"進修學士班 (進修四技)\",\"53.75% (43/80)\",\"50.91% (28/55)\",\"深水警戒區\",\"核定主動減招25名，仍受在地夜校生源緊縮衝擊\"',\n",
        "                '\"進修二年制 (夜二技)\",\"62.67% (47/75)\",\"89.09% (49/55)\",\"大幅回彈 (+26.4%)\",\"減招20名後成效立竿見影，註冊率衝回近9成\"',\n",
        "                '\"日間五專部 (國貿科)\",\"100.00% (50/50)\",\"100.00% (50/50)\",\"常年 100% 額滿\",\"國中直升一中商圈名校，品牌護城河極深\"',\n",
        "                '',\n"
    ]
    lines[start_t3:end_t4] = new_tables_code

with open("interactive_dashboard.html", "w", encoding="utf-8") as f:
    f.writelines(lines)

print("Replaced Table 3 & Table 4 in exportAllCSV successfully!")
