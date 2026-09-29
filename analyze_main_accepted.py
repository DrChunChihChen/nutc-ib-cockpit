import csv
from collections import Counter

with open("/Users/chenchunchih/Downloads/ntcust_flow_all_113_115.csv", "r", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

itm = [r for r in rows if r.get("來源系所代碼") == "113001"]
mains = [r for r in itm if "正取" in r.get("頁面狀態", "")]
print(f"Total 正取生: {len(mains)}")

dest_cats = Counter(r.get("去向分類") for r in mains)
print("正取生去向分類:", dest_cats)

poached_depts = Counter()
for r in mains:
    if r.get("去向分類") == "其他學校":
        sch = r.get("最後分發學校", "").strip()
        dept = r.get("最後分發系所", "").strip()
        name = f"{sch} {dept}".strip() if dept else sch
        poached_depts[name] += 1

print("\n【正取生被奪校系排行 (Top Poachers of Main Candidates)】:")
for d, cnt in poached_depts.most_common(10):
    print(f"  • {d}: 奪走 {cnt} 名正取生")
