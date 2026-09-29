import csv, json

# 1. Read the 504 rows from ntcust_flow_all_113_115.csv
with open("/Users/chenchunchih/Downloads/ntcust_flow_all_113_115.csv", "r", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

itm = [r for r in rows if r.get("來源系所代碼") == "113001"]

compact_504 = []
for idx, r in enumerate(itm, 1):
    sch = r.get("最後分發學校", "").strip()
    dept = r.get("最後分發系所", "").strip()
    compact_504.append([
        idx,
        r.get("年度", "").strip(),
        r.get("准考證號", "").strip(),
        r.get("姓名", "").strip(),
        r.get("頁面狀態", "").strip(),
        sch if sch else "—",
        dept if dept else "—",
        r.get("去向分類", "").strip(),
        r.get("最後分發狀態", "").strip()
    ])

json_504_str = json.dumps(compact_504, ensure_ascii=False)

# 2. Read interactive_dashboard.html
with open("interactive_dashboard.html", "r", encoding="utf-8") as f:
    html = f.read()

# Fix top button in banner:
html = html.replace(
    'onclick="exportCrossAdmissionCSV()" class="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-500 text-slate-900 text-xs font-bold flex items-center gap-2 shadow-lg shadow-purple-600/30 transition"',
    'onclick="exportCrossAdmissionCSV()" class="px-4 py-2 rounded-xl bg-purple-600 hover:bg-purple-700 text-white text-xs font-bold flex items-center gap-2 shadow-sm transition"'
)

# Fix second button in micro-table header:
html = html.replace(
    '<button onclick="exportModule6CSV()" class="text-xs px-3 py-1.5 rounded-lg bg-white border border-slate-300 hover:bg-slate-50 text-slate-800 font-medium transition flex items-center gap-1.5 shadow-sm">',
    '<button onclick="exportCrossAdmissionCSV()" class="text-xs px-3 py-1.5 rounded-lg bg-white border border-slate-300 hover:bg-slate-50 text-slate-800 font-medium transition flex items-center gap-1.5 shadow-sm">'
)

# 3. Build the full export logic
new_export_logic = f'''
        // =========================================================================
        // 模組 6：四技甄選交叉查榜全量 504 筆實證母體資料庫 (113~115 學年度)
        // =========================================================================
        const MODULE6_CANDIDATES_504 = {json_504_str};

        function exportCrossAdmissionCSV() {{
            const header = [
                ['# 國立臺中科技大學 國際貿易與經營系 (NUTC ITM) 113~115學年度四技甄選交叉查榜生源流向全量實證資料庫 (504筆)'],
                ['# 資料來源：大學/技專交叉查榜系統 (www.com.tw) 官方微觀實證數據 (涵蓋 113、114、115 三個學年度)'],
                ['序號', '學年度', '准考證號', '考生姓名', '來源錄取狀態', '最後分發學校', '最後分發系所', '去向分類', '最後分發狀態']
            ];

            const bodyRows = MODULE6_CANDIDATES_504.map(row => [
                row[0],
                `${{row[1]}}學年度`,
                row[2],
                `"${{row[3]}}"`,
                `"${{row[4]}}"`,
                `"${{row[5]}}"`,
                `"${{row[6]}}"`,
                `"${{row[7]}}"`,
                `"${{row[8]}}"`
            ]);

            const allRows = [...header, ...bodyRows];
            const csvContent = "\\uFEFF" + allRows.map(r => r.join(",")).join("\\n");
            
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", "NUTC_ITM_Cross_Admission_Poaching_113_115_Full_504.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }}

        // 同步相容函式
        function exportModule6CSV() {{
            exportCrossAdmissionCSV();
        }}
'''

import re
old_func_pattern = r'// Module 6 甄選流向全量 504 筆 CSV 匯出功能\s+function exportModule6CSV\(\)[\s\S]*?document\.body\.removeChild\(link\);\s+\}'
if re.search(old_func_pattern, html):
    html = re.sub(old_func_pattern, lambda m: new_export_logic, html)
else:
    html = html.replace('function exportAllCSV() {', new_export_logic + '\n        function exportAllCSV() {')

with open("interactive_dashboard.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully injected full 504 rows JSON and exportCrossAdmissionCSV() function!")
