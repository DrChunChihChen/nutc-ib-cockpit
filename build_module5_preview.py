# -*- coding: utf-8 -*-
"""
Build standalone local preview HTML for Module 5:
四技甄選各校互打與雙向重疊錄取趨勢 (113-115)
純地端預覽，不執行任何外部部署。
"""

import os
import json
import pandas as pd

# 讀取剛剛產出的資料庫
df_new = pd.read_csv("/Users/chenchunchih/Downloads/校務資料/高科大_北商_113_115四技二專交叉查榜資料庫.csv")
df_nutc = pd.read_csv("/Users/chenchunchih/Downloads/ntcust_flow_all_113_115.csv")
itm = df_nutc[df_nutc["來源系所代碼"] == 113001]

# 整合可供微觀檢索的候選人生源名冊 (前 150 筆最具代表性的跨校對決樣本)
sample_rows = []
# 1. 北商 -> 中科 / 高科
for idx, r in df_new[df_new["系所名稱"].str.contains("臺北商業")].iterrows():
    sample_rows.append({
        "year": int(r["學年度"]),
        "origin_dept": "北商大 國際商務系",
        "exam_no": str(r["准考證號"]),
        "name": str(r["考生姓名"]),
        "status": str(r["本系錄取狀態"]),
        "dest_school": str(r["最終分發學校"]),
        "dest_dept": str(r["最終分發系所"]),
        "category": str(r["去向分類"])
    })

# 2. 高科 -> 中科 / 北商
for idx, r in df_new[df_new["系所名稱"].str.contains("高雄科技")].iterrows():
    dest = str(r["最終分發學校"])
    if "臺中科技" in dest or "臺北商業" in dest or "高雄科技" in dest:
        dept_tag = "高科大 航運管理系" if "航運" in str(r["系所名稱"]) else "高科大 國際企業系"
        sample_rows.append({
            "year": int(r["學年度"]),
            "origin_dept": dept_tag,
            "exam_no": str(r["准考證號"]),
            "name": str(r["考生姓名"]),
            "status": str(r["本系錄取狀態"]),
            "dest_school": dest,
            "dest_dept": str(r["最終分發系所"]),
            "category": str(r["去向分類"])
        })

# 3. 中科 -> 北商 / 高科
for idx, r in itm.iterrows():
    dest_sch = str(r.get("最後分發學校", ""))
    if "高雄科技" in dest_sch or "臺北商業" in dest_sch or "臺中科技" in dest_sch:
        sample_rows.append({
            "year": int(r["年度"]),
            "origin_dept": "中科大 國際貿易與經營系",
            "exam_no": str(r.get("准考證號", "—")),
            "name": str(r.get("姓名", "—")),
            "status": str(r.get("頁面狀態", "正取")),
            "dest_school": dest_sch,
            "dest_dept": str(r.get("最後分發系所", "—")),
            "category": str(r.get("去向分類", "—"))
        })

print(f"篩選出精華跨校對決檢索樣本: {len(sample_rows)} 筆")
sample_json = json.dumps(sample_rows, ensure_ascii=False)

html_content = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>【地端預覽】模組 5：四技甄選各校互打與雙向重疊錄取趨勢 (113-115) · Lieflat Editorial</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Lucide Icons -->
    <script src="https://cdn.jsdelivr.net/npm/lucide@latest/dist/umd/lucide.min.js"></script>
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Serif+TC:wght@500;700;900&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, sans-serif;
            background-color: #fafaf7;
            color: #1c1917;
        }}
        .font-serif-tc {{
            font-family: 'Noto Serif TC', Georgia, serif;
        }}
        .font-mono-num {{
            font-family: 'Space Grotesk', 'JetBrains Mono', monospace;
        }}
        .double-border-b {{
            border-bottom: 4px double #d6d3d1;
        }}
        .double-border-t {{
            border-top: 4px double #d6d3d1;
        }}
        .badge-positive {{
            background-color: #ecfdf5;
            color: #047857;
            border: 1px solid #a7f3d0;
        }}
        .badge-negative {{
            background-color: #fff1f2;
            color: #be123c;
            border: 1px solid #fecdd3;
        }}
    </style>
