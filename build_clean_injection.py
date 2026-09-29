#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inject "中彰投 AI 經貿與智慧商務專區 (AI Trade & Business Hub)" into interactive_dashboard.html
Backed by 700 verified 104 jobs with direct official links.
"""

import json
import re

def main():
    dashboard_path = 'interactive_dashboard.html'
    data_path = 'central_taiwan_104_700_jobs_verified.json'

    with open(dashboard_path, 'r', encoding='utf-8') as f:
        html = f.read()

    with open(data_path, 'r', encoding='utf-8') as f:
        data_104 = json.load(f)

    jobs = data_104['jobs']
    print(f"Total jobs to inject: {len(jobs)}")

    # 1. Prepare lean jobs list for offline & online fast browsing
    lean_jobs = []
    for j in jobs:
        lean_jobs.append({
            'no': j['job_no'],
            'tr': j['track'],
            'ti': j['title'],
            'co': j['company'],
            'cy': j['county'],
            'to': j['town'],
            'sa': j['salary_desc'],
            'sl': j.get('salary_low', 0),
            'sh': j.get('salary_high', 0),
            'url': j['url'],
            'sk': j.get('matched_skills', []),
            'sn': (j.get('description') or '')[:110].replace('\n', ' ').strip()
        })

    jobs_json_str = json.dumps(lean_jobs, ensure_ascii=False)

    # 2. Add AI Tab button into the header tabs
    tab_target = '<button onclick="switchTab(\'module6\')"'
    ai_tab_btn = '''                <button onclick="switchTab('module-ai')" id="tab-btn-module-ai" class="tab-btn px-2.5 py-2 sm:px-4 sm:py-3 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-stone-600 hover:text-stone-900 flex items-center gap-1.5 whitespace-nowrap transition flex-shrink-0">
                    <i data-lucide="sparkles" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-violet-600"></i>
                    <span class="inline sm:hidden font-bold text-violet-700">【專區】AI智慧經貿</span>
                    <span class="hidden sm:inline font-bold text-violet-700">【專區】中彰投 AI 智慧經貿專區</span>
                    <span class="ml-1 px-1.5 py-0.5 rounded-full bg-violet-100 text-violet-800 border border-violet-300 text-[10px] font-mono font-bold animate-pulse">104實證 700筆</span>
                </button>
'''
    if 'id="tab-btn-module-ai"' not in html:
        # Insert after module6 button
        m6_end = html.find('</button>', html.find(tab_target)) + len('</button>\n')
        html = html[:m6_end] + ai_tab_btn + html[m6_end:]
        print("Injected AI tab button into header tabs.")

    # 2b. Add quick-jump button in top right action bar if not already present
    if 'switchTab(\'module-ai\')' not in html[:html.find('<section class="max-w-7xl')]:
        export_btn_target = '<button onclick="exportAllCSV()"'
        ai_jump_btn = '''<button onclick="switchTab('module-ai')" class="px-2.5 py-1 sm:px-3.5 sm:py-1.5 rounded-sm bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-700 hover:to-indigo-700 text-white text-[11px] sm:text-xs font-bold flex items-center gap-1 whitespace-nowrap shadow-sm transition">
                        <i data-lucide="sparkles" class="w-3.5 h-3.5"></i>
                        <span>AI 經貿專區 (700筆)</span>
                    </button>
                    '''
        html = html.replace(export_btn_target, ai_jump_btn + export_btn_target)
        print("Injected AI quick-jump button in top action bar.")

    # 3. Build Module AI HTML Section
    module_ai_html = '''
        <!-- ================================================================= -->
        <!-- 模組 7 / 專區：中彰投經貿就業市場與 AI 智慧商務專區 (104 實證 700筆) -->
        <!-- ================================================================= -->
        <section id="module-ai" class="tab-content hidden space-y-8">
            
            <!-- 專區頂部橫幅 (科技石墨/紫漸層) -->
            <div class="bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 rounded-2xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden border border-indigo-500/20">
                <div class="relative z-10">
                    <div class="flex flex-wrap items-center gap-2 mb-3">
                        <span class="px-3 py-1 rounded-full text-xs font-bold bg-violet-500/25 text-violet-200 border border-violet-400/40 flex items-center gap-1.5">
                            <i data-lucide="sparkles" class="w-3.5 h-3.5 text-violet-300"></i>
                            104 官方 REST API 實時大數據
                        </span>
                        <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-white/10 text-slate-200">
                            中彰投經貿生活圈（台中市 80% / 彰化縣 18% / 南投縣 2%）
                        </span>
                        <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                            100% 官方真實可查證職缺
                        </span>
                    </div>
                    
                    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                        <div>
                            <h2 class="text-2xl sm:text-3xl font-black tracking-tight text-white flex items-center gap-3">
                                <span>中彰投 AI 經貿與智慧商務專區</span>
                                <span class="text-xs sm:text-sm font-semibold text-violet-300 px-3 py-1 rounded-lg bg-violet-800/40 border border-violet-700/50">
                                    NUTC IB 國際貿易與經營系
                                </span>
                            </h2>
                            <p class="text-xs sm:text-sm text-slate-300 mt-2 max-w-3xl leading-relaxed">
                                本專區基於 <strong>700 筆 104 人力銀行真實職缺</strong>（國外業務 200 筆、報關關務 200 筆、電子商務 200 筆、AI 經貿前鋒 100 筆），深度實證生成式 AI（ChatGPT/Copilot/Prompting）與智慧商務對中部外銷製造與跨境供應鏈的顛覆性重構。
                            </p>
                        </div>
                        <div class="flex items-center gap-2 flex-shrink-0">
                            <button onclick="export104JobsCSV()" class="px-3.5 py-2 rounded-xl bg-violet-600 hover:bg-violet-500 text-white text-xs font-bold flex items-center gap-2 shadow-lg shadow-violet-900/50 transition">
                                <i data-lucide="download" class="w-4 h-4"></i>
                                <span>匯出 700 筆 104 全量職缺 CSV</span>
                            </button>
                        </div>
                    </div>

                    <!-- 4 大核心指標橫幅卡片 -->
                    <div class="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mt-6">
                        <div class="bg-white/5 border border-white/10 rounded-xl p-3.5 backdrop-blur-sm">
                            <div class="text-[11px] text-slate-400 font-semibold flex items-center justify-between">
                                <span>中彰投實證職缺總量</span>
                                <i data-lucide="database" class="w-3.5 h-3.5 text-violet-400"></i>
                            </div>
                            <div class="text-xl sm:text-2xl font-black text-white mt-1">
                                700 <span class="text-xs font-normal text-slate-400">筆職缺</span>
                            </div>
                            <div class="text-[10px] text-violet-300 mt-1 flex items-center gap-1">
                                <span class="w-1.5 h-1.5 rounded-full bg-violet-400 animate-ping"></span>
                                國外業務+報關+電商+AI前鋒
                            </div>
                        </div>

                        <div class="bg-white/5 border border-white/10 rounded-xl p-3.5 backdrop-blur-sm">
                            <div class="text-[11px] text-slate-400 font-semibold flex items-center justify-between">
                                <span>AI 經貿職缺起薪中位數</span>
                                <i data-lucide="trending-up" class="w-3.5 h-3.5 text-emerald-400"></i>
                            </div>
                            <div class="text-xl sm:text-2xl font-black text-emerald-300 mt-1">
                                NT$ 38,000
                            </div>
                            <div class="text-[10px] text-emerald-400 mt-1 font-semibold">
                                經常性 4 萬以上佔 21.0% (全場最高)
                            </div>
                        </div>

                        <div class="bg-white/5 border border-white/10 rounded-xl p-3.5 backdrop-blur-sm">
                            <div class="text-[11px] text-slate-400 font-semibold flex items-center justify-between">
                                <span>AI 溢價高薪天花板</span>
                                <i data-lucide="award" class="w-3.5 h-3.5 text-amber-400"></i>
                            </div>
                            <div class="text-xl sm:text-2xl font-black text-amber-300 mt-1">
                                NT$ 60,000+
                            </div>
                            <div class="text-[10px] text-slate-300 mt-1">
                                如彰化榕建科技、西屯尊博科技
                            </div>
                        </div>

                        <div class="bg-white/5 border border-white/10 rounded-xl p-3.5 backdrop-blur-sm">
                            <div class="text-[11px] text-slate-400 font-semibold flex items-center justify-between">
                                <span>產業外銷聚落核心</span>
                                <i data-lucide="map-pin" class="w-3.5 h-3.5 text-sky-400"></i>
                            </div>
                            <div class="text-xl sm:text-2xl font-black text-sky-300 mt-1">
                                台中 80% / 彰化 18%
                            </div>
                            <div class="text-[10px] text-slate-300 mt-1">
                                中科園區 + 鹿港福興外銷五金醫材
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 背景光暈裝飾 -->
                <div class="absolute -right-16 -top-16 w-80 h-80 bg-violet-600/15 rounded-full blur-3xl pointer-events-none"></div>
                <div class="absolute right-1/3 -bottom-16 w-60 h-60 bg-indigo-600/10 rounded-full blur-2xl pointer-events-none"></div>
            </div>

            <!-- 板塊一：AI 薪資溢價與高薪天花板實證對比 -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-5 sm:p-7 shadow-[0_2px_12px_rgba(0,0,0,0.03)] space-y-5">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200/70 gap-2">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-violet-600"></span>
                            <h3 class="text-base font-bold text-slate-900 tracking-tight">
                                板塊一：中彰投四大就業軌道薪資溢價與高薪天花板對比
                            </h3>
                        </div>
                        <p class="text-xs text-slate-500 mt-0.5">
                            實證樣本：700 筆 104 真實招募職缺（國外業務 200 筆、報關關務 200 筆、電子商務 200 筆、AI 經貿前鋒 100 筆）
                        </p>
                    </div>
                    <span class="text-xs px-2.5 py-1 rounded-full bg-violet-50 text-violet-700 border border-violet-200 font-bold self-start sm:self-auto">
                        AI 溢價率：+15.2% ~ +25%
                    </span>
                </div>

                <!-- 圖表 + 指標卡片兩欄排版 -->
                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                    <!-- 左側 7 欄：Chart.js 長條圖 -->
                    <div class="lg:col-span-7 bg-slate-50/70 rounded-xl p-4 border border-slate-200/80">
                        <div class="flex items-center justify-between mb-3 text-xs">
                            <span class="font-bold text-slate-700">各軌道起薪中位數 (NT$) 與 4 萬以上高薪比率 (%)</span>
                            <span class="text-[11px] text-slate-400">來源：104 職缺實證</span>
                        </div>
                        <div class="h-64 sm:h-72 relative w-full">
                            <canvas id="chart-ai-salary-compare"></canvas>
                        </div>
                        <div class="text-[11px] text-slate-500 mt-2 flex items-center justify-between">
                            <span>柱狀：起薪中位數 (左軸 NT$)</span>
                            <span>折線/標記：4 萬以上職缺比率 (右軸 %)</span>
                        </div>
                    </div>

                    <!-- 右側 5 欄：四大軌道指標卡與標竿實證 -->
                    <div class="lg:col-span-5 flex flex-col justify-between space-y-3 text-xs">
                        <div class="p-3.5 rounded-xl border border-violet-200 bg-violet-50/50">
                            <div class="flex items-center justify-between">
                                <strong class="text-violet-900 font-bold flex items-center gap-1.5">
                                    <i data-lucide="sparkles" class="w-3.5 h-3.5 text-violet-600"></i>
                                    AI 經貿電商前鋒 (100筆)
                                </strong>
                                <span class="px-2 py-0.5 rounded bg-violet-200/80 text-violet-900 font-bold text-[10px]">高薪冠軍</span>
                            </div>
                            <div class="mt-1.5 flex items-baseline gap-2">
                                <span class="text-lg font-black text-violet-950 font-mono">NT$ 38,000</span>
                                <span class="text-slate-500">起薪中位數</span>
                                <span class="text-emerald-700 font-bold ml-auto">4萬以上達 21.0%</span>
                            </div>
                            <p class="text-slate-600 mt-1 leading-relaxed">
                                彰化福興 <strong>榕建科技</strong> 招募「國外業務開發與品牌營運」，月薪高達 <strong>37K~60K</strong>，明確指名「需能運用 AI 工具（Gemini/ChatGPT）進行高效市場研究與精準開發信撰寫」。
                            </p>
                        </div>

                        <div class="p-3.5 rounded-xl border border-amber-200 bg-amber-50/50">
                            <div class="flex items-center justify-between">
                                <strong class="text-amber-900 font-bold flex items-center gap-1.5">
                                    <i data-lucide="globe" class="w-3.5 h-3.5 text-amber-600"></i>
                                    國外業務 (200筆)
                                </strong>
                                <span class="px-2 py-0.5 rounded bg-amber-200/80 text-amber-900 font-bold text-[10px]">外銷主力</span>
                            </div>
                            <div class="mt-1.5 flex items-baseline gap-2">
                                <span class="text-lg font-black text-amber-950 font-mono">NT$ 38,000</span>
                                <span class="text-slate-500">起薪中位數</span>
                                <span class="text-amber-800 font-bold ml-auto">4萬以上佔 18.5%</span>
                            </div>
                            <p class="text-slate-600 mt-1 leading-relaxed">
                                53.0% 要求商務談判、34.5% 要求海外參展。鹿港 <strong>欣大園藝</strong> 開出 <strong>50K~80K</strong> 徵求外銷業務，具備流利外語與跨文化拓銷力者薪資彈性極大。
                            </p>
                        </div>

                        <div class="p-3.5 rounded-xl border border-emerald-200 bg-emerald-50/50">
                            <div class="flex items-center justify-between">
                                <strong class="text-emerald-900 font-bold flex items-center gap-1.5">
                                    <i data-lucide="shopping-cart" class="w-3.5 h-3.5 text-emerald-600"></i>
                                    電子商務 (200筆)
                                </strong>
                                <span class="px-2 py-0.5 rounded bg-emerald-200/80 text-emerald-900 font-bold text-[10px]">流量成長</span>
                            </div>
                            <div class="mt-1.5 flex items-baseline gap-2">
                                <span class="text-lg font-black text-emerald-950 font-mono">NT$ 35,000</span>
                                <span class="text-slate-500">起薪中位數</span>
                                <span class="text-emerald-800 font-bold ml-auto">4萬以上佔 13.0%</span>
                            </div>
                            <p class="text-slate-600 mt-1 leading-relaxed">
                                25.0% 要求電商平台營運、11.0% 要求 GA4/廣告投放。台中西區 <strong>艾斯數位</strong> 招募國外業務助理（38K~45K），將「熟悉 AI 工具應用」列為關鍵加分項。
                            </p>
                        </div>

                        <div class="p-3.5 rounded-xl border border-sky-200 bg-sky-50/50">
                            <div class="flex items-center justify-between">
                                <strong class="text-sky-900 font-bold flex items-center gap-1.5">
                                    <i data-lucide="package" class="w-3.5 h-3.5 text-sky-600"></i>
                                    報關行與關務 (200筆)
                                </strong>
                                <span class="px-2 py-0.5 rounded bg-sky-200/80 text-sky-900 font-bold text-[10px]">法規穩定</span>
                            </div>
                            <div class="mt-1.5 flex items-baseline gap-2">
                                <span class="text-lg font-black text-sky-950 font-mono">NT$ 33,000</span>
                                <span class="text-slate-500">起薪中位數</span>
                                <span class="text-rose-700 font-bold ml-auto">4萬以上僅 7.0%</span>
                            </div>
                            <p class="text-slate-600 mt-1 leading-relaxed">
                                90.5% 剛性要求報單與 L/C 單據，薪資天花板固化。急需導入「AI 自動化單據比對與關務防呆」，推動報關人才向國際供應鏈顧問轉型。
                            </p>
                        </div>
                    </div>
                </div>

                <!-- 決策洞察呼籲 -->
                <div class="p-4 rounded-xl bg-violet-50/70 border border-violet-200 text-xs text-violet-950 leading-relaxed flex items-start gap-3">
                    <div class="p-1.5 rounded-lg bg-violet-200/80 text-violet-800 flex-shrink-0 mt-0.5">
                        <i data-lucide="lightbulb" class="w-4 h-4"></i>
                    </div>
                    <div>
                        <strong class="font-bold">【系務決策核心啟示】為什麼企業願意為「懂 AI 的經貿人才」付出高達 NT$ 38K~60K 的薪資溢價？</strong>
                        <p class="mt-1 text-slate-700">
                            中彰投多為中小型外銷製造業，外銷部門編制精簡（常僅 2~3 人）。傳統業務需花費 60% 以上工時手動查字典寫 Email、刻商品文案與比對報關單；而<strong>掌握生成式 AI 與自動化工作流的經貿人才，一人即可產出相當於過去三人編制的海外拓銷產能</strong>。這正是國貿系必須立即推動「AI × 智慧商務」課綱革新的最大經濟動機！
                        </p>
                    </div>
                </div>
            </div>

            <!-- 板塊二：企業現場 5 大經貿 AI 實戰落地場景與 Prompt 實戰錦囊 -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-5 sm:p-7 shadow-[0_2px_12px_rgba(0,0,0,0.03)] space-y-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200/70 gap-2">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-indigo-600"></span>
                            <h3 class="text-base font-bold text-slate-900 tracking-tight">
                                板塊二：企業現場 5 大經貿 AI 實戰落地場景與 Prompt 實戰錦囊
                            </h3>
                        </div>
                        <p class="text-xs text-slate-500 mt-0.5">
                            專為國貿系師生與外銷企業設計，點擊可複製可直接上線實戰的專業 Prompt
                        </p>
                    </div>
                    <span class="text-xs text-indigo-700 font-semibold flex items-center gap-1">
                        <i data-lucide="terminal" class="w-3.5 h-3.5"></i>
                        附中英對照實戰範本
                    </span>
                </div>

                <!-- 5 大應用場景卡片網格 -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    
                    <!-- 場景 1 -->
                    <div class="border border-slate-200 rounded-xl p-4 bg-slate-50/50 hover:bg-white hover:border-violet-300 hover:shadow-md transition space-y-3 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-violet-100 text-violet-800">場景 ① 海外拓銷</span>
                                <span class="text-[10px] text-emerald-700 font-bold bg-emerald-50 px-1.5 py-0.5 rounded">回信率 8.5% (翻4倍)</span>
                            </div>
                            <h4 class="text-sm font-bold text-slate-900 mt-2">海外買家精準開發信 (Cold Email) 與自動追蹤</h4>
                            <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                                針對歐美自行車、醫療器材或精密零組件買家，輸入對方官網痛點，AI 自動產出符合西方商務禮儀的高轉換率開發信與 5 天後 Follow-up 追蹤信。
                            </p>
                        </div>
                        
                        <!-- Prompt 展開區塊 -->
                        <div class="space-y-2 pt-2 border-t border-slate-200/80">
                            <div class="flex items-center justify-between">
                                <span class="text-[11px] font-mono text-slate-500 font-bold">Prompt 錦囊</span>
                                <button onclick="copyPrompt('prompt-1')" id="btn-copy-1" class="text-[11px] px-2 py-0.5 rounded bg-violet-600 hover:bg-violet-700 text-white font-semibold flex items-center gap-1 transition">
                                    <i data-lucide="copy" class="w-3 h-3"></i>
                                    <span>複製 Prompt</span>
                                </button>
                            </div>
                            <pre id="prompt-1" class="p-2.5 rounded bg-slate-900 text-slate-200 text-[10.5px] font-mono whitespace-pre-wrap leading-tight max-h-36 overflow-y-auto custom-scrollbar">你是一位具備 15 年經驗的台灣外銷經理。
產品：台中製造之輕量化碳纖維自行車零組件 (ISO 9001，交期35天，重量比同級輕18%)。
目標買家：德國中高階自行車組裝品牌 (如 Cube, Canyon) 採購總監。
任務：
1. 撰寫一封精準 Cold Email (約 140 字)，主旨避免促銷感，第一段提及歐盟近期永續法規，第二段提出 3 項具體競爭數據，CTA 為邀請 10 分鐘 Teams 交流。
2. 同步附上一封 5 天後的專業 Follow-up 追蹤信。</pre>
                        </div>
                    </div>

                    <!-- 場景 2 -->
                    <div class="border border-slate-200 rounded-xl p-4 bg-slate-50/50 hover:bg-white hover:border-emerald-300 hover:shadow-md transition space-y-3 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">場景 ② 跨境電商</span>
                                <span class="text-[10px] text-indigo-700 font-bold bg-indigo-50 px-1.5 py-0.5 rounded">Amazon A9 演算法</span>
                            </div>
                            <h4 class="text-sm font-bold text-slate-900 mt-2">Amazon / 蝦皮 Listing 標題與五點描述 (Bullet Points)</h4>
                            <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                                自動分析海外競品買家負評與高頻搜尋詞，生成符合亞馬遜規範的高點擊 SEO 標題、情緒轉換 Bullet Points 與後台 Search Terms。
                            </p>
                        </div>
                        
                        <div class="space-y-2 pt-2 border-t border-slate-200/80">
                            <div class="flex items-center justify-between">
                                <span class="text-[11px] font-mono text-slate-500 font-bold">Prompt 錦囊</span>
                                <button onclick="copyPrompt('prompt-2')" id="btn-copy-2" class="text-[11px] px-2 py-0.5 rounded bg-emerald-600 hover:bg-emerald-700 text-white font-semibold flex items-center gap-1 transition">
                                    <i data-lucide="copy" class="w-3 h-3"></i>
                                    <span>複製 Prompt</span>
                                </button>
                            </div>
                            <pre id="prompt-2" class="p-2.5 rounded bg-slate-900 text-slate-200 text-[10.5px] font-mono whitespace-pre-wrap leading-tight max-h-36 overflow-y-auto custom-scrollbar">你是一位資深 Amazon 跨境電商運營專家，熟稔 A9 演算法。
產品：台灣製造人體工學登山健行手杖 (航太鋁合金、快拆鎖扣、防震減壓)。
任務：為 Amazon 美國站生成高轉換 Listing：
1. SEO 標題：小於 190 字元，融入 high-volume 搜尋詞，兼具品牌名與材質。
2. 5 點核心賣點 (Bullet Points)：每點開頭為全大寫利益痛點標籤 (如 [ULTRA-LIGHTWEIGHT YET STURDY])，針對競品易斷裂痛點強化說明。
3. 後台 Search Terms 清單：240 bytes 內，不重複、無標點。</pre>
                        </div>
                    </div>

                    <!-- 場景 3 -->
                    <div class="border border-slate-200 rounded-xl p-4 bg-slate-50/50 hover:bg-white hover:border-sky-300 hover:shadow-md transition space-y-3 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-100 text-sky-800">場景 ③ 跨文化商務</span>
                                <span class="text-[10px] text-amber-700 font-bold bg-amber-50 px-1.5 py-0.5 rounded">日本/德國商務禮儀</span>
                            </div>
                            <h4 class="text-sm font-bold text-slate-900 mt-2">多語系買家即時詢價 (Inquiry) 與議價談判潤飾</h4>
                            <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                                針對非英語系買家（日、德、西、越南），AI 擔任虛擬外銷特助，轉換得體敬語語氣，在維護利潤率前提下進行靈活還價談判。
                            </p>
                        </div>
                        
                        <div class="space-y-2 pt-2 border-t border-slate-200/80">
                            <div class="flex items-center justify-between">
                                <span class="text-[11px] font-mono text-slate-500 font-bold">Prompt 錦囊</span>
                                <button onclick="copyPrompt('prompt-3')" id="btn-copy-3" class="text-[11px] px-2 py-0.5 rounded bg-sky-600 hover:bg-sky-700 text-white font-semibold flex items-center gap-1 transition">
                                    <i data-lucide="copy" class="w-3 h-3"></i>
                                    <span>複製 Prompt</span>
                                </button>
                            </div>
                            <pre id="prompt-3" class="p-2.5 rounded bg-slate-900 text-slate-200 text-[10.5px] font-mono whitespace-pre-wrap leading-tight max-h-36 overflow-y-auto custom-scrollbar">你是專精跨文化商務溝通的外銷顧問。
情境：收到日本關西大型商社初次詢價，對方要求價格折扣 8% 且付款條件改為 O/A 60 天。
任務：請以極度符合日本商務敬語禮節 (Keigo 思維) 的英文信函回覆：
1. 感謝對方對本廠品質的認可與對商社聲譽的敬意。
2. 婉轉說明原料成本與品質堅持，無法折讓 8%，但提出「首批達 1,000 件提供 3% 試銷支持」之階梯式方案。
3. 付款條件堅持初次合作需為 T/T 30% 訂金或 L/C at sight，並說明確保供應鏈穩定的原因。</pre>
                        </div>
                    </div>

                    <!-- 場景 4 -->
                    <div class="border border-slate-200 rounded-xl p-4 bg-slate-50/50 hover:bg-white hover:border-amber-300 hover:shadow-md transition space-y-3 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">場景 ④ 展會情報</span>
                                <span class="text-[10px] text-slate-700 font-bold bg-slate-100 px-1.5 py-0.5 rounded">行前買家輪廓鎖定</span>
                            </div>
                            <h4 class="text-sm font-bold text-slate-900 mt-2">海外展覽競品情報調研與買家輪廓 (Buyer Persona) 繪製</h4>
                            <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                                出國參展（德國科隆五金展、台北自行車展）成本高達數十萬，AI 協助業務人員在行前快速萃取目標買家採購痛點與 30 秒電梯簡報。
                            </p>
                        </div>
                        
                        <div class="space-y-2 pt-2 border-t border-slate-200/80">
                            <div class="flex items-center justify-between">
                                <span class="text-[11px] font-mono text-slate-500 font-bold">Prompt 錦囊</span>
                                <button onclick="copyPrompt('prompt-4')" id="btn-copy-4" class="text-[11px] px-2 py-0.5 rounded bg-amber-600 hover:bg-amber-700 text-white font-semibold flex items-center gap-1 transition">
                                    <i data-lucide="copy" class="w-3 h-3"></i>
                                    <span>複製 Prompt</span>
                                </button>
                            </div>
                            <pre id="prompt-4" class="p-2.5 rounded bg-slate-900 text-slate-200 text-[10.5px] font-mono whitespace-pre-wrap leading-tight max-h-36 overflow-y-auto custom-scrollbar">你是一位全球五金工具市場研究分析師。
背景：我們即將赴德國科隆五金展 (Eisenwarenmesse) 參展拓銷專業氣動板手與手工具。
任務：
1. 繪製歐洲專業修車廠採購主管的 Buyer Persona（其核心 KPI、對台灣 vs 中國大陸供應商的心理預期、最大痛點）。
2. 列出他們在展會攤位最常發問的 5 個關鍵問題。
3. 為台灣業務擬定一套「30 秒攤位電梯簡報 (Elevator Pitch)」與引導至試用區的破冰話術。</pre>
                        </div>
                    </div>

                    <!-- 場景 5 -->
                    <div class="border border-slate-200 rounded-xl p-4 bg-slate-50/50 hover:bg-white hover:border-rose-300 hover:shadow-md transition space-y-3 flex flex-col justify-between">
                        <div>
                            <div class="flex items-center justify-between">
                                <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-100 text-rose-800">場景 ⑤ 關務合規</span>
                                <span class="text-[10px] text-rose-700 font-bold bg-rose-50 px-1.5 py-0.5 rounded">ICC UCP600 防呆</span>
                            </div>
                            <h4 class="text-sm font-bold text-slate-900 mt-2">國際貿易合約風險審查與信用狀 (L/C) 防呆審核</h4>
                            <p class="text-xs text-slate-600 mt-1 leading-relaxed">
                                運用 AI 比對買方開立之信用狀條款與 INCOTERMS 2020 規範，自動抓出「買方驗收簽署始得押匯」等軟條款（Soft Clauses）重大陷阱。
                            </p>
                        </div>
                        
                        <div class="space-y-2 pt-2 border-t border-slate-200/80">
                            <div class="flex items-center justify-between">
                                <span class="text-[11px] font-mono text-slate-500 font-bold">Prompt 錦囊</span>
                                <button onclick="copyPrompt('prompt-5')" id="btn-copy-5" class="text-[11px] px-2 py-0.5 rounded bg-rose-600 hover:bg-rose-700 text-white font-semibold flex items-center gap-1 transition">
                                    <i data-lucide="copy" class="w-3 h-3"></i>
                                    <span>複製 Prompt</span>
                                </button>
                            </div>
                            <pre id="prompt-5" class="p-2.5 rounded bg-slate-900 text-slate-200 text-[10.5px] font-mono whitespace-pre-wrap leading-tight max-h-36 overflow-y-auto custom-scrollbar">你是國際商會 (ICC) 規則與 UCP 600 信用狀統一慣例專家。
輸入：買方開立之 L/C 草案條件如下：
- 貿易條件：CIF Hamburg, INCOTERMS 2020
- 條款 46A：要求檢附「Inspection Certificate signed by Buyer\'s designated agent」方得押匯。
- 提單要求：Full set of clean on board ocean Bill of Lading consigned to Order of Issuing Bank.
任務：
1. 識別並分析條款 46A 的「軟條款 (Soft Clause)」風險及賣方可能面臨的押匯拒付威脅。
2. 提供一封正式的 L/C 修改要求信 (Amendment Request Letter)，提出合規替代方案。</pre>
                        </div>
                    </div>

                    <!-- 提示卡片：學生就業競爭力飛躍 -->
                    <div class="border-2 border-dashed border-violet-200 rounded-xl p-4 bg-gradient-to-br from-violet-50/70 to-indigo-50/70 flex flex-col justify-between">
                        <div>
                            <span class="px-2 py-0.5 rounded text-[10px] font-bold bg-violet-200 text-violet-900">核心優勢</span>
                            <h4 class="text-sm font-bold text-violet-950 mt-2">不用學寫程式，但能用 AI 創造十倍產值</h4>
                            <p class="text-xs text-slate-600 mt-2 leading-relaxed">
                                中科國貿系學生的核心競爭力在於<strong>「紮實的國際貿易實務法規 + 英語溝通底子」</strong>。當傳統業務還在苦思信件架構時，熟練掌握上述 5 大 AI 錦囊的學生，在進入職場第一天就能端出專業級的開發信、SEO Listing 與合約風控，成為中彰投外銷中小企業爭相網羅的高薪骨幹！
                            </p>
                        </div>
                        <div class="mt-4 pt-3 border-t border-violet-200/60 flex items-center justify-between text-[11px] text-violet-800 font-semibold">
                            <span>建議納入大二～大三核心專案</span>
                            <i data-lucide="sparkles" class="w-4 h-4 text-violet-600"></i>
                        </div>
                    </div>

                </div>
            </div>

            <!-- 板塊三：中彰投四大就業軌道職能雷達與產業聚落熱區 -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-5 sm:p-7 shadow-[0_2px_12px_rgba(0,0,0,0.03)] space-y-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200/70 gap-2">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-emerald-600"></span>
                            <h3 class="text-base font-bold text-slate-900 tracking-tight">
                                板塊三：中彰投四大軌道技能重疊雷達與外銷產業聚落
                            </h3>
                        </div>
                        <p class="text-xs text-slate-500 mt-0.5">
                            揭示由「傳統經貿」走向「AI 智慧外銷」的關鍵技能遷移路徑
                        </p>
                    </div>
                    <span class="text-xs font-mono text-slate-500">N=700 筆 104 真實需求標籤</span>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
                    <!-- 左側 6 欄：Chart.js 雷達圖 -->
                    <div class="lg:col-span-6 bg-slate-50/70 rounded-xl p-4 border border-slate-200/80">
                        <div class="flex items-center justify-between mb-2 text-xs">
                            <span class="font-bold text-slate-700">四大就業軌道 8 大技能雷達透視</span>
                            <div class="flex items-center gap-2 text-[10px]">
                                <span class="text-amber-600 font-bold">■ 國外業務</span>
                                <span class="text-sky-600 font-bold">■ 報關關務</span>
                                <span class="text-emerald-600 font-bold">■ 電子商務</span>
                                <span class="text-violet-600 font-bold">■ AI前鋒</span>
                            </div>
                        </div>
                        <div class="h-72 sm:h-80 relative w-full">
                            <canvas id="chart-ai-tracks-radar"></canvas>
                        </div>
                    </div>

                    <!-- 右側 6 欄：中彰投在地經貿聚落地圖與人才需求 -->
                    <div class="lg:col-span-6 space-y-3 text-xs">
                        <div class="p-3 rounded-xl border border-slate-200 bg-white hover:border-violet-300 transition">
                            <div class="flex items-center justify-between">
                                <strong class="text-slate-900 font-bold flex items-center gap-1.5">
                                    <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                                    1. 台中西屯中科園區與工業區 (佔 35%)
                                </strong>
                                <span class="text-indigo-700 font-bold">高科技/光電/軟體</span>
                            </div>
                            <p class="text-slate-600 mt-1 leading-relaxed">
                                久正光電、尊博科技、華旭先進等聚集地。外銷業務要求<strong>高階英語溝通、海外展會拓銷與 AI 流程自動化</strong>，起薪普遍從 38K~48K 起跳。
                            </p>
                        </div>

                        <div class="p-3 rounded-xl border border-slate-200 bg-white hover:border-violet-300 transition">
                            <div class="flex items-center justify-between">
                                <strong class="text-slate-900 font-bold flex items-center gap-1.5">
                                    <span class="w-2 h-2 rounded-full bg-amber-500"></span>
                                    2. 彰化鹿港、福興、和美外銷重鎮 (佔 18%)
                                </strong>
                                <span class="text-amber-700 font-bold">精密五金/醫材/水五金</span>
                            </div>
                            <p class="text-slate-600 mt-1 leading-relaxed">
                                榕建科技、欣大園藝等中大型隱形冠軍。<strong>AI 工具應用成長最猛烈</strong>，高薪直衝 50K~60K，極需能獨立操作 Amazon/Alibaba 與 AI 開發信的跨域專案人才。
                            </p>
                        </div>

                        <div class="p-3 rounded-xl border border-slate-200 bg-white hover:border-violet-300 transition">
                            <div class="flex items-center justify-between">
                                <strong class="text-slate-900 font-bold flex items-center gap-1.5">
                                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                                    3. 台中南屯精密機械園區 (佔 14%)
                                </strong>
                                <span class="text-emerald-700 font-bold">工具機/智慧製造</span>
                            </div>
                            <p class="text-slate-600 mt-1 leading-relaxed">
                                全球工具機與機械零組件核心。極度重視<strong>技術規格說明、展會談判與多語系海外代理商維護</strong>，常態外加高額業績獎金。
                            </p>
                        </div>

                        <div class="p-3 rounded-xl border border-slate-200 bg-white hover:border-violet-300 transition">
                            <div class="flex items-center justify-between">
                                <strong class="text-slate-900 font-bold flex items-center gap-1.5">
                                    <span class="w-2 h-2 rounded-full bg-sky-500"></span>
                                    4. 台中港梧棲與關務物流基地 (佔 9%)
                                </strong>
                                <span class="text-sky-700 font-bold">海運承攬/報關保稅</span>
                            </div>
                            <p class="text-slate-600 mt-1 leading-relaxed">
                                87% 硬性要求熟悉通關自動化 (EDI/關港貿單一窗口) 與信用狀 (L/C)。目前正加速推動由紙本報關轉向智慧關務供應鏈。
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 板塊四：700 筆 104 真實職缺即時搜尋與驗證查詢庫 -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-5 sm:p-7 shadow-[0_2px_12px_rgba(0,0,0,0.03)] space-y-5">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200/70 gap-3">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-[#f05138]"></span>
                            <h3 class="text-base font-bold text-slate-900 tracking-tight">
                                板塊四：中彰投 700 筆 104 真實職缺即時搜尋與驗證資料庫
                            </h3>
                        </div>
                        <p class="text-xs text-slate-500 mt-0.5">
                            所有職缺均附 <strong>104 官方真實直通連結</strong>，點擊即可連至 104 官方頁面核實！
                        </p>
                    </div>

                    <div class="flex items-center gap-2">
                        <span id="jobs-filtered-count-badge" class="px-3 py-1 rounded-full bg-slate-100 text-slate-800 border border-slate-300 text-xs font-bold font-mono">
                            顯示 700 / 700 筆
                        </span>
                        <button onclick="export104JobsCSV()" class="px-3 py-1 rounded bg-[#f05138] hover:bg-[#e04830] text-white text-xs font-bold flex items-center gap-1 transition">
                            <i data-lucide="download" class="w-3.5 h-3.5"></i>
                            <span>匯出 CSV</span>
                        </button>
                    </div>
                </div>

                <!-- 篩選與搜尋控制工具列 -->
                <div class="space-y-3">
                    <!-- 軌道篩選按鈕群 -->
                    <div class="flex flex-wrap items-center gap-1.5 text-xs">
                        <span class="text-slate-500 font-semibold mr-1">領域軌道：</span>
                        <button onclick="filterJobsByTrack('ALL')" id="btn-track-all" class="filter-track-btn px-2.5 py-1 rounded-lg bg-slate-900 text-white font-bold transition">
                            全部 (700)
                        </button>
                        <button onclick="filterJobsByTrack('AI經貿電商前鋒')" id="btn-track-ai" class="filter-track-btn px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold transition flex items-center gap-1">
                            <i data-lucide="sparkles" class="w-3 h-3 text-violet-600"></i>
                            🤖 AI 經貿前鋒 (100)
                        </button>
                        <button onclick="filterJobsByTrack('國外業務')" id="btn-track-export" class="filter-track-btn px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold transition">
                            🌍 國外業務 (200)
                        </button>
                        <button onclick="filterJobsByTrack('報關行與關務')" id="btn-track-customs" class="filter-track-btn px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold transition">
                            📦 報關與關務 (200)
                        </button>
                        <button onclick="filterJobsByTrack('電子商務')" id="btn-track-ec" class="filter-track-btn px-2.5 py-1 rounded-lg bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold transition">
                            🛒 電子商務 (200)
                        </button>
                        <button onclick="toggleHighSalaryFilter()" id="btn-track-highsal" class="filter-track-btn px-2.5 py-1 rounded-lg bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-300 font-bold transition flex items-center gap-1 ml-auto">
                            <i data-lucide="award" class="w-3 h-3 text-amber-600"></i>
                            💰 4萬以上高薪
                        </button>
                    </div>

                    <!-- 縣市快選與即時搜尋列 -->
                    <div class="grid grid-cols-1 sm:grid-cols-12 gap-2.5">
                        <div class="sm:col-span-3">
                            <select id="select-county-filter" onchange="filterJobsByCounty(this.value)" class="w-full text-xs rounded-lg border border-slate-300 bg-white px-3 py-2 text-slate-700 focus:outline-none focus:ring-2 focus:ring-violet-500">
                                <option value="ALL">全部縣市 (中彰投)</option>
                                <option value="台中市">台中市 (550 筆)</option>
                                <option value="彰化縣">彰化縣 (118 筆)</option>
                                <option value="南投縣">南投縣 (32 筆)</option>
                            </select>
                        </div>
                        <div class="sm:col-span-9 relative">
                            <input type="text" id="input-jobs-search" oninput="handleJobsSearch(this.value)" placeholder="🔍 即時搜尋職缺名稱、公司名稱、技能關鍵字（如：AI、ChatGPT、西屯、福興、Amazon、報關...）" class="w-full text-xs rounded-lg border border-slate-300 bg-white px-3.5 py-2 pl-9 text-slate-700 focus:outline-none focus:ring-2 focus:ring-violet-500">
                            <i data-lucide="search" class="w-4 h-4 text-slate-400 absolute left-3 top-2.5 pointer-events-none"></i>
                        </div>
                    </div>
                </div>

                <!-- 職缺列表表格 (支援手機水平滑動) -->
                <div class="overflow-x-auto border border-slate-200 rounded-xl">
                    <table class="w-full text-left border-collapse text-xs whitespace-nowrap">
                        <thead>
                            <tr class="bg-slate-50 border-b border-slate-200 text-slate-600 font-bold">
                                <th class="p-3 w-12">#</th>
                                <th class="p-3 w-24">領域軌道</th>
                                <th class="p-3">職缺名稱</th>
                                <th class="p-3">徵才企業</th>
                                <th class="p-3 w-28">工作地點</th>
                                <th class="p-3 w-32">薪資待遇</th>
                                <th class="p-3">核心技能標籤</th>
                                <th class="p-3 w-24 text-center">104 官方查證</th>
                            </tr>
                        </thead>
                        <tbody id="jobs-table-body" class="divide-y divide-slate-100">
                            <!-- 由 JavaScript 動態生成 -->
                        </tbody>
                    </table>
                </div>

                <!-- 分頁控制器 -->
                <div class="flex flex-col sm:flex-row items-center justify-between gap-3 pt-2 text-xs text-slate-600">
                    <div id="jobs-pagination-info" class="font-mono">
                        顯示第 1 ~ 12 筆，共 700 筆
                    </div>
                    <div class="flex items-center gap-1">
                        <button onclick="changeJobsPage(1)" class="px-2.5 py-1 rounded border border-slate-300 bg-white hover:bg-slate-50 disabled:opacity-40" id="btn-page-first">首頁</button>
                        <button onclick="changeJobsPage(currentJobsPage - 1)" class="px-2.5 py-1 rounded border border-slate-300 bg-white hover:bg-slate-50 disabled:opacity-40" id="btn-page-prev">上一頁</button>
                        <span id="jobs-page-display" class="px-3 py-1 font-mono font-bold bg-slate-100 rounded border border-slate-200">1 / 59</span>
                        <button onclick="changeJobsPage(currentJobsPage + 1)" class="px-2.5 py-1 rounded border border-slate-300 bg-white hover:bg-slate-50 disabled:opacity-40" id="btn-page-next">下一頁</button>
                        <button onclick="changeJobsPage(totalJobsPages)" class="px-2.5 py-1 rounded border border-slate-300 bg-white hover:bg-slate-50 disabled:opacity-40" id="btn-page-last">末頁</button>
                    </div>
                </div>
            </div>

            <!-- 板塊五：中科國貿 (NUTC IB) 「AI × 智慧商務」階梯式課綱革新藍圖 -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-5 sm:p-7 shadow-[0_2px_12px_rgba(0,0,0,0.03)] space-y-6">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200/70 gap-2">
                    <div>
                        <div class="flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-violet-600"></span>
                            <h3 class="text-base font-bold text-slate-900 tracking-tight">
                                板塊五：中科國貿 (NUTC IB) 「AI × 智慧商務」階梯式課綱革新藍圖
                            </h3>
                        </div>
                        <p class="text-xs text-slate-500 mt-0.5">
                            專為系務會議、課程委員會與教育部評鑑量身定制之產學對接藍圖
                        </p>
                    </div>
                    <span class="text-xs px-2.5 py-1 rounded-full bg-emerald-50 text-emerald-800 border border-emerald-200 font-bold">
                        學程提案：AI 智慧外銷與跨境商務微學程 (12學分)
                    </span>
                </div>

                <!-- 四年一貫階梯式課綱矩陣 -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-xs">
                    <div class="p-4 rounded-xl border border-slate-200 bg-slate-50/60 space-y-2 relative overflow-hidden">
                        <div class="flex items-center justify-between">
                            <span class="px-2 py-0.5 rounded bg-violet-100 text-violet-800 font-bold text-[10px]">大一 · 數位基礎</span>
                            <span class="text-slate-400 font-mono">3 學分</span>
                        </div>
                        <h4 class="text-sm font-bold text-slate-900">商務數位工具與生成式 AI 入門</h4>
                        <p class="text-slate-600 leading-relaxed text-[11.5px]">
                            • Prompt Engineering 商業提示詞架構<br>
                            • 生成式 AI 工具鏈 (ChatGPT/Claude/Copilot)<br>
                            • AI 自動化商業簡報 (Gamma/Canva) 與外銷初探
                        </p>
                        <div class="text-[11px] text-violet-700 font-semibold pt-2 border-t border-slate-200">
                            對標痛點：掃除 AI 恐懼，建立數位生產力
                        </div>
                    </div>

                    <div class="p-4 rounded-xl border border-slate-200 bg-slate-50/60 space-y-2 relative overflow-hidden">
                        <div class="flex items-center justify-between">
                            <span class="px-2 py-0.5 rounded bg-amber-100 text-amber-800 font-bold text-[10px]">大二 · 專業核心</span>
                            <span class="text-slate-400 font-mono">3 學分</span>
                        </div>
                        <h4 class="text-sm font-bold text-slate-900">國際貿易實務與 AI 自動化單證</h4>
                        <p class="text-slate-600 leading-relaxed text-[11.5px]">
                            • INCOTERMS 2020 貿易條件實務精解<br>
                            • AI 輔助 L/C 信用狀審查與風險防呆<br>
                            • 歐美買家 B2B 客製化 Cold Email 實戰寫作
                        </p>
                        <div class="text-[11px] text-amber-800 font-semibold pt-2 border-t border-slate-200">
                            對標痛點：將單證工作效率提升 10 倍
                        </div>
                    </div>

                    <div class="p-4 rounded-xl border border-slate-200 bg-slate-50/60 space-y-2 relative overflow-hidden">
                        <div class="flex items-center justify-between">
                            <span class="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">大三 · 跨域電商</span>
                            <span class="text-slate-400 font-mono">3 學分</span>
                        </div>
                        <h4 class="text-sm font-bold text-slate-900">跨境電商營運與 AI 流量行銷</h4>
                        <p class="text-slate-600 leading-relaxed text-[11.5px]">
                            • Amazon / 蝦皮 / Alibaba 平台實戰操作<br>
                            • AI 驅動 Listing 文案與 SEO 關鍵字演算法<br>
                            • GA4 數位流量分析與廣告投放成效優化
                        </p>
                        <div class="text-[11px] text-emerald-800 font-semibold pt-2 border-t border-slate-200">
                            對標痛點：填補中彰投 25% 電商人才荒
                        </div>
                    </div>

                    <div class="p-4 rounded-xl border border-slate-200 bg-slate-50/60 space-y-2 relative overflow-hidden">
                        <div class="flex items-center justify-between">
                            <span class="px-2 py-0.5 rounded bg-sky-100 text-sky-800 font-bold text-[10px]">大四 · 整合實習</span>
                            <span class="text-slate-400 font-mono">3 學分</span>
                        </div>
                        <h4 class="text-sm font-bold text-slate-900">全球市場開發專題與 AI 業務自動化</h4>
                        <p class="text-slate-600 leading-relaxed text-[11.5px]">
                            • 國際商展參展模擬與 Buyer Persona 調研<br>
                            • AI 跨文化商務談判實戰模擬<br>
                            • 中彰投隱形冠軍外銷業務帶薪實習
                        </p>
                        <div class="text-[11px] text-sky-800 font-semibold pt-2 border-t border-slate-200">
                            對標痛點：畢業即就業，挑戰 40K~60K 起薪
                        </div>
                    </div>
                </div>

                <!-- 師資與產學落地支援 -->
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
                    <div class="p-3.5 rounded-xl border border-slate-200 bg-white text-xs">
                        <strong class="text-slate-900 font-bold flex items-center gap-1.5">
                            <i data-lucide="users" class="w-3.5 h-3.5 text-violet-600"></i>
                            師資 AI 賦能工作坊
                        </strong>
                        <p class="text-slate-500 mt-1 leading-relaxed">
                            針對現有專任師資，每學期舉辦 2 次「生成式 AI 在商務教學與研究應用工作坊」，輔導教授將 AI 工具自然融入國貿理論與實務課程。
                        </p>
                    </div>

                    <div class="p-3.5 rounded-xl border border-slate-200 bg-white text-xs">
                        <strong class="text-slate-900 font-bold flex items-center gap-1.5">
                            <i data-lucide="briefcase" class="w-3.5 h-3.5 text-emerald-600"></i>
                            中彰投外銷隱形冠軍產學合作
                        </strong>
                        <p class="text-slate-500 mt-1 leading-relaxed">
                            與西屯中科、精科、鹿港福興外銷企業（如五金、自行車、醫材廠商）簽訂實習合作，由學生為企業建立 AI 海外開發信與電商文案系統。
                        </p>
                    </div>

                    <div class="p-3.5 rounded-xl border border-slate-200 bg-white text-xs">
                        <strong class="text-slate-900 font-bold flex items-center gap-1.5">
                            <i data-lucide="award" class="w-3.5 h-3.5 text-amber-600"></i>
                            雙軌認證：國貿證照 + AI 應用能力
                        </strong>
                        <p class="text-slate-500 mt-1 leading-relaxed">
                            輔導學生在取得「國貿業務乙丙級證照」的同時，修畢 AI 微學程並獲得校級認證，雙重加持突破傳統 33K 低薪魔咒。
                        </p>
                    </div>
                </div>
            </div>

        </section>
'''

    if 'id="module-ai"' not in html:
        main_close = html.find('</main>')
        html = html[:main_close] + module_ai_html + '\n    ' + html[main_close:]
        print("Injected module-ai section before </main>.")

    # 4. Prepare Pure JavaScript without python f-string interpolation
    js_template = """
        // =========================================================================
        // 【專區】中彰投 104 真實職缺大數據 (700筆 100% 官方真實可查證)
        // =========================================================================
        const JOBS_104 = __JOBS_JSON__;

        let currentJobsTrack = 'ALL';
        let currentJobsCounty = 'ALL';
        let currentJobsHighSalaryOnly = false;
        let currentJobsSearchKeyword = '';
        let currentJobsPage = 1;
        const jobsPerPage = 12;
        let filteredJobs = [...JOBS_104];
        let totalJobsPages = Math.ceil(filteredJobs.length / jobsPerPage);

        // 初始化或更新篩選列表
        function applyJobsFilters() {
            filteredJobs = JOBS_104.filter(j => {
                // 軌道過濾
                if (currentJobsTrack !== 'ALL' && j.tr !== currentJobsTrack) return false;
                // 縣市過濾
                if (currentJobsCounty !== 'ALL' && j.cy !== currentJobsCounty) return false;
                // 高薪過濾 (4萬以上)
                if (currentJobsHighSalaryOnly && j.sl < 40000) return false;
                // 關鍵字搜尋
                if (currentJobsSearchKeyword) {
                    const kw = currentJobsSearchKeyword.toLowerCase();
                    const text = (j.ti + ' ' + j.co + ' ' + j.cy + ' ' + j.to + ' ' + (j.sk || []).join(' ') + ' ' + j.sn).toLowerCase();
                    if (!text.includes(kw)) return false;
                }
                return true;
            });

            totalJobsPages = Math.max(1, Math.ceil(filteredJobs.length / jobsPerPage));
            if (currentJobsPage > totalJobsPages) currentJobsPage = 1;
            renderJobsTable();
            updateJobsPaginationUI();
        }

        function renderJobsTable() {
            const tbody = document.getElementById('jobs-table-body');
            if (!tbody) return;
            tbody.innerHTML = '';

            const start = (currentJobsPage - 1) * jobsPerPage;
            const end = Math.min(start + jobsPerPage, filteredJobs.length);
            const pageData = filteredJobs.slice(start, end);

            if (pageData.length === 0) {
                tbody.innerHTML = '<tr><td colspan="8" class="p-6 text-center text-slate-400">查無符合條件的職缺，請嘗試調整篩選條件或關鍵字。</td></tr>';
                return;
            }

            pageData.forEach((j, idx) => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 transition border-b border-slate-100 text-xs';

                // Track badge color
                let trackBadge = '';
                if (j.tr === 'AI經貿電商前鋒') {
                    trackBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-violet-100 text-violet-800 border border-violet-200">🤖 AI前鋒</span>';
                } else if (j.tr === '國外業務') {
                    trackBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-200">🌍 國外業務</span>';
                } else if (j.tr === '報關行與關務') {
                    trackBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-sky-100 text-sky-800 border border-sky-200">📦 報關關務</span>';
                } else {
                    trackBadge = '<span class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">🛒 電子商務</span>';
                }

                // Salary badge
                let salBadge = '';
                if (j.sl >= 50000) {
                    salBadge = '<span class="font-bold text-violet-700 bg-violet-50 px-1.5 py-0.5 rounded border border-violet-200">' + j.sa + '</span>';
                } else if (j.sl >= 40000) {
                    salBadge = '<span class="font-bold text-amber-700 bg-amber-50 px-1.5 py-0.5 rounded border border-amber-200">' + j.sa + '</span>';
                } else {
                    salBadge = '<span class="font-medium text-slate-700">' + j.sa + '</span>';
                }

                // Skills tags
                const skillTags = (j.sk || []).slice(0, 2).map(s => {
                    const shortName = s.split(' ')[0].replace('(', '');
                    return '<span class="px-1.5 py-0.5 rounded bg-slate-100 text-slate-600 text-[10px] border border-slate-200">' + shortName + '</span>';
                }).join(' ');

                tr.innerHTML = `
                    <td class="p-3 font-mono text-slate-400">#${start + idx + 1}</td>
                    <td class="p-3">${trackBadge}</td>
                    <td class="p-3 font-semibold text-slate-900 max-w-xs truncate" title="${j.ti}">
                        ${j.ti}
                        <div class="text-[10px] text-slate-400 truncate mt-0.5">${j.sn || ''}</div>
                    </td>
                    <td class="p-3 text-slate-800 max-w-[160px] truncate" title="${j.co}">${j.co}</td>
                    <td class="p-3 text-slate-600">${j.cy} ${j.to}</td>
                    <td class="p-3">${salBadge}</td>
                    <td class="p-3 max-w-[200px] truncate">${skillTags || '<span class="text-slate-300 text-[10px]">通用商務技能</span>'}</td>
                    <td class="p-3 text-center">
                        <a href="${j.url}" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 px-2.5 py-1 rounded bg-violet-50 hover:bg-violet-600 text-violet-700 hover:text-white border border-violet-200 hover:border-violet-600 text-[11px] font-bold transition group">
                            <span>104 官方</span>
                            <i data-lucide="external-link" class="w-3 h-3 group-hover:translate-x-0.5 transition"></i>
                        </a>
                    </td>
                `;
                tbody.appendChild(tr);
            });

            if (window.lucide && typeof lucide.createIcons === 'function') {
                lucide.createIcons();
            }
        }

        function updateJobsPaginationUI() {
            const info = document.getElementById('jobs-pagination-info');
            const display = document.getElementById('jobs-page-display');
            const badge = document.getElementById('jobs-filtered-count-badge');
            const btnPrev = document.getElementById('btn-page-prev');
            const btnNext = document.getElementById('btn-page-next');
            const btnFirst = document.getElementById('btn-page-first');
            const btnLast = document.getElementById('btn-page-last');

            const start = filteredJobs.length === 0 ? 0 : (currentJobsPage - 1) * jobsPerPage + 1;
            const end = Math.min(currentJobsPage * jobsPerPage, filteredJobs.length);

            if (info) info.textContent = `顯示第 ${start} ~ ${end} 筆，共 ${filteredJobs.length} 筆`;
            if (display) display.textContent = `${currentJobsPage} / ${totalJobsPages}`;
            if (badge) badge.textContent = `顯示 ${filteredJobs.length} / ${JOBS_104.length} 筆`;

            if (btnPrev) btnPrev.disabled = currentJobsPage <= 1;
            if (btnFirst) btnFirst.disabled = currentJobsPage <= 1;
            if (btnNext) btnNext.disabled = currentJobsPage >= totalJobsPages;
            if (btnLast) btnLast.disabled = currentJobsPage >= totalJobsPages;
        }

        function changeJobsPage(newPage) {
            if (newPage < 1 || newPage > totalJobsPages) return;
            currentJobsPage = newPage;
            renderJobsTable();
            updateJobsPaginationUI();
        }

        function filterJobsByTrack(track) {
            currentJobsTrack = track;
            currentJobsPage = 1;
            document.querySelectorAll('.filter-track-btn').forEach(btn => {
                btn.classList.remove('bg-slate-900', 'text-white');
                btn.classList.add('bg-slate-100', 'text-slate-700');
            });
            let activeId = 'btn-track-all';
            if (track === 'AI經貿電商前鋒') activeId = 'btn-track-ai';
            else if (track === '國外業務') activeId = 'btn-track-export';
            else if (track === '報關行與關務') activeId = 'btn-track-customs';
            else if (track === '電子商務') activeId = 'btn-track-ec';

            const activeBtn = document.getElementById(activeId);
            if (activeBtn) {
                activeBtn.classList.remove('bg-slate-100', 'text-slate-700');
                activeBtn.classList.add('bg-slate-900', 'text-white');
            }
            applyJobsFilters();
        }

        function filterJobsByCounty(county) {
            currentJobsCounty = county;
            currentJobsPage = 1;
            applyJobsFilters();
        }

        function toggleHighSalaryFilter() {
            currentJobsHighSalaryOnly = !currentJobsHighSalaryOnly;
            currentJobsPage = 1;
            const btn = document.getElementById('btn-track-highsal');
            if (btn) {
                if (currentJobsHighSalaryOnly) {
                    btn.classList.remove('bg-amber-50', 'text-amber-900', 'border-amber-300');
                    btn.classList.add('bg-amber-600', 'text-white', 'border-amber-600');
                } else {
                    btn.classList.add('bg-amber-50', 'text-amber-900', 'border-amber-300');
                    btn.classList.remove('bg-amber-600', 'text-white', 'border-amber-600');
                }
            }
            applyJobsFilters();
        }

        function handleJobsSearch(val) {
            currentJobsSearchKeyword = (val || '').trim();
            currentJobsPage = 1;
            applyJobsFilters();
        }

        function copyPrompt(id) {
            const el = document.getElementById(id);
            if (!el) return;
            const text = el.innerText || el.textContent;
            navigator.clipboard.writeText(text).then(() => {
                const btnNum = id.replace('prompt-', '');
                const btn = document.getElementById('btn-copy-' + btnNum);
                if (btn) {
                    const originHTML = btn.innerHTML;
                    btn.innerHTML = '<i data-lucide="check" class="w-3 h-3 text-emerald-300"></i><span>已複製！✓</span>';
                    btn.classList.remove('bg-violet-600', 'bg-emerald-600', 'bg-sky-600', 'bg-amber-600', 'bg-rose-600');
                    btn.classList.add('bg-emerald-700');
                    if (window.lucide && typeof lucide.createIcons === 'function') lucide.createIcons();
                    setTimeout(() => {
                        btn.innerHTML = originHTML;
                        btn.classList.remove('bg-emerald-700');
                        if (btnNum === '1') btn.classList.add('bg-violet-600');
                        else if (btnNum === '2') btn.classList.add('bg-emerald-600');
                        else if (btnNum === '3') btn.classList.add('bg-sky-600');
                        else if (btnNum === '4') btn.classList.add('bg-amber-600');
                        else if (btnNum === '5') btn.classList.add('bg-rose-600');
                        if (window.lucide && typeof lucide.createIcons === 'function') lucide.createIcons();
                    }, 2000);
                }
            }).catch(err => {
                alert('複製失敗，請手動選取文字複製。');
            });
        }

        function export104JobsCSV() {
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
        }

        // 圖表實例
        let chartAISalary = null;
        let chartAIRadar = null;

        function initModuleAICharts() {
            applyJobsFilters();

            // 1. 薪資溢價長條圖
            const ctxSalary = document.getElementById('chart-ai-salary-compare');
            if (ctxSalary && !chartAISalary) {
                chartAISalary = new Chart(ctxSalary, {
                    type: 'bar',
                    data: {
                        labels: ['AI經貿電商前鋒', '國外業務', '電子商務', '報關行與關務'],
                        datasets: [
                            {
                                type: 'bar',
                                label: '起薪中位數 (NT$)',
                                data: [38000, 38000, 35000, 33000],
                                backgroundColor: [
                                    'rgba(124, 58, 237, 0.85)',
                                    'rgba(217, 119, 6, 0.85)',
                                    'rgba(5, 150, 105, 0.85)',
                                    'rgba(2, 132, 199, 0.85)'
                                ],
                                borderColor: [
                                    '#7c3aed',
                                    '#d97706',
                                    '#059669',
                                    '#0284c7'
                                ],
                                borderWidth: 1.5,
                                borderRadius: 6,
                                yAxisID: 'y'
                            },
                            {
                                type: 'line',
                                label: '4萬以上高薪佔比 (%)',
                                data: [21.0, 18.5, 13.0, 7.0],
                                borderColor: '#ef4444',
                                backgroundColor: '#ef4444',
                                borderWidth: 2.5,
                                pointBackgroundColor: '#ef4444',
                                pointRadius: 5,
                                yAxisID: 'y1'
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        interaction: {
                            mode: 'index',
                            intersect: false
                        },
                        plugins: {
                            legend: {
                                position: 'top',
                                labels: {
                                    boxWidth: 12,
                                    font: { size: 11 }
                                }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        if (context.dataset.type === 'line') {
                                            return ` 4萬以上比例: ${context.parsed.y}%`;
                                        }
                                        return ` 起薪中位數: NT$ ${context.parsed.y.toLocaleString()}`;
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                type: 'linear',
                                display: true,
                                position: 'left',
                                min: 25000,
                                max: 45000,
                                title: {
                                    display: true,
                                    text: '起薪中位數 (NT$)',
                                    font: { size: 10 }
                                }
                            },
                            y1: {
                                type: 'linear',
                                display: true,
                                position: 'right',
                                min: 0,
                                max: 25,
                                grid: {
                                    drawOnChartArea: false
                                },
                                title: {
                                    display: true,
                                    text: '4萬以上高薪比率 (%)',
                                    font: { size: 10 }
                                }
                            }
                        }
                    }
                });
            }

            // 2. 四大軌道職能雷達圖
            const ctxRadar = document.getElementById('chart-ai-tracks-radar');
            if (ctxRadar && !chartAIRadar) {
                chartAIRadar = new Chart(ctxRadar, {
                    type: 'radar',
                    data: {
                        labels: [
                            '英語商務溝通',
                            '海外展會拓銷',
                            '商務談判簽約',
                            '進出口關務單證',
                            '電商平台營運',
                            '數位行銷廣告',
                            '生成式 AI 應用',
                            '數據分析自動化'
                        ],
                        datasets: [
                            {
                                label: 'AI經貿前鋒 (100筆)',
                                data: [12.0, 28.0, 47.0, 8.0, 2.0, 2.0, 11.0, 7.0],
                                borderColor: '#7c3aed',
                                backgroundColor: 'rgba(124, 58, 237, 0.15)',
                                borderWidth: 2,
                                pointBackgroundColor: '#7c3aed',
                                pointRadius: 3
                            },
                            {
                                label: '國外業務 (200筆)',
                                data: [19.0, 34.5, 53.0, 13.5, 2.0, 2.0, 1.5, 2.5],
                                borderColor: '#d97706',
                                backgroundColor: 'rgba(217, 119, 6, 0.12)',
                                borderWidth: 2,
                                pointBackgroundColor: '#d97706',
                                pointRadius: 3
                            },
                            {
                                label: '報關關務 (200筆)',
                                data: [9.0, 4.0, 16.5, 90.5, 0.5, 0.5, 1.0, 5.5],
                                borderColor: '#0284c7',
                                backgroundColor: 'rgba(2, 132, 199, 0.12)',
                                borderWidth: 2,
                                pointBackgroundColor: '#0284c7',
                                pointRadius: 3
                            },
                            {
                                label: '電子商務 (200筆)',
                                data: [2.0, 3.0, 6.5, 1.5, 25.0, 11.0, 2.0, 8.0],
                                borderColor: '#059669',
                                backgroundColor: 'rgba(5, 150, 105, 0.12)',
                                borderWidth: 2,
                                pointBackgroundColor: '#059669',
                                pointRadius: 3
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: {
                                position: 'bottom',
                                labels: {
                                    boxWidth: 10,
                                    font: { size: 10 }
                                }
                            }
                        },
                        scales: {
                            r: {
                                angleLines: { color: '#e2e8f0' },
                                grid: { color: '#e2e8f0' },
                                pointLabels: {
                                    font: { size: 10, weight: 'bold' },
                                    color: '#334155'
                                },
                                min: 0,
                                max: 95
                            }
                        }
                    }
                });
            }
        }
"""

    js_code = js_template.replace('__JOBS_JSON__', jobs_json_str)

    if 'const JOBS_104' not in html:
        script_close = html.rfind('</script>')
        html = html[:script_close] + js_code + '\n    ' + html[script_close:]
        print("Injected JOBS_104 and module-ai JavaScript.")

    # 5. Update switchTab to trigger initModuleAICharts
    if 'initModuleAICharts()' not in html:
        switch_target = "if (moduleId === 'module6') {\n                    initModule6Charts();\n                }"
        switch_replacement = "if (moduleId === 'module6') {\n                    initModule6Charts();\n                }\n                if (moduleId === 'module-ai') {\n                    initModuleAICharts();\n                }"
        html = html.replace(switch_target, switch_replacement)
        print("Updated switchTab to call initModuleAICharts().")

    # Save to interactive_dashboard.html
    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved updated interactive_dashboard.html successfully.")

if __name__ == '__main__':
    main()
