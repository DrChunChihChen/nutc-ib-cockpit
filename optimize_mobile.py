#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Mobile Responsiveness Optimization for interactive_dashboard.html:
1. Prevent page-level horizontal overflow (overflow-x-hidden, responsive paddings).
2. Refactor Header & Navigation: flexible wrap on mobile, hide unnecessary elements, horizontal touch scroll on tabs.
3. Top Ribbon responsive typography and wrap.
4. Top 6 KPI cards responsive sizing (p-3 sm:p-4, text-lg sm:text-xl).
5. Add touch-scroll and min-width to all wide data tables with mobile swipe indicators.
6. Responsive chart container heights (min-h-[260px] sm:min-h-[340px]).
"""

import re

def main():
    with open('interactive_dashboard.html', 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Custom CSS additions in <head> for mobile scrolling
    mobile_css = '''
        /* 手機版橫向滑動與隱藏滾動條 */
        .no-scrollbar::-webkit-scrollbar {
            display: none;
        }
        .no-scrollbar {
            -ms-overflow-style: none;
            scrollbar-width: none;
        }
        .touch-scroll {
            -webkit-overflow-scrolling: touch;
        }
        /* 防止手機端整體頁面橫向爆版 */
        html, body {
            max-width: 100vw;
            overflow-x: hidden;
        }
'''
    if '.touch-scroll' not in c:
        c = c.replace('/* 經典出版品雙細線 */', mobile_css + '\n        /* 經典出版品雙細線 */')

    # 2. Refactor Top Ribbon for mobile
    old_ribbon = '''    <!-- 頂部學術出版與校務實證標註 Ribbon (Lieflat Editorial Standard) -->
    <div class="bg-[#18181b] text-[#fafaf7] px-4 py-2 border-b border-stone-800 text-[11px] font-mono tracking-widest uppercase no-print">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-1">
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-[#f05138]"></span>
                <span class="font-bold">NUTC IB · 國立臺中科技大學 國際貿易與經營系 (Department of International Business)</span>
                <span class="text-stone-500">|</span>
                <span class="text-stone-300 font-sans">校務分析與生源實證評估報告 (114學年度)</span>
            </div>
            <div class="text-stone-400">
                教育部大專校院校務資訊公開平台 (UDB) · 技專招聯會官方實證數據
            </div>
        </div>
    </div>'''

    new_ribbon = '''    <!-- 頂部學術出版與校務實證標註 Ribbon (Lieflat Editorial Standard) -->
    <div class="bg-[#18181b] text-[#fafaf7] px-3 sm:px-4 py-2 border-b border-stone-800 text-[10px] sm:text-[11px] font-mono tracking-wider sm:tracking-widest uppercase no-print">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-start sm:items-center justify-between gap-1.5">
            <div class="flex flex-wrap items-center gap-1.5 sm:gap-2">
                <span class="w-2 h-2 rounded-full bg-[#f05138] flex-shrink-0"></span>
                <span class="font-bold">NUTC IB · 國立臺中科技大學 國際貿易與經營系</span>
                <span class="text-stone-500 hidden sm:inline">|</span>
                <span class="text-stone-300 font-sans text-[10px] sm:text-[11px]">校務分析與生源實證評估報告 (114學年度)</span>
            </div>
            <div class="text-stone-400 text-[10px] sm:text-[11px]">
                教育部大專校院校務資訊公開平台 (UDB) · 技專招聯會官方實證數據
            </div>
        </div>
    </div>'''

    if old_ribbon in c:
        c = c.replace(old_ribbon, new_ribbon)
        print("Updated top ribbon for mobile!")
    else:
        print("Note: old_ribbon not matched exactly")

    # 3. Refactor Header for mobile (flexible wrap, avoid fixed h-20 blowing out)
    old_header_content = '''        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-20">
                <!-- 標題與所屬單位 -->
                <div class="flex items-center space-x-4">
                    <div class="w-12 h-12 rounded-sm bg-[#18181b] border border-stone-800 flex items-center justify-center shadow-sm text-white font-serif-tc font-bold text-lg relative overflow-hidden">
                        <span class="relative z-10 tracking-tight">IB</span>
                        <div class="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-[#f05138]"></div>
                    </div>
                    <div>
                        <div class="flex items-center space-x-2">
                            <h1 class="text-xl font-extrabold tracking-tight text-slate-900 flex items-center gap-2 font-serif-tc">
                                國立臺中科技大學 國際貿易與經營系
                                <span class="bg-stone-100 text-stone-800 border border-stone-300 text-xs font-mono px-2.5 py-0.5 rounded-sm font-semibold">114 學年度校務實證</span>
                            </h1>
                        </div>
                        <p class="text-xs text-slate-600 font-medium tracking-wide mt-0.5 flex flex-wrap items-center gap-2">
                            <span class="font-mono text-stone-500 font-semibold">Department of International Business (IB)</span>
                            <span class="text-slate-300">|</span>
                            <span>系務發展分析與生源趨勢評估報告</span>
                            <span class="text-slate-400">|</span>
                            <span>UDB 教育部公開平台與技專招聯會交叉查榜數據</span>
                        </p>
                    </div>
                </div>

                <!-- 頂部功能區 -->
                <div class="flex items-center space-x-3 no-print">
                    <button onclick="openSpecModal()" class="px-3 py-1.5 rounded-sm bg-[#fafaf7] hover:bg-stone-100 text-stone-700 border border-stone-300 shadow-sm text-xs font-medium flex items-center gap-1.5 transition">
                        <i data-lucide="file-text" class="w-4 h-4 text-stone-600"></i>
                        <span>研究架構與規格</span>
                    </button>
                    <button onclick="window.print()" class="px-3 py-1.5 rounded-sm bg-[#fafaf7] hover:bg-stone-100 text-stone-700 border border-stone-300 shadow-sm text-xs font-medium flex items-center gap-1.5 transition">
                        <i data-lucide="printer" class="w-4 h-4 text-stone-600"></i>
                        <span>列印/匯出PDF</span>
                    </button>
                    <button onclick="exportAllCSV()" class="px-3.5 py-1.5 rounded-sm bg-[#f05138] hover:bg-[#e04830] text-white text-xs font-bold flex items-center gap-1.5 shadow-sm transition">
                        <i data-lucide="download" class="w-4 h-4"></i>
                        <span>下載實證數據集 (CSV)</span>
                    </button>
                </div>
            </div>

            <!-- 5 大核心功能模組導航切換 Tabs -->
            <div class="flex space-x-1 border-t border-stone-200 pt-1 overflow-x-auto no-print">'''

    new_header_content = '''        <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
            <div class="flex flex-col md:flex-row md:items-center justify-between py-2.5 md:py-0 md:h-20 gap-2 md:gap-4">
                <!-- 標題與所屬單位 -->
                <div class="flex items-center space-x-3 sm:space-x-4">
                    <div class="w-10 h-10 sm:w-12 sm:h-12 flex-shrink-0 rounded-sm bg-[#18181b] border border-stone-800 flex items-center justify-center shadow-sm text-white font-serif-tc font-bold text-base sm:text-lg relative overflow-hidden">
                        <span class="relative z-10 tracking-tight">IB</span>
                        <div class="absolute top-1 right-1 sm:top-1.5 sm:right-1.5 w-1.5 h-1.5 rounded-full bg-[#f05138]"></div>
                    </div>
                    <div class="min-w-0">
                        <div class="flex flex-wrap items-center gap-1.5 sm:gap-2">
                            <h1 class="text-base sm:text-xl font-extrabold tracking-tight text-slate-900 flex items-center gap-1.5 sm:gap-2 font-serif-tc">
                                <span>國立臺中科技大學 國際貿易與經營系</span>
                            </h1>
                            <span class="bg-stone-100 text-stone-800 border border-stone-300 text-[10px] sm:text-xs font-mono px-2 py-0.5 rounded-sm font-semibold whitespace-nowrap">114 學年實證</span>
                        </div>
                        <p class="text-[10px] sm:text-xs text-slate-600 font-medium tracking-wide mt-0.5 flex flex-wrap items-center gap-1.5 sm:gap-2">
                            <span class="font-mono text-stone-500 font-semibold">Department of International Business (IB)</span>
                            <span class="text-slate-300 hidden sm:inline">|</span>
                            <span class="hidden md:inline">系務發展分析與生源趨勢評估報告</span>
                        </p>
                    </div>
                </div>

                <!-- 頂部功能區 (手機版橫向緊湊排列) -->
                <div class="flex items-center space-x-2 overflow-x-auto no-scrollbar py-0.5 self-end md:self-center no-print">
                    <button onclick="openSpecModal()" class="px-2.5 py-1 sm:px-3 sm:py-1.5 rounded-sm bg-[#fafaf7] hover:bg-stone-100 text-stone-700 border border-stone-300 shadow-sm text-[11px] sm:text-xs font-medium flex items-center gap-1 whitespace-nowrap transition">
                        <i data-lucide="file-text" class="w-3.5 h-3.5 text-stone-600"></i>
                        <span>研究規格</span>
                    </button>
                    <button onclick="window.print()" class="hidden sm:flex px-3 py-1.5 rounded-sm bg-[#fafaf7] hover:bg-stone-100 text-stone-700 border border-stone-300 shadow-sm text-xs font-medium items-center gap-1.5 whitespace-nowrap transition">
                        <i data-lucide="printer" class="w-4 h-4 text-stone-600"></i>
                        <span>列印/PDF</span>
                    </button>
                    <button onclick="exportAllCSV()" class="px-2.5 py-1 sm:px-3.5 sm:py-1.5 rounded-sm bg-[#f05138] hover:bg-[#e04830] text-white text-[11px] sm:text-xs font-bold flex items-center gap-1 whitespace-nowrap shadow-sm transition">
                        <i data-lucide="download" class="w-3.5 h-3.5"></i>
                        <span>匯出全量 CSV</span>
                    </button>
                </div>
            </div>

            <!-- 5 大核心功能模組導航切換 Tabs (支援手機平滑觸控滑動) -->
            <div class="flex space-x-1 border-t border-stone-200 pt-1 overflow-x-auto touch-scroll no-scrollbar no-print">'''

    if old_header_content in c:
        c = c.replace(old_header_content, new_header_content)
        print("Updated header for mobile responsiveness!")
    else:
        print("Note: old_header_content not matched exactly")

    # 4. Update Tab buttons padding on mobile
    c = c.replace(
        'class="tab-btn px-4 py-3 text-xs sm:text-sm',
        'class="tab-btn px-3 py-2.5 sm:px-4 sm:py-3 text-xs sm:text-sm'
    )

    # 5. Update KPI Cards grid and padding for mobile
    c = c.replace(
        '<section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6 pb-2">',
        '<section class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 pt-4 sm:pt-6 pb-2">'
    )
    c = c.replace(
        '<div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">',
        '<div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-2.5 sm:gap-3">'
    )
    c = c.replace(
        'class="bg-white border border-slate-200/90 rounded-xl p-4 shadow-[0_2px_10px_rgba(0,0,0,0.03)]',
        'class="bg-white border border-slate-200/90 rounded-xl p-3 sm:p-4 shadow-[0_2px_10px_rgba(0,0,0,0.03)]'
    )

    # 6. Module 1 Table mobile improvements
    old_m1_table = '''                <!-- 戰略六強橫向真實數據比對表 -->
                <div class="overflow-x-auto mt-4 rounded-xl border border-slate-200">
                    <table class="w-full text-left text-xs border-collapse">'''

    new_m1_table = '''                <!-- 戰略六強橫向真實數據比對表 -->
                <div class="text-[11px] text-stone-500 font-mono flex items-center gap-1 lg:hidden mt-3 mb-1"><i data-lucide="chevrons-right" class="w-3.5 h-3.5 text-[#f05138]"></i> 可向右滑動查看 12 項完整官方指標</div>
                <div class="overflow-x-auto touch-scroll mt-1 rounded-xl border border-slate-200">
                    <table class="w-full min-w-[780px] text-left text-xs border-collapse">'''

    if old_m1_table in c:
        c = c.replace(old_m1_table, new_m1_table)
        print("Updated Module 1 table for mobile scroll!")
    else:
        print("Note: old_m1_table not matched")

    # 7. Module 3 Score trend chart responsive min-height
    c = c.replace(
        '<div class="relative min-h-[380px]">',
        '<div class="relative min-h-[280px] sm:min-h-[380px]">'
    )

    # 8. Module 4 Simulation table mobile swipe notice and min-width
    old_m4_table = '<div class="overflow-x-auto mt-4 rounded-xl border border-slate-200">\n                        <table class="w-full text-left text-xs border-collapse">'
    new_m4_table = '<div class="text-[11px] text-stone-500 font-mono flex items-center gap-1 lg:hidden mt-3 mb-1"><i data-lucide="chevrons-right" class="w-3.5 h-3.5 text-[#f05138]"></i> 可向右滑動查看 15 年推估數據</div>\n                    <div class="overflow-x-auto touch-scroll mt-1 rounded-xl border border-slate-200">\n                        <table class="w-full min-w-[650px] text-left text-xs border-collapse">'
    if old_m4_table in c:
        c = c.replace(old_m4_table, new_m4_table)
        print("Updated Module 4 simulation table for mobile!")

    # 9. Module 5 (504 candidates) tables mobile swipe notice and min-width
    old_cand_table = '<div class="overflow-x-auto">\n                    <table class="w-full text-left border-collapse">'
    new_cand_table = '<div class="text-[11px] text-stone-500 font-mono flex items-center gap-1 lg:hidden mb-1"><i data-lucide="chevrons-right" class="w-3.5 h-3.5 text-[#f05138]"></i> 可左右滑動查看考生志願與分發結果</div>\n                <div class="overflow-x-auto touch-scroll">\n                    <table class="w-full min-w-[560px] text-left border-collapse">'
    if old_cand_table in c:
        c = c.replace(old_cand_table, new_cand_table)
        print("Updated Candidate table for mobile!")

    # 10. Main container padding
    c = c.replace(
        '<main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">',
        '<main class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 py-3 sm:py-4">'
    )

    with open('interactive_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(c)

    print("Mobile optimizations applied to interactive_dashboard.html successfully!")

if __name__ == '__main__':
    main()
