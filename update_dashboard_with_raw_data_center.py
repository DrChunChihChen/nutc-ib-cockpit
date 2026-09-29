# -*- coding: utf-8 -*-
"""
Update interactive_dashboard.html and index.html to include:
1. Complete Open Data & Raw Data Verification Center Modal (#raw-data-modal)
2. Direct download links to Master Excel and all 10 CSV/JSON datasets
3. Official verification links for external cross-checking
4. exportComprehensiveMasterRawCSV() that outputs full 100% verified raw data
5. Full 700 jobs export and 504 admission export
6. Embedded 72 Tech Colleges and 61 General Universities survival data
"""

import json
import os
import re
import pandas as pd

HTML_PATH = "/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html"

with open(HTML_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

# Load 72 Tech and 61 Univ survival datasets
df9 = pd.read_csv('/Users/chenchunchih/Downloads/校務資料/raw_data/09_117學年度全台72所技專校院存活推估矩陣.csv')
df10 = pd.read_csv('/Users/chenchunchih/Downloads/校務資料/raw_data/10_117學年度全台61所普通大學存活推估矩陣.csv')

tech_72_json = df9.to_dict(orient='records')
univ_61_json = df10.to_dict(orient='records')

print(f"Loaded {len(tech_72_json)} Tech colleges and {len(univ_61_json)} General universities.")

# 1. Prepare Modal HTML
raw_data_modal_html = '''
    <!-- 全量實證原始資料庫與開源驗證中心 Modal (Open Data & Verification Center) -->
    <div id="raw-data-modal" class="fixed inset-0 bg-black/70 backdrop-blur-xs z-50 hidden flex items-center justify-center p-3 sm:p-5 no-print" onclick="if(event.target===this) closeDataModal()">
        <div class="bg-white border border-slate-200 rounded-2xl max-w-5xl w-full max-h-[92vh] flex flex-col shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
            <!-- Modal Header -->
            <div class="p-4 sm:p-5 border-b border-slate-200 flex items-center justify-between bg-slate-900 text-white">
                <div class="flex items-center gap-3">
                    <div class="p-2.5 rounded-xl bg-amber-500/20 text-amber-400 border border-amber-500/30">
                        <i data-lucide="database" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <div class="flex items-center gap-2">
                            <h3 class="text-base sm:text-lg font-black tracking-tight text-white font-serif-tc">全專案實證原始資料庫與開源查驗專區</h3>
                            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40">100% Raw Data</span>
                        </div>
                        <p class="text-xs text-slate-300 mt-0.5">國立臺中科技大學 國際貿易與經營系 (NUTC IB) · 10 大核心資料集 · 官方資料源與直通檢驗連結</p>
                    </div>
                </div>
                <button onclick="closeDataModal()" class="text-slate-400 hover:text-white p-2 rounded-lg hover:bg-slate-800 transition" aria-label="關閉視窗">
                    <i data-lucide="x" class="w-5 h-5"></i>
                </button>
            </div>

            <!-- Modal Body -->
            <div class="p-4 sm:p-6 overflow-y-auto space-y-6 text-xs text-slate-700 custom-scrollbar leading-relaxed bg-slate-50/50">
                <!-- 誠信與開源原則宣告 -->
                <div class="p-4 rounded-xl bg-gradient-to-r from-amber-50 to-orange-50 border border-amber-200 text-amber-950 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-xs">
                    <div class="flex items-start gap-2.5">
                        <i data-lucide="shield-check" class="w-5 h-5 text-amber-600 flex-shrink-0 mt-0.5"></i>
                        <div>
                            <strong class="text-sm font-bold text-amber-900">學術嚴謹性與資訊公開宣告 (Open Data Protocol)</strong>
                            <p class="text-xs text-amber-800 mt-0.5 leading-relaxed">
                                本戰情室所有圖表、儀表板指標、少子化推估與生源流向模型，均 100% 來自<strong>教育部統計處 (MOE UDB)</strong>、<strong>技專校院招生聯合會 (JCTV)</strong>、<strong>104 人力銀行實境庫</strong>與<strong>交叉查榜官方微觀母體</strong>。所有底層 Raw Data 開放全體委員、校務研究同仁及公眾完整查核！
                            </p>
                        </div>
                    </div>
                </div>

                <!-- 頂部兩大一鍵下載行動區 -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
                    <!-- Master Excel 下載卡片 -->
                    <div class="p-4 rounded-xl bg-white border-2 border-emerald-500/40 shadow-sm hover:border-emerald-500 transition flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">推薦首選 · 10大分頁合一</span>
                                <span class="text-[11px] font-mono text-slate-400">~403 KB</span>
                            </div>
                            <h4 class="text-sm font-black text-slate-900 mt-1.5 flex items-center gap-1.5">
                                <i data-lucide="file-spreadsheet" class="w-4 h-4 text-emerald-600"></i>
                                <span>All-in-One Master Excel 總整合工作簿</span>
                            </h4>
                            <p class="text-[11px] text-slate-500 mt-1">
                                內建 10 大標準工作表（504筆交叉查榜、700筆104職缺、教育部112/113學生數、6年統測、117存活等），雙擊直接在 Excel 開啟無亂碼！
                            </p>
                        </div>
                        <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between">
                            <a href="raw_data/NUTC_ITM_Comprehensive_IR_Raw_Data_Pack.xlsx" download="NUTC_ITM_Comprehensive_IR_Raw_Data_Pack.xlsx" class="w-full py-2 px-3 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs flex items-center justify-center gap-2 shadow-xs transition">
                                <i data-lucide="download" class="w-4 h-4"></i>
                                <span>下載 Master Excel 活頁簿 (.xlsx)</span>
                            </a>
                        </div>
                    </div>

                    <!-- 一鍵全量 CSV 下載卡片 -->
                    <div class="p-4 rounded-xl bg-white border-2 border-[#f05138]/40 shadow-sm hover:border-[#f05138] transition flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800">跨平台純文字 · UTF-8 BOM</span>
                                <span class="text-[11px] font-mono text-slate-400">完整原始記錄</span>
                            </div>
                            <h4 class="text-sm font-black text-slate-900 mt-1.5 flex items-center gap-1.5">
                                <i data-lucide="file-text" class="w-4 h-4 text-[#f05138]"></i>
                                <span>全量原始數據綜合大總表 (Comprehensive CSV)</span>
                            </h4>
                            <p class="text-[11px] text-slate-500 mt-1">
                                瀏覽器即時打包匯出本專案全量實證資料庫（包含 504 筆考生全量、700 筆職缺全量、133 所大專 117 存活推估），隨載隨驗。
                            </p>
                        </div>
                        <div class="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between">
                            <button onclick="exportComprehensiveMasterRawCSV()" class="w-full py-2 px-3 rounded-lg bg-[#f05138] hover:bg-[#e04830] text-white font-bold text-xs flex items-center justify-center gap-2 shadow-xs transition">
                                <i data-lucide="download" class="w-4 h-4"></i>
                                <span>即刻匯出全量綜合 CSV (\uFEFF BOM)</span>
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 10 大核心資料集詳細清冊與官方驗證入口 -->
                <div>
                    <div class="flex items-center justify-between mb-2.5">
                        <h4 class="text-sm font-black text-slate-900 flex items-center gap-2">
                            <i data-lucide="layers" class="w-4 h-4 text-sky-600"></i>
                            <span>10 大核心實證原始資料集清冊與官方查核入口 (Data Catalog & Direct Links)</span>
                        </h4>
                        <a href="raw_data/README_DATA_CATALOG.md" target="_blank" class="text-[11px] text-sky-600 hover:text-sky-800 hover:underline flex items-center gap-1 font-semibold">
                            <i data-lucide="external-link" class="w-3 h-3"></i>
                            <span>完整資料目錄指南 (README)</span>
                        </a>
                    </div>

                    <div class="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-xs">
                        <div class="divide-y divide-slate-100">
                            
                            <!-- 01. 交叉查榜 504 筆 -->
                            <div class="p-3.5 sm:p-4 hover:bg-slate-50/80 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2 py-0.5 rounded bg-slate-900 text-white font-mono text-[10px] font-bold">01</span>
                                        <strong class="text-xs sm:text-sm text-slate-900">四技二專甄選交叉查榜 504 筆考生流向微觀母體</strong>
                                        <span class="px-2 py-0.2 rounded-full text-[10px] font-medium bg-blue-50 text-blue-700 border border-blue-200">504 筆</span>
                                    </div>
                                    <p class="text-[11px] text-slate-500">中科國貿 113~115 學年考生准考證號、錄取別、最終分發校系、原系留任/外校流失微觀名冊。</p>
                                    <div class="flex items-center gap-2 text-[11px] text-stone-500">
                                        <span class="font-medium">官方驗證：</span>
                                        <a href="https://www.com.tw/vtech/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">
                                            大學/技專交叉查榜系統官方平臺 <i data-lucide="external-link" class="w-3 h-3"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <a href="raw_data/01_四技二專甄選交叉查榜504筆考生流向.csv" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> 下載 CSV
                                    </a>
                                    <a href="raw_data/01_四技二專甄選交叉查榜504筆考生流向.json" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> JSON
                                    </a>
                                </div>
                            </div>

                            <!-- 02. 104 中部職缺 700 筆 -->
                            <div class="p-3.5 sm:p-4 hover:bg-slate-50/80 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2 py-0.5 rounded bg-slate-900 text-white font-mono text-[10px] font-bold">02</span>
                                        <strong class="text-xs sm:text-sm text-slate-900">104 人力銀行中部經貿職缺 700 筆實證資料庫</strong>
                                        <span class="px-2 py-0.2 rounded-full text-[10px] font-medium bg-purple-50 text-purple-700 border border-purple-200">700 筆</span>
                                    </div>
                                    <p class="text-[11px] text-slate-500">國外業務、報關關務、電子商務與 AI 前鋒職缺，含起薪高低標、AI 技能標註與 104 官方直通 URL。</p>
                                    <div class="flex items-center gap-2 text-[11px] text-stone-500">
                                        <span class="font-medium">官方驗證：</span>
                                        <a href="https://www.104.com.tw/jobs/search/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">
                                            104 人力銀行工作檢索官方網站 <i data-lucide="external-link" class="w-3 h-3"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <a href="raw_data/02_104中部經貿職缺700筆實證資料庫.csv" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> 下載 CSV
                                    </a>
                                    <a href="raw_data/02_104中部經貿職缺700筆實證資料庫.json" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> JSON
                                    </a>
                                </div>
                            </div>

                            <!-- 03. 教育部 113 在學生統計 -->
                            <div class="p-3.5 sm:p-4 hover:bg-slate-50/80 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2 py-0.5 rounded bg-slate-900 text-white font-mono text-[10px] font-bold">03</span>
                                        <strong class="text-xs sm:text-sm text-slate-900">教育部 113 學年度大專校院各校學生數原始資料</strong>
                                        <span class="px-2 py-0.2 rounded-full text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">737 列全量</span>
                                    </div>
                                    <p class="text-[11px] text-slate-500">全國大專各校各學制男女在學生、大一新生實招數官方最底層全量母體。</p>
                                    <div class="flex items-center gap-2 text-[11px] text-stone-500">
                                        <span class="font-medium">官方驗證：</span>
                                        <a href="https://udb.moe.edu.tw/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">
                                            教育部大專校院校務資訊公開平台 (UDB) <i data-lucide="external-link" class="w-3 h-3"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <a href="raw_data/03_教育部113學年度大專校院各校學生數原始資料.csv" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> 下載 CSV
                                    </a>
                                </div>
                            </div>

                            <!-- 04. 教育部 112 在學生統計 -->
                            <div class="p-3.5 sm:p-4 hover:bg-slate-50/80 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2 py-0.5 rounded bg-slate-900 text-white font-mono text-[10px] font-bold">04</span>
                                        <strong class="text-xs sm:text-sm text-slate-900">教育部 112 學年度大專校院各校學生數原始資料</strong>
                                        <span class="px-2 py-0.2 rounded-full text-[10px] font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">764 列全量</span>
                                    </div>
                                    <p class="text-[11px] text-slate-500">全國大專各校各學制男女在學生、大一新生實招數官方基期比對母體。</p>
                                    <div class="flex items-center gap-2 text-[11px] text-stone-500">
                                        <span class="font-medium">官方驗證：</span>
                                        <a href="https://udb.moe.edu.tw/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">
                                            教育部大專校院校務資訊公開平台 (UDB) <i data-lucide="external-link" class="w-3 h-3"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <a href="raw_data/04_教育部112學年度大專校院各校學生數原始資料.csv" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> 下載 CSV
                                    </a>
                                </div>
                            </div>

                            <!-- 05. 6年統測錄取分走勢 -->
                            <div class="p-3.5 sm:p-4 hover:bg-slate-50/80 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2 py-0.5 rounded bg-slate-900 text-white font-mono text-[10px] font-bold">05</span>
                                        <strong class="text-xs sm:text-sm text-slate-900">109 至 114 學年度商管群統測最低錄取分與單科均分</strong>
                                        <span class="px-2 py-0.2 rounded-full text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200">6 年走勢</span>
                                    </div>
                                    <p class="text-[11px] text-slate-500">中科國貿、中科企管、雲科國管、北商國商、勤益企管歷年最低門檻與單科均分。</p>
                                    <div class="flex items-center gap-2 text-[11px] text-stone-500">
                                        <span class="font-medium">官方驗證：</span>
                                        <a href="https://www.jctv.ntut.edu.tw/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">
                                            技專校院招生委員會聯合會 (JCTV) <i data-lucide="external-link" class="w-3 h-3"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <a href="raw_data/05_109至114學年度商管群統測最低錄取分與單科均分.csv" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> 下載 CSV
                                    </a>
                                </div>
                            </div>

                            <!-- 06. 全國國立商管六強指標 -->
                            <div class="p-3.5 sm:p-4 hover:bg-slate-50/80 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2 py-0.5 rounded bg-slate-900 text-white font-mono text-[10px] font-bold">06</span>
                                        <strong class="text-xs sm:text-sm text-slate-900">全國國立商管六強戰略旗盤指標矩陣</strong>
                                        <span class="px-2 py-0.2 rounded-full text-[10px] font-medium bg-rose-50 text-rose-700 border border-rose-200">6 所旗艦系所</span>
                                    </div>
                                    <p class="text-[11px] text-slate-500">北商國商、中科國貿、雲科國管、高科航管/國企/供應鏈學生結構、師資比、註冊率與特色。</p>
                                    <div class="flex items-center gap-2 text-[11px] text-stone-500">
                                        <span class="font-medium">官方驗證：</span>
                                        <a href="https://udb.moe.edu.tw/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">
                                            教育部大專校院校務資訊公開平台 <i data-lucide="external-link" class="w-3 h-3"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <a href="raw_data/06_全國國立商管六強戰略旗盤指標矩陣.csv" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> 下載 CSV
                                    </a>
                                </div>
                            </div>

                            <!-- 07. 少子化海嘯 16 年推估 -->
                            <div class="p-3.5 sm:p-4 hover:bg-slate-50/80 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2 py-0.5 rounded bg-slate-900 text-white font-mono text-[10px] font-bold">07</span>
                                        <strong class="text-xs sm:text-sm text-slate-900">113 至 128 學年度少子化海嘯 16 年動態模擬推估</strong>
                                        <span class="px-2 py-0.2 rounded-full text-[10px] font-medium bg-indigo-50 text-indigo-700 border border-indigo-200">16 年序列</span>
                                    </div>
                                    <p class="text-[11px] text-slate-500">全國大一新生數、統測人數、商管群人數、中科日間錄取分底線與進修四技存活年限精算。</p>
                                    <div class="flex items-center gap-2 text-[11px] text-stone-500">
                                        <span class="font-medium">官方驗證：</span>
                                        <a href="https://depart.moe.edu.tw/ED4500/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">
                                            教育部統計處學生數預測報告 <i data-lucide="external-link" class="w-3 h-3"></i>
                                        </a>
                                        <span class="text-slate-300">|</span>
                                        <a href="https://www.ris.gov.tw/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">
                                            內政部戶政司人口統計 <i data-lucide="external-link" class="w-3 h-3"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <a href="raw_data/07_113至128學年度少子化海嘯16年動態模擬推估.csv" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> 下載 CSV
                                    </a>
                                </div>
                            </div>

                            <!-- 08. 中科國貿學制與體質 -->
                            <div class="p-3.5 sm:p-4 hover:bg-slate-50/80 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2 py-0.5 rounded bg-slate-900 text-white font-mono text-[10px] font-bold">08</span>
                                        <strong class="text-xs sm:text-sm text-slate-900">中科國貿各學制體質診斷與休退學註冊率消長</strong>
                                        <span class="px-2 py-0.2 rounded-full text-[10px] font-medium bg-amber-50 text-amber-700 border border-amber-200">5 大學制</span>
                                    </div>
                                    <p class="text-[11px] text-slate-500">日間四技、進修四技、日間五專、日間碩士、碩專班之核定名額、註冊率、休退學人數與主因。</p>
                                    <div class="flex items-center gap-2 text-[11px] text-stone-500">
                                        <span class="font-medium">數據來源：</span>
                                        <span class="text-stone-700 font-medium">國立臺中科技大學 校務系統 IR 實證統計</span>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <a href="raw_data/08_中科國貿各學制體質診斷與休退學註冊率消長.csv" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> 下載 CSV
                                    </a>
                                </div>
                            </div>

                            <!-- 09. 117 全台 72 所技專存活預測 -->
                            <div class="p-3.5 sm:p-4 hover:bg-slate-50/80 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2 py-0.5 rounded bg-slate-900 text-white font-mono text-[10px] font-bold">09</span>
                                        <strong class="text-xs sm:text-sm text-slate-900">117 學年度全台 72 所技專校院存活推估矩陣</strong>
                                        <span class="px-2 py-0.2 rounded-full text-[10px] font-medium bg-red-50 text-red-700 border border-red-200">72 所技專全量</span>
                                    </div>
                                    <p class="text-[11px] text-slate-500">公立安全區(14校)、財團大校(10校)、穩健特色(14校)、生死拉鋸(14校)與高危深水(20校)存活分層推估。</p>
                                    <div class="flex items-center gap-2 text-[11px] text-stone-500">
                                        <span class="font-medium">官方驗證：</span>
                                        <a href="https://udb.moe.edu.tw/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">
                                            教育部大專校院學生統計與技職統測生源腰斬精算 <i data-lucide="external-link" class="w-3 h-3"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <a href="raw_data/09_117學年度全台72所技專校院存活推估矩陣.csv" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> 下載 CSV
                                    </a>
                                </div>
                            </div>

                            <!-- 10. 117 全台 61 所普通大學存活預測 -->
                            <div class="p-3.5 sm:p-4 hover:bg-slate-50/80 transition flex flex-col md:flex-row md:items-center justify-between gap-3">
                                <div class="space-y-1">
                                    <div class="flex items-center gap-2">
                                        <span class="px-2 py-0.5 rounded bg-slate-900 text-white font-mono text-[10px] font-bold">10</span>
                                        <strong class="text-xs sm:text-sm text-slate-900">117 學年度全台 61 所普通大學存活推估矩陣</strong>
                                        <span class="px-2 py-0.2 rounded-full text-[10px] font-medium bg-red-50 text-red-700 border border-red-200">61 所普大全量</span>
                                    </div>
                                    <p class="text-[11px] text-slate-500">公立頂大(26校)、老牌名校(15校)、中度拉鋸(13校)、退場捐贈(中華大學)與高危深水(6校)預測。</p>
                                    <div class="flex items-center gap-2 text-[11px] text-stone-500">
                                        <span class="font-medium">官方驗證：</span>
                                        <a href="https://udb.moe.edu.tw/" target="_blank" rel="noopener" class="text-sky-600 hover:underline inline-flex items-center gap-0.5">
                                            教育部學生統計與教育部核定停招停辦公告 <i data-lucide="external-link" class="w-3 h-3"></i>
                                        </a>
                                    </div>
                                </div>
                                <div class="flex items-center gap-2 flex-shrink-0">
                                    <a href="raw_data/10_117學年度全台61所普通大學存活推估矩陣.csv" download class="px-2.5 py-1.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-800 font-semibold text-[11px] flex items-center gap-1 border border-slate-300 transition">
                                        <i data-lucide="download" class="w-3 h-3"></i> 下載 CSV
                                    </a>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>

                <!-- 數據引用與系所評鑑規範指南 -->
                <div class="p-4 rounded-xl bg-slate-100 border border-slate-200 text-slate-600">
                    <h5 class="text-xs font-bold text-slate-900 mb-1">💡 數據應用與委員會自評指引 (Usage & Citation Recommendations)</h5>
                    <ul class="list-disc pl-4 space-y-1 text-[11px] leading-relaxed">
                        <li><strong>招生委員會生源防守：</strong>請引用 <strong>01 交叉查榜 (504筆)</strong> 作為高科大 (航管/國企/運籌) 及逢甲國貿之生源天敵防禦與備取遞補策略。</li>
                        <li><strong>課程委員會與就業接軌：</strong>請引用 <strong>02 104 職缺庫 (700筆)</strong> 作為增設「跨境電商實作」與「生成式 AI 商務提示工程」之實證產業背書。</li>
                        <li><strong>院務與校級中長程發展：</strong>請引用 <strong>07 少子化推估</strong>、<strong>09 技專存活矩陣</strong> 與 <strong>10 普大存活矩陣</strong> 作為 117 虎年海嘯進修部轉型專班之智庫依據。</li>
                    </ul>
                </div>
            </div>

            <!-- Modal Footer -->
            <div class="p-3 sm:p-4 border-t border-slate-200 bg-white flex items-center justify-between">
                <div class="text-[11px] font-mono text-slate-400">
                    NUTC IB Comprehensive IR Raw Data Pack · Version 3.2
                </div>
                <div class="flex items-center gap-2">
                    <button onclick="closeDataModal()" class="px-4 py-2 rounded-lg bg-slate-200 hover:bg-slate-300 text-slate-700 font-bold text-xs transition">
                        關閉視窗
                    </button>
                    <button onclick="exportComprehensiveMasterRawCSV()" class="px-4 py-2 rounded-lg bg-[#f05138] hover:bg-[#e04830] text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition">
                        <i data-lucide="download" class="w-3.5 h-3.5"></i>
                        <span>匯出全量 CSV</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
'''

# Check if #spec-modal exists and place #raw-data-modal right after it
if 'id="spec-modal"' in html:
    # Find closing of spec-modal
    idx = html.find('</div>\n    </div>', html.find('id="spec-modal"'))
    if idx != -1:
        insert_pos = idx + len('</div>\n    </div>')
        html = html[:insert_pos] + '\n' + raw_data_modal_html + html[insert_pos:]
        print("Successfully injected #raw-data-modal HTML!")
    else:
        print("Could not find end of spec-modal, injecting before </body>")
        html = html.replace('</body>', raw_data_modal_html + '\n</body>')
else:
    html = html.replace('</body>', raw_data_modal_html + '\n</body>')

# 2. Update Header buttons
# Replace existing export button in Header
header_old = '''                    <button onclick="exportAllCSV()" class="px-2.5 py-1 sm:px-3.5 sm:py-1.5 rounded-sm bg-[#f05138] hover:bg-[#e04830] text-white text-[11px] sm:text-xs font-bold flex items-center gap-1 whitespace-nowrap shadow-xs transition">
                        <i data-lucide="download" class="w-3.5 h-3.5"></i>
                        <span>匯出全量 CSV</span>
                    </button>'''

header_new = '''                    <button onclick="openDataModal()" class="px-2.5 py-1 sm:px-3 sm:py-1.5 rounded-sm bg-[#f05138] hover:bg-[#e04830] text-white text-[11px] sm:text-xs font-bold flex items-center gap-1.5 whitespace-nowrap shadow-xs transition">
                        <i data-lucide="database" class="w-3.5 h-3.5"></i>
                        <span class="hidden sm:inline">實證 Raw Data 驗證中心</span>
                        <span class="inline sm:hidden">Raw Data</span>
                    </button>
                    <button onclick="exportComprehensiveMasterRawCSV()" class="hidden md:flex px-2.5 py-1 sm:px-3 sm:py-1.5 rounded-sm bg-stone-800 hover:bg-stone-700 text-stone-200 text-[11px] sm:text-xs font-medium items-center gap-1 whitespace-nowrap border border-stone-700 transition">
                        <i data-lucide="download" class="w-3 h-3 text-stone-400"></i>
                        <span>匯出全量 CSV</span>
                    </button>'''

if header_old in html:
    html = html.replace(header_old, header_new)
    print("Updated Header button!")
else:
    print("Header old pattern not found, trying regex...")
    html = re.sub(
        r'<button onclick="exportAllCSV\(\)" class="px-2\.5 py-1 sm:px-3\.5 sm:py-1\.5 rounded-sm bg-\[#f05138\] hover:bg-\[#e04830\] text-white text-\[11px\] sm:text-xs font-bold flex items-center gap-1 whitespace-nowrap shadow-xs transition">.*?<span>匯出全量 CSV</span>\s*</button>',
        header_new,
        html,
        flags=re.DOTALL
    )

# 3. Update Desktop Sidebar Footer
sidebar_old = '''                <button onclick="exportAllCSV()" class="w-full px-3 py-2 rounded-md bg-[#f05138] hover:bg-[#e04830] text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition">
                    <i data-lucide="download" class="w-3.5 h-3.5"></i>
                    <span>匯出全量 CSV</span>
                </button>'''

sidebar_new = '''                <button onclick="openDataModal()" class="w-full px-3 py-2 rounded-md bg-[#f05138] hover:bg-[#e04830] text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition">
                    <i data-lucide="database" class="w-3.5 h-3.5"></i>
                    <span>實證 Raw Data 驗證中心</span>
                </button>
                <button onclick="exportComprehensiveMasterRawCSV()" class="w-full px-3 py-1.5 rounded-md bg-[#27272a] hover:bg-[#3f3f46] text-stone-300 text-[11px] font-medium flex items-center justify-center gap-1.5 transition">
                    <i data-lucide="download" class="w-3 h-3 text-stone-400"></i>
                    <span>匯出全量 CSV</span>
                </button>'''

if sidebar_old in html:
    html = html.replace(sidebar_old, sidebar_new)
    print("Updated Sidebar footer!")
else:
    print("Sidebar old pattern not found, trying regex...")
    html = re.sub(
        r'<button onclick="exportAllCSV\(\)" class="w-full px-3 py-2 rounded-md bg-\[#f05138\] hover:bg-\[#e04830\] text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm transition">.*?<span>匯出全量 CSV</span>\s*</button>',
        sidebar_new,
        html,
        flags=re.DOTALL
    )

# 4. Update Mobile Sidebar Drawer Footer
mobile_old = '''                <button onclick="exportAllCSV(); closeMobileSidebar();" class="w-full px-3 py-2.5 rounded-md bg-[#f05138] text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm">
                    <i data-lucide="download" class="w-4 h-4"></i>
                    <span>匯出全量 CSV</span>
                </button>'''

mobile_new = '''                <button onclick="openDataModal(); closeMobileSidebar();" class="w-full px-3 py-2.5 rounded-md bg-[#f05138] text-white text-xs font-bold flex items-center justify-center gap-2 shadow-sm">
                    <i data-lucide="database" class="w-4 h-4"></i>
                    <span>實證 Raw Data 驗證中心</span>
                </button>
                <button onclick="exportComprehensiveMasterRawCSV(); closeMobileSidebar();" class="w-full px-3 py-2 rounded-md bg-stone-800 text-stone-300 text-xs font-medium flex items-center justify-center gap-2">
                    <i data-lucide="download" class="w-3.5 h-3.5 text-stone-400"></i>
                    <span>匯出全量 CSV</span>
                </button>'''

if mobile_old in html:
    html = html.replace(mobile_old, mobile_new)
    print("Updated Mobile drawer footer!")

# 5. Inject survival data arrays and open/close modal functions and exportComprehensiveMasterRawCSV
js_injection = f'''
        // =========================================================================
        // 全專案 117 學年度大專校院存活推估矩陣 (72所技專 + 61所普通大學)
        // =========================================================================
        const TECH_SURVIVAL_72 = {json.dumps(tech_72_json, ensure_ascii=False)};
        const UNIV_SURVIVAL_61 = {json.dumps(univ_61_json, ensure_ascii=False)};

        // Modal 控制函式
        function openDataModal() {{
            const m = document.getElementById('raw-data-modal');
            if (m) {{
                m.classList.remove('hidden');
                if (window.lucide && typeof lucide.createIcons === 'function') lucide.createIcons();
            }}
        }}

        function closeDataModal() {{
            const m = document.getElementById('raw-data-modal');
            if (m) m.classList.add('hidden');
        }}

        // =========================================================================
        // 全量 Master Raw CSV 綜合匯出函式 (匯出所有 10 個核心資料集之完整原始資料)
        // =========================================================================
        function exportComprehensiveMasterRawCSV() {{
            const lines = [
                '# ===================================================================================',
                '# 國立臺中科技大學 國際貿易與經營系 (NUTC IB) 校務研究策略分析全量實證資料庫 (Master Dataset)',
                '# 官方資料來源：教育部統計處大專公開平臺 (UDB)、技專校院招聯會 (JCTV)、104人力銀行實境庫、交叉查榜母體',
                '# 檔案編碼：UTF-8 with BOM (Microsoft Excel / Numbers 完美支援開檔不亂碼)',
                '# ===================================================================================',
                '',
                '# -----------------------------------------------------------------------------------',
                '# 【表一】全國國立科大 國貿/商務/航管/供應鏈 六強旗艦指標矩陣',
                '# -----------------------------------------------------------------------------------',
                '代號,學校名稱,系所名稱,區域,在學總人數,五專部人數,日間學士人數,進修學士人數,碩博生人數,專任師資總數,正教授,副教授,助理教授,境外生人數,境外生比率(%),114日間四技註冊率(%),114統測單科均分(分),113退學人數,113退學率(%)',
                ...DB.regional_six.map(x => [
                    x.code, x.school, x.dept, x.region, x.total_stu, x.five_year, x.undergrad_day, x.undergrad_eve, x.grad, x.faculty_total, x.faculty_prof, x.faculty_assoc, x.faculty_asst, x.oversea_stu, x.oversea_pct, x.reg_114_rate, x.score_114, x.drop_cnt_113, x.drop_rate_113
                ].join(',')),
                '',
                '# -----------------------------------------------------------------------------------',
                '# 【表二】中部大專商管競爭系所綜合情報比對',
                '# -----------------------------------------------------------------------------------',
                '學校系所,定位類型,核定名額現況,114日間註冊率(%),114進修註冊率(%),門檻均分估值(分),在學總人數,退學流失率(%),財務現金存量,每學期學費,生源管道分流,戰略威脅等級',
                ...DB.central_competitors.map(c => [
                    c.school, c.type, `"${{c.quota_status}}"`, c.reg_114_day, c.reg_114_eve, c.score_cutoff, c.students_total, c.drop_rate, `"${{c.cash_reserve}}"`, `"${{c.tuition_per_sem}}"`, `"${{c.source_mix}}"`, `"${{c.threat_level}}"`
                ].join(',')),
                '',
                '# -----------------------------------------------------------------------------------',
                '# 【表三】全國國立科大商管旗艦 6 年統測單科均分走勢 (109~114學年度)',
                '# -----------------------------------------------------------------------------------',
                '學年度,中科大國貿,北商大國商,雲科大國管,高科大航管,高科大國企,高科供應鏈',
                ...DB.score_trends.years.map((y, i) => {{
                    const itm = DB.score_trends.departments['中科大國貿'][i];
                    const ntub = DB.score_trends.departments['北商大國商'][i];
                    const yun = DB.score_trends.departments['雲科大國管'][i];
                    const ship = DB.score_trends.departments['高科大航管'][i];
                    const ib = DB.score_trends.departments['高科大國企'][i];
                    const scm = DB.score_trends.departments['高科供應鏈'][i];
                    return `${{y}}學年,${{itm}},${{ntub}},${{yun}},${{ship}},${{ib}},${{scm}}`;
                }}),
                '',
                '# -----------------------------------------------------------------------------------',
                '# 【表四】中科國貿 各學制新生註冊率、名額消長與退學原因體質矩陣',
                '# -----------------------------------------------------------------------------------',
                '學制班別,113學年度註冊率,114學年度註冊率,體質狀態,戰略消長與因應策略',
                '"日間學士班 (含四技)","100.00% (80/80)","99.06% (79/80, 境+26)","常年滿招・核心主力","生源防守穩健，外加境外專班充裕"',
                '"日間二年制 (二技)","97.37% (37/38)","100.00% (38/38, 境+1)","100% 滿招","五專畢業直升四技/二技核心管道"',
                '"進修學士班 (進修四技)","53.75% (43/80)","50.91% (28/55)","深水警戒區","核定主動減招25名，仍受在地夜校生源緊縮衝擊"',
                '"進修二年制 (夜二技)","62.67% (47/75)","89.09% (49/55)","大幅回彈 (+26.4%)","減招20名後成效立竿見影，註冊率衝回近9成"',
                '"日間五專部 (國貿科)","100.00% (50/50)","100.00% (50/50)","常年 100% 額滿","國中直升一中商圈名校，生源穩健優勢顯著"',
                '',
                '# -----------------------------------------------------------------------------------',
                '# 【表五】教育部 113~128 學年度少子化預測基準模型 (16年動態推估)',
                '# -----------------------------------------------------------------------------------',
                '學年度,全國大一新生總數(萬人),統測報考總數(萬人),商管群人數(萬人),中部商管生源池(人),中科日間錄取均分推估(分),中科進修部註冊率推估(%),五專部防護力',
                ...DB.fertility_timeline.map(f => [
                    `${{f.yr}}學年`, f.fresh, f.tcte, f.biz, f.pool, f.day_score, f.eve_rate, `"${{f.five_def}}"`
                ].join(',')),
                '',
                '# -----------------------------------------------------------------------------------',
                '# 【表六】中科國貿 115~120學年度 專任師資退休換血與轉型排程',
                '# -----------------------------------------------------------------------------------',
                '學年度,預估退休人數,專長領域,員額釋出與轉型對策',
                ...DB.faculty_strategy.retire_schedule.map(s => [
                    `${{s.yr}}學年`, s.count, `"${{s.domain}}"`, `"${{s.detail}}"`
                ].join(',')),
                '',
                '# -----------------------------------------------------------------------------------',
                '# 【表七】113~115 學年度四技二專甄選交叉查榜 504 筆考生流向全量名冊',
                '# -----------------------------------------------------------------------------------',
                '序號,學年度,准考證號,考生姓名,來源錄取狀態,最後分發學校,最後分發系所,去向分類,最後分發狀態',
                ...MODULE6_CANDIDATES_504.map(r => [
                    r[0], `${{r[1]}}學年度`, r[2], `"${{r[3]}}"`, `"${{r[4]}}"`, `"${{r[5]}}"`, `"${{r[6]}}"`, `"${{r[7]}}"`, `"${{r[8]}}"`
                ].join(',')),
                '',
                '# -----------------------------------------------------------------------------------',
                '# 【表八】104 人力銀行中部經貿外銷/跨境電商/AI 經貿 700 筆真實職缺庫全量',
                '# -----------------------------------------------------------------------------------',
                '序號,軌道分類,職缺名稱,徵才企業,工作簡介摘要,縣市,鄉鎮區,薪資待遇,起薪低標,起薪高標,104官方直通連結,匹配關鍵技能',
                ...JOBS_104.map((j, idx) => [
                    idx + 1,
                    `"${{j.tr || ''}}"`,
                    `"${{(j.ti || '').replace(/"/g, '""')}}"`,
                    `"${{(j.co || '').replace(/"/g, '""')}}"`,
                    `"${{(j.sn || '').replace(/"/g, '""')}}"`,
                    `"${{j.cy || ''}}"`,
                    `"${{j.to || ''}}"`,
                    `"${{j.sa || ''}}"`,
                    j.sl || 0,
                    j.sh || 0,
                    `"${{j.url || ''}}"`,
                    `"${{(j.sk || []).join('; ')}}"`
                ].join(',')),
                '',
                '# -----------------------------------------------------------------------------------',
                '# 【表九】117 學年度全台 72 所技專校院存活推估矩陣',
                '# -----------------------------------------------------------------------------------',
                '學校代碼,學校名稱,公私立,學校類型,縣市,113全校總人數,113大一新生實招,日間大一生,進修大一生,117存活分層,117預估存活率,117命運與因應策略推估',
                ...TECH_SURVIVAL_72.map(s => [
                    s.學校代碼, `"${{s.學校名稱}}"`, s.公私立, s.學校類型, s.縣市, s.113全校總人數, s.113大一新生實招, s.日間大一生, s.進修大一生, `"${{s.117存活分層}}"`, s.117預估存活率, `"${{s.117命運與因應策略推估}}"`
                ].join(',')),
                '',
                '# -----------------------------------------------------------------------------------',
                '# 【表十】117 學年度全台 61 所普通大學存活推估矩陣',
                '# -----------------------------------------------------------------------------------',
                '學校代碼,學校名稱,公私立,縣市,113全校總人數,113大一新生實招,日間大一生,進修大一生,117存活分層,117預估存活率,117命運與因應策略推估',
                ...UNIV_SURVIVAL_61.map(u => [
                    u.學校代碼, `"${{u.學校名稱}}"`, u.公私立, u.縣市, u.113全校總人數, u.113大一新生實招, u.日間大一生, u.進修大一生, `"${{u.117存活分層}}"`, u.117預估存活率, `"${{u.117命運與因應策略推估}}"`
                ].join(','))
            ];

            let csvContent = "\\uFEFF" + lines.join("\\n");
            const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8;' }});
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", "NUTC_IB_Comprehensive_Full_Raw_Data_Master.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }}

        // 舊版匯出介面相容導向
        function exportAllCSV() {{
            openDataModal();
        }}
'''

# Find a good spot to insert JS functions, right before function exportSimCSV()
if 'function exportSimCSV()' in html:
    html = html.replace('function exportSimCSV()', js_injection + '\n        function exportSimCSV()')
    print("Injected JS functions and survival data before exportSimCSV()!")
else:
    html = html.replace('</script>', js_injection + '\n    </script>')
    print("Injected JS before </script>!")

# 6. Ensure export104JobsCSV() exports ALL 700 jobs with description
old_export_104 = '''        function export104JobsCSV() {
            const headers = ['編號', '領域軌道', '職缺名稱', '徵才企業', '縣市', '鄉鎮市區', '薪資待遇描述', '起薪低標(NT$)', '高薪高標(NT$)', '104官方連結', '匹配關鍵技能'];
            const rows = filteredJobs.map((j, idx) => [
                idx + 1,
                `"${j.tr}"`,
                `"${j.ti.replace(/"/g, '""')}"`,
                `"${j.co.replace(/"/g, '""')}"`,
                `"${j.cy}"`,
                `"${j.to}"`,
                `"${j.sa}"`,
                j.sl,
                j.sh,
                `"${j.url}"`,
                `"${(j.sk || []).join('; ')}"`
            ]);

            const csvContent = "\\uFEFF" + [headers.join(','), ...rows.map(r => r.join(','))].join('\\n');
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", `NUTC_104_Central_Taiwan_Jobs_${currentJobsTrack}_N${filteredJobs.length}.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }'''

new_export_104 = '''        function export104JobsCSV() {
            const headers = ['編號', '領域軌道', '職缺名稱', '徵才企業', '工作簡介摘要', '縣市', '鄉鎮市區', '薪資待遇描述', '起薪低標(NT$)', '高薪高標(NT$)', '104官方直通連結', '匹配關鍵技能'];
            const rows = JOBS_104.map((j, idx) => [
                idx + 1,
                `"${j.tr || ''}"`,
                `"${(j.ti || '').replace(/"/g, '""')}"`,
                `"${(j.co || '').replace(/"/g, '""')}"`,
                `"${(j.sn || '').replace(/"/g, '""')}"`,
                `"${j.cy || ''}"`,
                `"${j.to || ''}"`,
                `"${j.sa || ''}"`,
                j.sl || 0,
                j.sh || 0,
                `"${j.url || ''}"`,
                `"${(j.sk || []).join('; ')}"`
            ]);

            const csvContent = "\\uFEFF" + [headers.join(','), ...rows.map(r => r.join(','))].join('\\n');
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const url = URL.createObjectURL(blob);
            const link = document.createElement("a");
            link.setAttribute("href", url);
            link.setAttribute("download", `NUTC_104_Central_Taiwan_Jobs_Full_700.csv`);
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        }'''

if old_export_104 in html:
    html = html.replace(old_export_104, new_export_104)
    print("Updated export104JobsCSV to export full 700 jobs!")
else:
    print("Could not match exact old_export_104, trying pattern replacement...")
    html = re.sub(
        r'function export104JobsCSV\(\)\s*\{.*?URL\.revokeObjectURL.*?\n\s*\}|function export104JobsCSV\(\)\s*\{.*?document\.body\.removeChild\(link\);\s*\}',
        new_export_104,
        html,
        flags=re.DOTALL
    )

# Save back to interactive_dashboard.html, index.html, and dist/index.html
for path in [
    "/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html",
    "/Users/chenchunchih/Downloads/校務資料/index.html",
    "/Users/chenchunchih/Downloads/校務資料/dist/index.html"
]:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Updated {path} successfully ({os.path.getsize(path)} bytes)")