</head>
<body class="min-h-screen pb-16">

    <!-- 頂部地端提示 Bar -->
    <div class="bg-stone-900 text-stone-200 text-xs px-4 py-2 flex flex-wrap items-center justify-between border-b border-stone-800">
        <div class="flex items-center gap-2">
            <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
            <span class="font-bold text-amber-300 font-mono tracking-wide">[LOCAL ONLY] 純地端沙盒預覽 · 未執行任何外部部署</span>
            <span class="text-stone-400">｜</span>
            <span>四技商管三大校系：中科國貿 × 北商國商 × 高科國企/航管</span>
        </div>
        <div class="text-stone-400 font-mono text-[11px]">
            校務研究資料庫版本：113~115 全量 1,673 筆實證母體 (Apple Vision OCR 校驗)
        </div>
    </div>

    <!-- 主體內容容器 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-6 space-y-8">

        <!-- 模組標題橫幅 -->
        <header class="bg-white border-l-4 border-l-[#f05138] border border-stone-200 rounded-sm p-6 shadow-sm">
            <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <div class="flex flex-wrap items-center gap-2 mb-2">
                        <span class="px-2 py-0.5 rounded-sm text-[11px] font-mono font-bold bg-stone-100 text-stone-800 border border-stone-300">模組 5 升級版</span>
                        <span class="px-2 py-0.5 rounded-sm text-[11px] font-bold bg-rose-50 text-rose-700 border border-rose-200">全台首創 · 雙向跨校互打模型</span>
                        <span class="text-xs text-stone-500 font-medium">113~115 三學年度全量交叉查榜母體</span>
                    </div>
                    <h1 class="text-2xl sm:text-3xl font-black text-stone-900 tracking-tight font-serif-tc">
                        四技甄選各校互打與雙向重疊錄取趨勢分析
                    </h1>
                    <p class="text-xs sm:text-sm text-stone-700 mt-2 max-w-4xl leading-relaxed">
                        突破過去僅由單一學校單向觀察外流之侷限，完整匯流 <strong>中科國貿（113001）</strong>、<strong>北商國商（114004/5）</strong>、<strong>高科國企（105044/5/6）</strong> 與 <strong>高科航管（105075/6）</strong> 四大系所共 21 個官方榜單頁面。精確解構 113~114 年間各校「奪生 vs 失生」的淨勝態勢，並追蹤考生在雙榜錄取時的跨區流向抉擇。
                    </p>
                </div>
                <div class="flex flex-col items-end gap-2 flex-shrink-0">
                    <div class="flex items-center gap-2">
                        <span class="text-xs text-stone-500 font-mono">母體樣本數</span>
                        <span class="text-2xl font-black text-stone-900 font-mono-num">1,673 <span class="text-xs font-normal text-stone-500">人次</span></span>
                    </div>
                    <div class="text-[11px] text-emerald-700 font-semibold bg-emerald-50 px-2.5 py-1 rounded border border-emerald-200">
                        <i data-lucide="shield-check" class="w-3.5 h-3.5 inline mr-1"></i>Apple Vision OCR 完整還原
                    </div>
                </div>
            </div>
        </header>

        <!-- 4 大互打對決戰情報告卡 (Duel Cards) -->
        <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            
            <!-- 對決 1: 中科 vs 北商 -->
            <div class="bg-white border border-stone-200 rounded-sm p-4 shadow-sm hover:shadow-md transition">
                <div class="flex items-center justify-between border-b border-stone-100 pb-2.5 mb-3">
                    <div>
                        <span class="text-[11px] font-mono text-stone-500 font-bold uppercase">Duel 01</span>
                        <h3 class="text-base font-bold text-stone-900 font-serif-tc">中科國貿 vs 北商國商</h3>
                    </div>
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold font-mono badge-positive">中科 3.2x 勝出</span>
                </div>
                <div class="space-y-2">
                    <div class="flex justify-between items-baseline">
                        <span class="text-xs text-stone-600">中科奪取北商生源</span>
                        <span class="text-lg font-black text-emerald-700 font-mono-num">45 <span class="text-[11px] font-normal text-stone-500">人</span></span>
                    </div>
                    <div class="flex justify-between items-baseline">
                        <span class="text-xs text-stone-600">北商奪取中科生源</span>
                        <span class="text-sm font-bold text-stone-500 font-mono-num">14 <span class="text-[11px] font-normal text-stone-400">人</span></span>
                    </div>
                    <div class="pt-2 border-t border-stone-100 flex justify-between items-center text-xs">
                        <span class="font-semibold text-stone-700">3年累計淨勝差額</span>
                        <span class="font-black text-[#f05138] font-mono-num text-base">+31 人</span>
                    </div>
                    <div class="text-[11px] text-stone-500 leading-snug bg-stone-50 p-2 rounded border border-stone-200/60 mt-1">
                        <strong>關鍵轉折：</strong> 114 學年北商國商報到率自 35.5% 崩跌至 8.5%，單年被中科狂奪 21 人。
                    </div>
                </div>
            </div>

            <!-- 對決 2: 中科 vs 高科航管 -->
            <div class="bg-white border border-stone-200 rounded-sm p-4 shadow-sm hover:shadow-md transition">
                <div class="flex items-center justify-between border-b border-stone-100 pb-2.5 mb-3">
                    <div>
                        <span class="text-[11px] font-mono text-stone-500 font-bold uppercase">Duel 02</span>
                        <h3 class="text-base font-bold text-stone-900 font-serif-tc">中科國貿 vs 高科航管</h3>
                    </div>
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold font-mono badge-positive">中科 2.6x 勝出</span>
                </div>
                <div class="space-y-2">
                    <div class="flex justify-between items-baseline">
                        <span class="text-xs text-stone-600">中科奪取高科航管</span>
                        <span class="text-lg font-black text-emerald-700 font-mono-num">97 <span class="text-[11px] font-normal text-stone-500">人</span></span>
                    </div>
                    <div class="flex justify-between items-baseline">
                        <span class="text-xs text-stone-600">高科航管奪取中科</span>
                        <span class="text-sm font-bold text-stone-500 font-mono-num">37 <span class="text-[11px] font-normal text-stone-400">人</span></span>
                    </div>
                    <div class="pt-2 border-t border-stone-100 flex justify-between items-center text-xs">
                        <span class="font-semibold text-stone-700">3年累計淨勝差額</span>
                        <span class="font-black text-[#f05138] font-mono-num text-base">+60 人</span>
                    </div>
                    <div class="text-[11px] text-stone-500 leading-snug bg-stone-50 p-2 rounded border border-stone-200/60 mt-1">
                        <strong>吸磁暴增：</strong> 高科航管為全台最大重疊生源庫，中科奪生數自 113年16人飆升至 115年42人。
                    </div>
                </div>
            </div>

            <!-- 對決 3: 中科 vs 高科國企 -->
            <div class="bg-white border border-stone-200 rounded-sm p-4 shadow-sm hover:shadow-md transition">
                <div class="flex items-center justify-between border-b border-stone-100 pb-2.5 mb-3">
                    <div>
                        <span class="text-[11px] font-mono text-stone-500 font-bold uppercase">Duel 03</span>
                        <h3 class="text-base font-bold text-stone-900 font-serif-tc">中科國貿 vs 高科國企</h3>
                    </div>
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold font-mono badge-positive">中科 2.2x 勝出</span>
                </div>
                <div class="space-y-2">
                    <div class="flex justify-between items-baseline">
                        <span class="text-xs text-stone-600">中科奪取高科國企</span>
                        <span class="text-lg font-black text-emerald-700 font-mono-num">67 <span class="text-[11px] font-normal text-stone-500">人</span></span>
                    </div>
                    <div class="flex justify-between items-baseline">
                        <span class="text-xs text-stone-600">高科國企奪取中科</span>
                        <span class="text-sm font-bold text-stone-500 font-mono-num">30 <span class="text-[11px] font-normal text-stone-400">人</span></span>
                    </div>
                    <div class="pt-2 border-t border-stone-100 flex justify-between items-center text-xs">
                        <span class="font-semibold text-stone-700">3年累計淨勝差額</span>
                        <span class="font-black text-[#f05138] font-mono-num text-base">+37 人</span>
                    </div>
                    <div class="text-[11px] text-stone-500 leading-snug bg-stone-50 p-2 rounded border border-stone-200/60 mt-1">
                        <strong>正統爭鋒：</strong> 國貿 vs 國企在商管群正面對決，中科在 113(+15)、114(+4)、115(+18) 連三屆全面勝出。
                    </div>
                </div>
            </div>

            <!-- 對決 4: 北商 vs 高科 -->
            <div class="bg-white border border-stone-200 rounded-sm p-4 shadow-sm hover:shadow-md transition">
                <div class="flex items-center justify-between border-b border-stone-100 pb-2.5 mb-3">
                    <div>
                        <span class="text-[11px] font-mono text-stone-500 font-bold uppercase">Duel 04</span>
                        <h3 class="text-base font-bold text-stone-900 font-serif-tc">北商國商 vs 高科國企/航管</h3>
                    </div>
                    <span class="px-2 py-0.5 rounded text-[11px] font-bold font-mono badge-positive">北商 +6 些微領先</span>
                </div>
                <div class="space-y-2">
                    <div class="flex justify-between items-baseline">
                        <span class="text-xs text-stone-600">北商奪取高科生源</span>
                        <span class="text-lg font-black text-indigo-700 font-mono-num">27 <span class="text-[11px] font-normal text-stone-500">人</span></span>
                    </div>
                    <div class="flex justify-between items-baseline">
                        <span class="text-xs text-stone-600">高科奪取北商生源</span>
                        <span class="text-sm font-bold text-stone-500 font-mono-num">21 <span class="text-[11px] font-normal text-stone-400">人</span></span>
                    </div>
                    <div class="pt-2 border-t border-stone-100 flex justify-between items-center text-xs">
                        <span class="font-semibold text-stone-700">3年累計淨勝差額</span>
                        <span class="font-black text-indigo-600 font-mono-num text-base">+6 人</span>
                    </div>
                    <div class="text-[11px] text-stone-500 leading-snug bg-stone-50 p-2 rounded border border-stone-200/60 mt-1">
                        <strong>南北拉鋸：</strong> 114 年高科反超北商 3 人（南向回流），115 年北商國商回穩搶下 12 人。
                    </div>
                </div>
            </div>

        </section>

        <!-- 圖表區：113~115 互打消長趨勢圖 (動態交互切換) -->
        <section class="bg-white border border-stone-200 rounded-sm p-6 shadow-sm">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 border-b border-stone-100 pb-4">
                <div>
                    <h3 class="text-lg font-bold text-stone-900 font-serif-tc flex items-center gap-2">
                        <span class="w-2.5 h-2.5 rounded-full bg-[#f05138]"></span>
                        113 ~ 115 學年度 各校雙向互打奪生／失生消長趨勢 (Head-to-Head Multi-Year Trend)
                    </h3>
                    <p class="text-xs text-stone-500 mt-1">點擊右側按鈕切換檢視維度：觀察三大名校在 113 至 115 年間的爭奪攻防消長</p>
                </div>
                <div class="inline-flex rounded-md shadow-sm bg-stone-100 p-1 border border-stone-200">
                    <button id="btn-trend-net" onclick="switchTrendView('net')" class="px-3 py-1.5 rounded text-xs font-bold transition bg-white text-stone-900 shadow-sm">淨勝差額趨勢</button>
                    <button id="btn-trend-flow" onclick="switchTrendView('flow')" class="px-3 py-1.5 rounded text-xs font-medium text-stone-600 hover:text-stone-900 transition">雙向攻防量體</button>
                    <button id="btn-trend-retention" onclick="switchTrendView('retention')" class="px-3 py-1.5 rounded text-xs font-medium text-stone-600 hover:text-stone-900 transition">各系報到率震盪</button>
                </div>
            </div>

            <div class="h-80 sm:h-96 relative w-full">
                <canvas id="chart-duel-trend"></canvas>
            </div>
            
            <div class="mt-4 pt-3 border-t border-stone-100 flex flex-wrap items-center justify-between text-xs text-stone-500">
                <div class="flex items-center gap-4">
                    <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-emerald-600 inline-block"></span> 中科 vs 北商 淨勝</span>
                    <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-sky-600 inline-block"></span> 中科 vs 高科航管 淨勝</span>
                    <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-sm bg-amber-600 inline-block"></span> 中科 vs 高科國企 淨勝</span>
                </div>
                <div class="font-mono text-[11px]">
                    * 淨勝人數 = 中科自該校系搶下之人數 - 該校系自中科搶下之人數
                </div>
            </div>
        </section>

        <!-- 雙向互打詳細數據矩陣表 (Yearly Breakdown) -->
        <section class="bg-white border border-stone-200 rounded-sm p-6 shadow-sm space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-stone-100 pb-3">
                <div>
                    <h3 class="text-base font-bold text-stone-900 font-serif-tc flex items-center gap-2">
                        <i data-lucide="crosshair" class="w-4 h-4 text-[#f05138]"></i>
                        四技商管三大校系 113~115 逐年攻防矩陣實證清冊
                    </h3>
                    <p class="text-xs text-stone-500 mt-0.5">跨校雙向交叉比對，精確還原歷年正備取生之實質流向消長</p>
                </div>
                <span class="text-xs bg-stone-100 text-stone-700 px-2.5 py-1 rounded font-mono font-medium">數據單位：人次</span>
            </div>

            <div class="overflow-x-auto border border-stone-200 rounded">
                <table class="w-full text-left text-xs border-collapse">
                    <thead class="bg-stone-100 text-stone-800 font-bold border-b border-stone-200">
                        <tr>
                            <th class="p-3">對決組合</th>
                            <th class="p-3 text-center">學年度</th>
                            <th class="p-3 text-right">中科奪生 (Inflow)</th>
                            <th class="p-3 text-right">中科失生 (Outflow)</th>
                            <th class="p-3 text-right">中科淨勝額</th>
                            <th class="p-3 text-center">勝率指標</th>
                            <th class="p-3">年度戰情核心解讀</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-stone-200/70 text-stone-700">
                        <!-- 中科 vs 北商 -->
                        <tr class="hover:bg-stone-50">
                            <td class="p-3 font-bold text-stone-900" rowspan="3">中科國貿 vs 北商國商</td>
                            <td class="p-3 text-center font-mono font-bold">113 年</td>
                            <td class="p-3 text-right font-mono text-emerald-700 font-bold">12</td>
                            <td class="p-3 text-right font-mono text-rose-600">6</td>
                            <td class="p-3 text-right font-mono font-black text-emerald-700">+6</td>
                            <td class="p-3 text-center font-mono font-bold badge-positive">66.7%</td>
                            <td class="p-3 text-stone-600">中科展現強勁吸磁，從北商國商搶下 12 位正備取生，北商僅逆向拉走 6 人。</td>
                        </tr>
                        <tr class="hover:bg-stone-50 bg-rose-50/20">
                            <td class="p-3 text-center font-mono font-bold text-[#f05138]">114 年</td>
                            <td class="p-3 text-right font-mono text-emerald-700 font-bold">21</td>
                            <td class="p-3 text-right font-mono text-rose-600">5</td>
                            <td class="p-3 text-right font-mono font-black text-[#f05138] text-sm">+16</td>
                            <td class="p-3 text-center font-mono font-bold badge-positive">80.8%</td>
                            <td class="p-3 text-[#f05138] font-medium"><strong>大突破！</strong> 北商國商 114 年報到率受重創，中科搶下高達 21 人，創歷史淨勝峰值。</td>
                        </tr>
                        <tr class="hover:bg-stone-50">
                            <td class="p-3 text-center font-mono font-bold">115 年</td>
                            <td class="p-3 text-right font-mono text-emerald-700 font-bold">12</td>
                            <td class="p-3 text-right font-mono text-rose-600">3</td>
                            <td class="p-3 text-right font-mono font-black text-emerald-700">+9</td>
                            <td class="p-3 text-center font-mono font-bold badge-positive">80.0%</td>
                            <td class="p-3 text-stone-600">北商回升報到率，但中科仍維持 4:1 壓倒性勝率，穩居中北對決優勢方。</td>
                        </tr>

                        <!-- 中科 vs 高科航管 -->
                        <tr class="hover:bg-stone-50 border-t-2 border-stone-200">
                            <td class="p-3 font-bold text-stone-900" rowspan="3">中科國貿 vs 高科航管</td>
                            <td class="p-3 text-center font-mono font-bold">113 年</td>
                            <td class="p-3 text-right font-mono text-emerald-700 font-bold">16</td>
                            <td class="p-3 text-right font-mono text-rose-600">11</td>
                            <td class="p-3 text-right font-mono font-black text-emerald-700">+5</td>
                            <td class="p-3 text-center font-mono font-bold badge-positive">59.3%</td>
                            <td class="p-3 text-stone-600">海陸經貿旗艦對決，雙方攻防緊密，中科淨勝 5 人。</td>
                        </tr>
                        <tr class="hover:bg-stone-50 bg-rose-50/20">
                            <td class="p-3 text-center font-mono font-bold text-[#f05138]">114 年</td>
                            <td class="p-3 text-right font-mono text-emerald-700 font-bold">39</td>
                            <td class="p-3 text-right font-mono text-rose-600">15</td>
                            <td class="p-3 text-right font-mono font-black text-[#f05138] text-sm">+24</td>
                            <td class="p-3 text-center font-mono font-bold badge-positive">72.2%</td>
                            <td class="p-3 text-[#f05138] font-medium">中科吸納量暴增，自高科航管搶下 39 人，中科地理與商務優勢完全壓制。</td>
                        </tr>
                        <tr class="hover:bg-stone-50">
                            <td class="p-3 text-center font-mono font-bold">115 年</td>
                            <td class="p-3 text-right font-mono text-emerald-700 font-bold">42</td>
                            <td class="p-3 text-right font-mono text-rose-600">11</td>
                            <td class="p-3 text-right font-mono font-black text-[#f05138] text-sm">+31</td>
                            <td class="p-3 text-center font-mono font-bold badge-positive">79.2%</td>
                            <td class="p-3 text-stone-600">高科航管規模擴增至 113 人，但被中科掠奪多達 42 人，中科成為該系第一首選對手。</td>
                        </tr>

                        <!-- 中科 vs 高科國企 -->
                        <tr class="hover:bg-stone-50 border-t-2 border-stone-200">
                            <td class="p-3 font-bold text-stone-900" rowspan="3">中科國貿 vs 高科國企</td>
                            <td class="p-3 text-center font-mono font-bold">113 年</td>
                            <td class="p-3 text-right font-mono text-emerald-700 font-bold">26</td>
                            <td class="p-3 text-right font-mono text-rose-600">11</td>
                            <td class="p-3 text-right font-mono font-black text-emerald-700">+15</td>
                            <td class="p-3 text-center font-mono font-bold badge-positive">70.3%</td>
                            <td class="p-3 text-stone-600">中南國貿國企正統爭鋒，中科憑藉台中都會區位，首年即取得 15 人淨勝。</td>
                        </tr>
                        <tr class="hover:bg-stone-50">
                            <td class="p-3 text-center font-mono font-bold">114 年</td>
                            <td class="p-3 text-right font-mono text-emerald-700 font-bold">14</td>
                            <td class="p-3 text-right font-mono text-rose-600">10</td>
                            <td class="p-3 text-right font-mono font-black text-emerald-700">+4</td>
                            <td class="p-3 text-center font-mono font-bold badge-positive">58.3%</td>
                            <td class="p-3 text-stone-600">戰況膠著，雙方互有斬獲，中科仍保持淨勝 +4 人。</td>
                        </tr>
                        <tr class="hover:bg-stone-50">
                            <td class="p-3 text-center font-mono font-bold">115 年</td>
                            <td class="p-3 text-right font-mono text-emerald-700 font-bold">27</td>
                            <td class="p-3 text-right font-mono text-rose-600">9</td>
                            <td class="p-3 text-right font-mono font-black text-[#f05138] text-sm">+18</td>
                            <td class="p-3 text-center font-mono font-bold badge-positive">75.0%</td>
                            <td class="p-3 text-stone-600">中科優勢再度擴大，自高科國企三個組別搶下 27 人，達到 3:1 勝率。</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </section>

        <!-- 專業 IR 校務研究洞察評析手記 (Editorial Notes) -->
        <section class="bg-[#fefdfb] border-2 border-stone-800 rounded-sm p-6 shadow-md relative overflow-hidden">
            <div class="absolute -right-6 -bottom-6 w-32 h-32 bg-stone-100 rounded-full opacity-40 pointer-events-none"></div>
            <div class="flex items-center gap-2 mb-3">
                <i data-lucide="book-open" class="w-5 h-5 text-[#f05138]"></i>
                <h3 class="text-base font-bold text-stone-900 font-serif-tc tracking-wide">
                    校務決策智庫深度評析：113 至 114 年商管跨校互打之結構性劇變
                </h3>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-stone-700 leading-relaxed mt-4">
                <div class="border-t-2 border-stone-800 pt-3">
                    <span class="font-bold text-stone-900 text-sm block mb-1.5 font-serif-tc">01. 114 北商報到率大跳水謎團</span>
                    <p>
                        過去普遍認為北商大因位處台北首都圈享有絕對優勢，但 114 年數據證實其國際商務系留任率由 35.5% 暴跌至 <strong>8.5%</strong>。其中關鍵外流推手即為中科大（單年吸走 21 人），顯示雙榜同時錄取時，台中都會生活成本與中部進出口產業實習機會，對商管高分群考生已具備強烈誘因。
                    </p>
                </div>

                <div class="border-t-2 border-stone-800 pt-3">
                    <span class="font-bold text-stone-900 text-sm block mb-1.5 font-serif-tc">02. 高科航管的生源擴張與虹吸</span>
                    <p>
                        高科航管系在 115 年將榜單人數倍增至 113 人，試圖擴大規模防線，但交叉查榜數據顯示，其遭中科大掠奪的人數亦同步飆升至 <strong>42 人</strong>。這代表中科國貿與高科航管的考生重疊池極度深厚，中科大實質上扮演了中南部國貿海運商務的首選「虹吸核心」。
                    </p>
                </div>

                <div class="border-t-2 border-stone-800 pt-3">
                    <span class="font-bold text-stone-900 text-sm block mb-1.5 font-serif-tc">03. 少子化下的生源防禦戰略建議</span>
                    <p>
                        面臨 117 虎年少子化波谷，各校互打的慘烈度將進一步提升。建議中科國貿強化兩項戰略利刃：一是鞏固對北商大「台中優勢生活圈」的宣傳訴求；二是與台中港海運承攬、報關業深化產學實習，直接化解高科航管的專業特色威脅。
                    </p>
                </div>
            </div>
        </section>

        <!-- 微觀考生穿透檢索表 -->
        <section class="bg-white border border-stone-200 rounded-sm p-6 shadow-sm space-y-4">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-stone-100 pb-3">
                <div>
                    <h3 class="text-base font-bold text-stone-900 font-serif-tc flex items-center gap-2">
                        <i data-lucide="database" class="w-4 h-4 text-emerald-600"></i>
                        跨校對決考生微觀流向穿透檢索名冊 ({len(sample_rows)} 筆實證樣本)
                    </h3>
                    <p class="text-xs text-stone-500 mt-0.5">即時搜尋准考證、姓名、來源系所或最終分發學校</p>
                </div>
                <div class="flex items-center gap-2">
                    <input id="cand-search-input" onkeyup="filterCandTable()" type="text" placeholder="搜尋考生、學校或系所..." class="text-xs px-3 py-1.5 rounded border border-stone-300 focus:outline-none focus:border-stone-800 w-56 font-mono">
                    <select id="cand-year-select" onchange="filterCandTable()" class="text-xs px-2.5 py-1.5 rounded border border-stone-300 focus:outline-none focus:border-stone-800 bg-white font-mono font-bold">
                        <option value="ALL">全部學年</option>
                        <option value="113">113 學年度</option>
                        <option value="114">114 學年度</option>
                        <option value="115">115 學年度</option>
                    </select>
                </div>
            </div>

            <div class="overflow-x-auto border border-stone-200 rounded max-h-96 overflow-y-auto">
                <table id="cand-table" class="w-full text-left text-xs border-collapse">
                    <thead class="bg-stone-50 text-stone-700 font-semibold sticky top-0 border-b border-stone-200">
                        <tr>
                            <th class="p-2.5">學年</th>
                            <th class="p-2.5">來源錄取系所</th>
                            <th class="p-2.5">准考證號</th>
                            <th class="p-2.5">考生姓名</th>
                            <th class="p-2.5">本系錄取</th>
                            <th class="p-2.5">最終分發學校</th>
                            <th class="p-2.5">最終分發系所</th>
                            <th class="p-2.5">去向分類</th>
                        </tr>
                    </thead>
                    <tbody id="cand-tbody" class="divide-y divide-stone-100 text-stone-700">
                    </tbody>
                </table>
            </div>
            <div class="text-[11px] text-stone-400 font-mono text-right" id="cand-count-label">
                顯示共 {len(sample_rows)} 筆跨校對決記錄
            </div>
        </section>

    </main>

    <!-- JavaScript 動態圖表與過濾邏輯 -->
    <script>
        if (window.lucide && typeof lucide.createIcons === 'function') {{
            lucide.createIcons();
        }}

        // 嵌入跨校微觀候選人數據
        const RAW_CANDIDATES = {sample_json};

        // 1. 渲染微觀檢索表格
        function renderCandidates(cands) {{
            const tbody = document.getElementById('cand-tbody');
            tbody.innerHTML = '';
            cands.forEach(c => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-stone-50';
                
                let badgeClass = 'text-stone-600 bg-stone-100';
                if (c.dest_school.includes('臺中科技')) badgeClass = 'text-emerald-700 bg-emerald-50 border border-emerald-200 font-bold';
                else if (c.dest_school.includes('臺北商業')) badgeClass = 'text-indigo-700 bg-indigo-50 border border-indigo-200 font-bold';
                else if (c.dest_school.includes('高雄科技')) badgeClass = 'text-sky-700 bg-sky-50 border border-sky-200 font-bold';

                tr.innerHTML = `
                    <td class="p-2.5 font-mono font-bold">${{c.year}}</td>
                    <td class="p-2.5 font-medium text-stone-900">${{c.origin_dept}}</td>
                    <td class="p-2.5 font-mono text-stone-500">${{c.exam_no}}</td>
                    <td class="p-2.5 font-bold text-stone-800 font-mono">${{c.name}}</td>
                    <td class="p-2.5"><span class="px-1.5 py-0.5 rounded text-[10px] ${{c.status.includes('正取') ? 'bg-rose-100 text-rose-800' : 'bg-stone-100 text-stone-600'}}">${{c.status}}</span></td>
                    <td class="p-2.5 font-semibold"><span class="px-1.5 py-0.5 rounded text-[11px] ${{badgeClass}}">${{c.dest_school}}</span></td>
                    <td class="p-2.5 text-stone-600">${{c.dest_dept}}</td>
                    <td class="p-2.5 text-stone-500">${{c.category}}</td>
                `;
                tbody.appendChild(tr);
            }});
            document.getElementById('cand-count-label').innerText = `顯示共 ${{cands.length}} 筆跨校對決記錄`;
        }}

        function filterCandTable() {{
            const kw = document.getElementById('cand-search-input').value.toLowerCase().trim();
            const yr = document.getElementById('cand-year-select').value;
            const filtered = RAW_CANDIDATES.filter(c => {{
                const matchYr = (yr === 'ALL' || c.year.toString() === yr);
                const matchKw = !kw || (
                    c.name.toLowerCase().includes(kw) ||
                    c.exam_no.includes(kw) ||
                    c.origin_dept.toLowerCase().includes(kw) ||
                    c.dest_school.toLowerCase().includes(kw) ||
                    c.dest_dept.toLowerCase().includes(kw)
                );
                return matchYr && matchKw;
            }});
            renderCandidates(filtered);
        }}

        // 2. Chart.js 趨勢圖表動態切換
        let duelChart = null;

        const trendDatasets = {{
            net: {{
                labels: ['113 學年度', '114 學年度 (互打高峰)', '115 學年度'],
                datasets: [
                    {{
                        label: '中科 vs 北商 淨勝人數',
                        data: [6, 16, 9],
                        backgroundColor: '#059669',
                        borderColor: '#047857',
                        borderWidth: 1.5
                    }},
                    {{
                        label: '中科 vs 高科航管 淨勝人數',
                        data: [5, 24, 31],
                        backgroundColor: '#0284c7',
                        borderColor: '#0369a1',
                        borderWidth: 1.5
                    }},
                    {{
                        label: '中科 vs 高科國企 淨勝人數',
                        data: [15, 4, 18],
                        backgroundColor: '#d97706',
                        borderColor: '#b45309',
                        borderWidth: 1.5
                    }}
                ],
                title: '三大主要對決組合：中科國貿 113~115 歷年淨勝差額 (Net Gain / Loss)'
            }},
            flow: {{
                labels: ['113 學年', '114 學年', '115 學年'],
                datasets: [
                    {{
                        label: '北商流向中科 (中科奪生)',
                        data: [12, 21, 12],
                        backgroundColor: '#10b981',
                        stack: 'NUTC_NTUB'
                    }},
                    {{
                        label: '中科流向北商 (北商奪生)',
                        data: [-6, -5, -3],
                        backgroundColor: '#f43f5e',
                        stack: 'NUTC_NTUB'
                    }},
                    {{
                        label: '高科航管流向中科 (中科奪生)',
                        data: [16, 39, 42],
                        backgroundColor: '#38bdf8',
                        stack: 'NUTC_NKUST'
                    }},
                    {{
                        label: '中科流向高科航管 (高科奪生)',
                        data: [-11, -15, -11],
                        backgroundColor: '#fb7185',
                        stack: 'NUTC_NKUST'
                    }}
                ],
                title: '113~115 雙向攻防進出量體堆疊對比 (正值: 中科奪得 / 負值: 對手搶走)'
            }},
            retention: {{
                labels: ['113 學年度', '114 學年度', '115 學年度'],
                datasets: [
                    {{
                        type: 'line',
                        label: '中科國貿 留任報到率 (%)',
                        data: [33.7, 33.1, 33.1],
                        borderColor: '#059669',
                        backgroundColor: '#059669',
                        borderWidth: 3,
                        tension: 0.2
                    }},
                    {{
                        type: 'line',
                        label: '北商國商 留任報到率 (%)',
                        data: [35.5, 8.5, 33.3],
                        borderColor: '#f05138',
                        backgroundColor: '#f05138',
                        borderWidth: 3,
                        tension: 0.2
                    }},
                    {{
                        type: 'line',
                        label: '高科國企 留任報到率 (%)',
                        data: [18.9, 27.5, 16.7],
                        borderColor: '#f59e0b',
                        backgroundColor: '#f59e0b',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        tension: 0.2
                    }},
                    {{
                        type: 'line',
                        label: '高科航管 留任報到率 (%)',
                        data: [24.5, 15.8, 20.4],
                        borderColor: '#6366f1',
                        backgroundColor: '#6366f1',
                        borderWidth: 2,
                        borderDash: [5, 5],
                        tension: 0.2
                    }}
                ],
                title: '各名校系 113~115 官方留任報到率走勢對比 (可見北商 114 年劇烈震盪)'
            }}
        }};

        function initDuelChart(viewMode) {{
            const ctx = document.getElementById('chart-duel-trend').getContext('2d');
            const dataConfig = trendDatasets[viewMode];
            
            if (duelChart) {{
                duelChart.destroy();
            }}

            duelChart = new Chart(ctx, {{
                type: (viewMode === 'retention') ? 'line' : 'bar',
                data: {{
                    labels: dataConfig.labels,
                    datasets: dataConfig.datasets
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: {{
                        mode: 'index',
                        intersect: false
                    }},
                    plugins: {{
                        title: {{
                            display: true,
                            text: dataConfig.title,
                            font: {{
                                family: "'Noto Serif TC', serif",
                                size: 14,
                                weight: 'bold'
                            }},
                            color: '#1c1917',
                            padding: {{ bottom: 15 }}
                        }},
                        legend: {{
                            position: 'bottom',
                            labels: {{
                                font: {{ family: "'Noto Sans TC', sans-serif", size: 11 }},
                                boxWidth: 12,
                                padding: 12
                            }}
                        }}
                    }},
                    scales: {{
                        y: {{
                            grid: {{ color: '#f5f5f4' }},
                            ticks: {{
                                font: {{ family: "'Space Grotesk', monospace", size: 11 }},
                                callback: function(val) {{
                                    return (viewMode === 'retention') ? val + '%' : val + ' 人';
                                }}
                            }}
                        }},
                        x: {{
                            grid: {{ display: false }},
                            ticks: {{
                                font: {{ family: "'Space Grotesk', sans-serif", size: 11, weight: 'bold' }}
                            }}
                        }}
                    }}
                }}
            }});
        }}

        function switchTrendView(mode) {{
            // 更新按鈕樣式
            ['net', 'flow', 'retention'].forEach(m => {{
                const btn = document.getElementById(`btn-trend-${{m}}`);
                if (m === mode) {{
                    btn.className = 'px-3 py-1.5 rounded text-xs font-bold transition bg-white text-stone-900 shadow-sm';
                }} else {{
                    btn.className = 'px-3 py-1.5 rounded text-xs font-medium text-stone-600 hover:text-stone-900 transition';
                }}
            }});
            initDuelChart(mode);
        }}

        // 暴露至全域方便調用與測試
        window.RAW_CANDIDATES = RAW_CANDIDATES;
        window.renderCandidates = renderCandidates;
        window.filterCandTable = filterCandTable;
        window.switchTrendView = switchTrendView;
        window.initDuelChart = initDuelChart;

        // 頁面初始化
        function initPreview() {{
            renderCandidates(RAW_CANDIDATES);
            initDuelChart('net');
            if (window.lucide && typeof lucide.createIcons === 'function') {{
                lucide.createIcons();
            }}
        }}

        if (document.readyState === 'loading') {{
            window.addEventListener('DOMContentLoaded', initPreview);
        }} else {{
            initPreview();
        }}
    </script>
</body>
</html>
'''

preview_path = "/Users/chenchunchih/Downloads/校務資料/preview_module5_cross_duel.html"
with open(preview_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ 地端預覽檔案已成功建置: {preview_path} ({len(html_content)} bytes)")
