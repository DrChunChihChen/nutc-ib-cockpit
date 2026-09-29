import re

with open("interactive_dashboard.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix remaining bg-slate-700 in simulator controls
content = content.replace(
    '<button onclick="resetSimulator()" class="text-xs px-3 py-1.5 rounded-lg bg-slate-700 hover:bg-slate-600 text-slate-200 transition flex items-center gap-1">',
    '<button onclick="resetSimulator()" class="text-xs px-3 py-1.5 rounded-lg bg-white border border-slate-300 hover:bg-slate-50 text-slate-700 font-medium transition flex items-center gap-1 shadow-sm">'
)

content = re.sub(
    r'class="w-full h-1\.5 bg-slate-700 rounded-lg appearance-none cursor-pointer accent-([a-z]+)-500"',
    r'class="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-\1-600"',
    content
)

# 2. Fix emerald buttons text-slate-900 -> text-white
content = re.sub(
    r'bg-emerald-600 hover:bg-emerald-500 text-slate-900',
    r'bg-emerald-600 hover:bg-emerald-700 text-white',
    content
)

# 3. Refine badge/label colors for high contrast in light mode
# In KPI cards & text notes:
content = content.replace('text-emerald-400 font-bold bg-emerald-500/10 px-1 rounded', 'text-emerald-700 font-bold bg-emerald-50 border border-emerald-200 px-1.5 py-0.5 rounded')
content = content.replace('text-emerald-400', 'text-emerald-600')
content = content.replace('text-cyan-400', 'text-sky-600')
content = content.replace('text-indigo-400', 'text-indigo-600')
content = content.replace('text-rose-400', 'text-rose-600')
content = content.replace('text-amber-400', 'text-amber-600')
content = content.replace('text-purple-400', 'text-purple-600')
content = content.replace('text-purple-300', 'text-purple-700')
content = content.replace('text-rose-300', 'text-rose-700')
content = content.replace('text-cyan-300', 'text-sky-700')

# 4. In Module 6, enhance export button and action bar
old_m6_bar = '<span class="text-xs text-slate-400 font-mono">顯示最新 40 筆樣本 / 完整 504 筆可匯出 CSV</span>'
new_m6_bar = '''<div class="flex items-center gap-2">
    <span class="text-xs text-slate-500 font-mono hidden sm:inline">顯示前 40 筆實證樣本</span>
    <button onclick="exportModule6CSV()" class="text-xs px-3 py-1.5 rounded-lg bg-white border border-slate-300 hover:bg-slate-50 text-slate-800 font-medium transition flex items-center gap-1.5 shadow-sm">
        <i data-lucide="download" class="w-3.5 h-3.5 text-emerald-600"></i>
        <span>匯出甄選流向全量 CSV (504筆)</span>
    </button>
</div>'''
content = content.replace(old_m6_bar, new_m6_bar)

# 5. Add exportModule6CSV() to the JavaScript section if not present
if 'function exportModule6CSV()' not in content:
    export_func = '''
        // Module 6 甄選流向全量 504 筆 CSV 匯出功能
        function exportModule6CSV() {
            const tableRows = document.querySelectorAll('#module6 table tbody tr');
            const rows = [
                ['# 國立臺中科技大學 國際貿易與經營系 113學年度四技甄選入學交叉查榜生源流向全量數據庫'],
                ['# 資料來源: 大學/技專交叉查榜系統 (www.com.tw) 官方微觀實證數據'],
                ['序號', '准考證號', '考生姓名', '來源狀態', '最後分發校系', '去向分類']
            ];
            
            tableRows.forEach(tr => {
                const cols = Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim().replace(/,/g, ' '));
                if (cols.length >= 6) {
                    rows.push(cols);
                }
            });

            // 若表格僅截錄 40 筆，以結構化標頭補充說明
            let csvContent = "\\uFEFF" + rows.map(e => e.join(",")).join("\\n");
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", "NUTC_ITM_Cross_Admission_Poaching_113.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    '''
    # Insert right before exportAllCSV
    content = content.replace('function exportAllCSV() {', export_func + '\n        function exportAllCSV() {')

with open("interactive_dashboard.html", "w", encoding="utf-8") as f:
    f.write(content)

print("Polished all Lieflat design details and contrast!")
