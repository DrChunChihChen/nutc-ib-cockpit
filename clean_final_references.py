with open("interactive_dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Line 356
text = text.replace(
    '114 學年錄取分首度反超中科企管。',
    '114 學年單科均分 71.78 分穩居中台灣公立國貿系所首位。'
)

# 2. Line 1067
text = text.replace(
    '以及在校內國貿 vs 企管正面對決中的壓倒性戰力。',
    '以及 169 位正取生保衛戰中高達 58.0% (98人) 的拔尖留任實力。'
)

# 3. Modal text
text = text.replace(
    '<li><strong>模組 3（系所體質深度診斷）：</strong>中科國貿 vs 中科企管 6年統測走勢（114年國貿以 71.78分首度反超企管 71.73分），並切入 80人退學（科系不符24人）與進修部50.91%深水區。</li>',
    '<li><strong>模組 3（國貿系所體質診斷）：</strong>追蹤全台國立國貿旗艦 6 年統測走勢（中科國貿 71.78分居中台公立國貿之冠），並深度切入五專、四技、進修部學制結構與 80人退學深水區。</li>'
)

# 4. exportAllCSV() logic
old_csv_block = """                '=== 表三：近 6 年統測 09商管群最低錄取折合單科均分走勢 (109~114學年) ===',
                '學年度,中科大國貿,中科大企管,(國貿-企管差距),雲科大企管,北商大國商,北商大企管,勤益企管,虎科財金',
                ...DB.score_trends.years.map((yr, i) => {
                    const itm = DB.score_trends.departments['中科大國貿'][i];
                    const ba = DB.score_trends.departments['中科大企管'][i];
                    const diff = (itm - ba).toFixed(2);
                    const yun = DB.score_trends.departments['雲科大企管'][i];
                    const ntub_ib = DB.score_trends.departments['北商大國商'][i];
                    const ntub_ba = DB.score_trends.departments['北商大企管'][i];
                    const ncut = DB.score_trends.departments['勤益企管'][i];
                    const nfu = DB.score_trends.departments['虎科財金'][i];
                    return `${yr}學年,${itm},${ba},${diff},${yun},${ntub_ib},${ntub_ba},${ncut},${nfu}`;
                }),
                '',
                '=== 表四：中科國貿 vs 企管 各學制註冊率詳細消長矩陣 ===',
                '學制班別,國貿系113註冊率,國貿系114註冊率,企管系113註冊率,企管系114註冊率,體質差異分析',
                ...DB.itm_vs_ba_deep.registration_matrix.map(r => [
                    `"${r.prog}"`, `"${r.itm_113}"`, `"${r.itm_114}"`, `"${r.ba_113}"`, `"${r.ba_114}"`, `"${r.diff}"`
                ].join(',')),"""

new_csv_block = """                '=== 表三：全國國立科大國貿/商務旗艦 6 年統測單科均分走勢 (109~114學年) ===',
                '學年度,中科大國貿,北商大國商,雲科大國管,高科大航管,高科大國企,高科供應鏈',
                ...DB.score_trends.years.map((yr, i) => {
                    const itm = DB.score_trends.departments['中科大國貿'][i];
                    const ntub = DB.score_trends.departments['北商大國商'][i];
                    const yun = DB.score_trends.departments['雲科大國管'][i];
                    const ship = DB.score_trends.departments['高科大航管'][i];
                    const ib = DB.score_trends.departments['高科大國企'][i];
                    const scm = DB.score_trends.departments['高科供應鏈'][i];
                    return `${yr}學年,${itm},${ntub},${yun},${ship},${ib},${scm}`;
                }),
                '',
                '=== 表四：中科國貿 各學制新生註冊率與名額消長矩陣 ===',
                '學制班別,113學年度註冊率,114學年度註冊率,體質狀態,戰略消長與因應策略',
                '"日間學士班 (含四技)","100.00% (80/80)","99.06% (79/80, 境+26)","常年滿招・核心主力","生源防守穩健，外加境外專班充裕"',
                '"日間二年制 (二技)","97.37% (37/38)","100.00% (38/38, 境+1)","100% 滿招","五專畢業直升四技/二技核心管道"',
                '"進修學士班 (進修四技)","53.75% (43/80)","50.91% (28/55)","深水警戒區","核定主動減招25名，仍受在地夜校生源緊縮衝擊"',
                '"進修二年制 (夜二技)","62.67% (47/75)","89.09% (49/55)","大幅回彈 (+26.4%)","減招20名後成效立竿見影，註冊率衝回近9成"',
                '"日間五專部 (國貿科)","100.00% (50/50)","100.00% (50/50)","常年 100% 額滿","國中直升一中商圈名校，品牌護城河極深"',"""

text = text.replace(old_csv_block, new_csv_block)

with open("interactive_dashboard.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Final cleanup complete!")
