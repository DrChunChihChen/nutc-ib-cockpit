#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Second pass refinement:
1. Eliminate all remaining marketing buzzwords (旗盤, 護城河, 深水區, 海嘯, 保衛戰, 天敵, 掠奪).
2. Upgrade header and cards to the pure Lieflat Editorial aesthetic (report-03 / report-09).
"""

import re

def main():
    with open('interactive_dashboard.html', 'r', encoding='utf-8') as f:
        c = f.read()

    # Replacements for remaining hype words
    replacements = [
        (
            '<!-- 模組 1：北中南國立商管/國貿六強戰略旗盤 -->',
            '<!-- 模組 1：公立國貿、商務與海運物流校系橫向指標評比 -->'
        ),
        (
            '<h2 class="text-lg font-bold text-slate-900 font-serif-tc">北中南國立商管/國貿六強戰略旗盤 (Regional Radar & Benchmarking)</h2>',
            '<h2 class="text-xl sm:text-2xl font-bold text-stone-900 font-serif-tc tracking-tight">公立國貿、商務與海運物流校系橫向指標評比 (Regional Benchmarks)</h2>'
        ),
        (
            '以教育部 UDB 校務資訊與技專招聯會官方數據為底層，深度橫向對比「北商國商、中科國貿、雲科國管、高科航管、高科國企、高科供應鏈」全方位戰力指標。',
            '整合教育部校務資訊公開平台 (UDB) 與技專招聯會官方數據，橫向比較北商國商、中科國貿、雲科國管、高科航管、高科國企、高科供應鏈等 6 所公立旗艦校系之辦學與招生指標。'
        ),
        (
            '以五專部 100% 滿招與日間四技 99.06% 形成堅實護城河，分數緊咬北部北商國商與雲科國管，展現高度生源競爭力。',
            '以五專部 100% 滿招與日間四技 99.06% 展現穩健生源優勢，統測最低錄取均分緊咬北部北商國商與雲科國管，維持公立領先群競爭力。'
        ),
        (
            '<!-- 模組 4：113~128 少子化海嘯動態模擬器 -->',
            '<!-- 模組 4：少子化生源走勢與學制規模試算模型 -->'
        ),
        (
            '進修四技註冊率預估在 120~122 年跌入 35% 停招深水區。建議於 116 年前主動將進修部員額轉化為高階在職證照專班。',
            '進修四技註冊率預估在 120~122 年面臨招生轉折點，建議提早研議招生名額最適化調整，並結合實務技能強化在職進修吸引力。'
        ),
        (
            '擴大五專部護城河：中科大五專部註冊率維持 98~100%，建議向教育部申請增設「五專國際雙語商務專班」，鎖定國中前 15% 優秀生源。',
            '發揮五專部招生優勢：中科大五專部註冊率維持 98~100%，建議爭取增設「五專國際雙語商務專案」，向下扎根鏈結國中優秀生源。'
        ),
        (
            '<!-- 圖表駕駛艙 Row 1: 掠奪天敵排行 + 最終去向分布 -->',
            '<!-- 圖表區 Row 1: 主要流向校系排行與最終分發分布 -->'
        ),
        (
            '<!-- 左側 2 欄：掠奪中科國貿生源前十大天敵校系 (橫向長條圖) -->',
            '<!-- 左側 2 欄：考生重疊錄取主要流向校系排行 (橫向長條圖) -->'
        ),
        (
            '<!-- 天敵跨年度拆解明細表 (Yearly Breakdown) -->',
            '<!-- 主要流向校系跨年度拆解明細表 (Yearly Breakdown) -->'
        ),
        (
            '<!-- 圖表駕駛艙 Row 2: 中科國貿 169 位正取生去向保衛戰 + 三大天敵情報深水區 -->',
            '<!-- 圖表區 Row 2: 中科國貿 169 位正取生分發去向 + 三大主要競爭校系深入剖析 -->'
        ),
        (
            '<!-- 左側 1 欄：中科國貿 169 名正取生去向保衛戰 (長條圖) -->',
            '<!-- 左側 1 欄：中科國貿 169 名正取生分發去向分析 (長條圖) -->'
        ),
        (
            '<li><strong>模組 1（北中南六強旗盤）：</strong>北商國商、中科國貿、雲科國管、高科航管/國企/供應鏈，橫向對比 12 項官方硬指標，揭示中科規模第一但退學率居冠之體質特徵。</li>',
            '<li><strong>模組 1（公立校系橫向評比）：</strong>北商國商、中科國貿、雲科國管、高科航管/國企/供應鏈，橫向對比 12 項官方指標，分析中科在學規模、註冊率與休退學結構。</li>'
        ),
        (
            '與 80人退學深水區。',
            '與 80 人在學退學原因結構。'
        ),
        (
            '"english_title": "NUTC ITM Executive Strategic Intelligence Cockpit"',
            '"english_title": "NUTC ITM Academic Intelligence & Admissions Analysis Report"'
        ),
        (
            '`資金護城河: ${raw.reserve}`',
            '`學校現金存量: ${raw.reserve}`'
        )
    ]

    for old, new in replacements:
        if old in c:
            c = c.replace(old, new)
        else:
            print(f"Refine notice: not matched '{old[:40]}...'")

    # Header logo upgrade to Lieflat editorial stamp
    old_logo = '''                    <div class="w-12 h-12 rounded-xl bg-gradient-to-tr from-emerald-600 to-teal-400 flex items-center justify-center shadow-lg shadow-emerald-500/20 text-white font-bold text-xl">
                        NUTC
                    </div>'''
    new_logo = '''                    <div class="w-12 h-12 rounded-sm bg-[#18181b] border border-stone-800 flex items-center justify-center shadow-sm text-white font-serif-tc font-bold text-lg relative overflow-hidden">
                        <span class="relative z-10 tracking-tight">ITM</span>
                        <div class="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-[#f05138]"></div>
                    </div>'''
    if old_logo in c:
        c = c.replace(old_logo, new_logo)

    # Header badge upgrade
    old_badge = '<span class="bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs px-2.5 py-0.5 rounded-full border border-emerald-500/30 font-semibold">114 學年度最新校務實證</span>'
    new_badge = '<span class="bg-stone-100 text-stone-800 border border-stone-300 text-xs font-mono px-2.5 py-0.5 rounded-sm font-semibold">114 學年度校務實證</span>'
    if old_badge in c:
        c = c.replace(old_badge, new_badge)

    with open('interactive_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(c)
    print("Refinement completed successfully!")

if __name__ == '__main__':
    main()
