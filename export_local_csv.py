import csv

with open("/Users/chenchunchih/Downloads/ntcust_flow_all_113_115.csv", "r", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

itm = [r for r in rows if r.get("來源系所代碼") == "113001"]

output_path = "/Users/chenchunchih/Downloads/NUTC_ITM_Cross_Admission_Poaching_113_115_Full_504.csv"
with open(output_path, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["# 國立臺中科技大學 國際貿易與經營系 (NUTC ITM) 113~115學年度四技甄選交叉查榜生源流向全量實證資料庫 (504筆)"])
    writer.writerow(["# 資料來源：大學/技專交叉查榜系統 (www.com.tw) 官方微觀實證數據 (涵蓋 113、114、115 三個學年度)"])
    writer.writerow(["序號", "學年度", "准考證號", "考生姓名", "來源錄取狀態", "最後分發學校", "最後分發系所", "去向分類", "最後分發狀態"])
    for idx, r in enumerate(itm, 1):
        yr_str = str(r.get("年度", "")) + "學年度"
        writer.writerow([
            idx,
            yr_str,
            r.get("准考證號", ""),
            r.get("姓名", ""),
            r.get("頁面狀態", ""),
            r.get("最後分發學校", "") if r.get("最後分發學校") else "—",
            r.get("最後分發系所", "") if r.get("最後分發系所") else "—",
            r.get("去向分類", ""),
            r.get("最後分發狀態", "")
        ])

print(f"Direct local CSV exported: {output_path} ({len(itm)} rows)")
