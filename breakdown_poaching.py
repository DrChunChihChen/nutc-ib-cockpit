import csv
from collections import Counter

csv_path = "/Users/chenchunchih/Downloads/ntcust_flow_all_113_115.csv"

with open(csv_path, "r", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

itm = [r for r in rows if r.get("來源系所代碼") == "113001"]

print(f"=== 國立臺中科技大學 國際貿易與經營系 (113001) 查榜全量數據結構 ===")
print(f"總筆數 (Rows): {len(itm)}")
years = sorted(list(set(r.get("年度", "") for r in itm)))
print(f"涵蓋年度: {years}\n")

# 1. 年度 breakdown
print("1. 【各年度樣本數 Breakdown】:")
for y in years:
    sub = [r for r in itm if r.get("年度") == y]
    dest_c = Counter(r.get("去向分類") for r in sub)
    retained = dest_c.get("原系留任", 0)
    poached = dest_c.get("其他學校", 0)
    unplaced = dest_c.get("未顯示分發", 0)
    print(f"   • {y} 學年度: 總計 {len(sub)} 人 (留任: {retained}, 流失他校: {poached}, 未顯示/未報到: {unplaced})")

# 2. 來源狀態 breakdown (正取 vs 備取)
print("\n2. 【來源錄取身分 Breakdown (全期累計)】:")
def get_status_type(st):
    if not st: return "未標註/其他"
    if "正取" in st: return "正取生"
    if "備取" in st: return "備取生"
    return "其他"

status_group = Counter(get_status_type(r.get("頁面狀態")) for r in itm)
for k, v in status_group.items():
    print(f"   • {k}: {v} 人")

# 3. 前十大天敵校系跨年度 Breakdown
print("\n3. 【前十大天敵校系：年度 Breakdown 與 正/備取身分】:")

dept_all = Counter()
for r in itm:
    sch = r.get("最後分發學校", "").strip()
    dept = r.get("最後分發系所", "").strip()
    if sch and "臺中科技" not in sch:
        full_d = f"{sch} {dept}" if dept else sch
        dept_all[full_d] += 1

top10 = dept_all.most_common(10)

header = f"{'排名':<4} | {'天敵校系':<30} | {'3年累計':<6} | {'113年':<5} | {'114年':<5} | {'115年':<5} | {'正取被奪':<6} | {'備取被奪':<6}"
print(header)
print("-" * len(header.encode('gbk', 'ignore')))

for rank, (d, total_cnt) in enumerate(top10, 1):
    sub_d = [r for r in itm if (f"{r.get('最後分發學校', '').strip()} {r.get('最後分發系所', '').strip()}".strip() == d) or (r.get('最後分發學校', '').strip() == d)]
    c_113 = sum(1 for r in sub_d if r.get("年度") == "113")
    c_114 = sum(1 for r in sub_d if r.get("年度") == "114")
    c_115 = sum(1 for r in sub_d if r.get("年度") == "115")
    
    c_main = sum(1 for r in sub_d if "正取" in r.get("頁面狀態", ""))
    c_reserve = sum(1 for r in sub_d if "備取" in r.get("頁面狀態", ""))
    c_unknown = total_cnt - c_main - c_reserve
    
    print(f"{rank:<4} | {d:<30} | {total_cnt:<6} | {c_113:<5} | {c_114:<5} | {c_115:<5} | {c_main:<6} | {c_reserve:<6}")

print("\n4. 【學校別掠奪總量 (School Level Poaching)】:")
sch_counts = Counter()
for r in itm:
    sch = r.get("最後分發學校", "").strip()
    if sch and "臺中科技" not in sch:
        sch_counts[sch] += 1

for s, cnt in sch_counts.most_common(6):
    print(f"   • {s}: 累計奪走 {cnt} 人")
