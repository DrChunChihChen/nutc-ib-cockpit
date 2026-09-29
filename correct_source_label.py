# -*- coding: utf-8 -*-
import re

# 1. Update README_DATA_CATALOG.md
readme_path = "/Users/chenchunchih/Downloads/校務資料/raw_data/README_DATA_CATALOG.md"
with open(readme_path, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    '中科大校務系統內部統計 (IR)',
    '教育部大專校院校務資訊公開平台 (MOE UDB) 系所報表'
)
with open(readme_path, 'w', encoding='utf-8') as f:
    f.write(text)

# Also copy to dist/raw_data
with open("/Users/chenchunchih/Downloads/校務資料/dist/raw_data/README_DATA_CATALOG.md", 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Update interactive_dashboard.html, index.html, dist/index.html
for path in [
    "/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html",
    "/Users/chenchunchih/Downloads/校務資料/index.html",
    "/Users/chenchunchih/Downloads/校務資料/dist/index.html"
]:
    with open(path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    c = c.replace(
        '<span class="text-stone-700 font-medium">國立臺中科技大學 校務系統 IR 實證統計</span>',
        '<a href="https://udb.moe.edu.tw/udata/DetailReportList/18/1/Statue" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">教育部大專資訊公開平臺 (MOE UDB 學1-1/學12-1/學13-1/學14-1) <i data-lucide="external-link" class="w-3 h-3"></i></a>'
    )
    c = c.replace(
        '國立臺中科技大學 校務系統 IR 實證統計',
        '教育部大專資訊公開平臺 (MOE UDB 學12-1/學14-1/學1-1)'
    )
    c = c.replace(
        '國立臺中科技大學 校務系統內部實證數據 (IR)',
        '教育部大專資訊公開平臺 (MOE UDB 官方系所報表)'
    )
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)

print("Successfully updated source labels to MOE UDB across all files!")
