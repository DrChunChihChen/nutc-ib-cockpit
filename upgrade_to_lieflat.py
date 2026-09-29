#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Upgrade interactive_dashboard.html to the Lieflat Editorial System (report-03 & report-09 aesthetic)
and purge all marketing hype/slogans into rigorous Institutional Research (IR) scholarly language.
"""

import re
import sys

def main():
    with open('interactive_dashboard.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Update fonts and styles in <head>
    font_link = '''    <!-- Google Fonts: Noto Serif TC, Noto Sans TC, Space Grotesk, JetBrains Mono -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@400;500;700;900&family=Noto+Serif+TC:wght@500;700;900&family=Space+Grotesk:wght@500;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">'''

    custom_css = '''        body {
            font-family: 'Noto Sans TC', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: #fafaf7;
            color: #1c1917;
        }
        .font-serif-tc {
            font-family: 'Noto Serif TC', Georgia, serif;
        }
        .font-mono-num {
            font-family: 'Space Grotesk', 'JetBrains Mono', monospace;
        }
        /* 經典出版品雙細線 */
        .double-border-b {
            border-bottom: 4px double #d6d3d1;
        }
        .double-border-t {
            border-top: 4px double #d6d3d1;
        }
        .double-border-r {
            border-right: 4px double #d6d3d1;
        }
        /* 點狀引線 Dot Leaders */
        .dot-leader {
            flex-grow: 1;
            border-bottom: 1px dotted #a8a29e;
            margin: 0 8px;
            position: relative;
            top: -4px;
        }
        .custom-scrollbar::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        @media print {
            .no-print { display: none !important; }
            .page-break { page-break-before: always; }
            body { background: white !important; color: black !important; }
        }'''

    # Replace fonts and style block
    content = re.sub(
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com".*?</style>',
        font_link + '\n    <style>\n' + custom_css + '\n    </style>',
        content,
        flags=re.DOTALL
    )
    if 'font-serif-tc' not in content:
        # Fallback if the regex didn't match the Google fonts block
        content = re.sub(
            r'<style>.*?</style>',
            font_link + '\n    <style>\n' + custom_css + '\n    </style>',
            content,
            flags=re.DOTALL
        )

    # 2. Update <body> tag
    content = re.sub(
        r'<body class="[^"]*">',
        r'<body class="bg-[#fafaf7] text-stone-900 min-h-screen custom-scrollbar antialiased selection:bg-[#f05138] selection:text-white">',
        content
    )

    # 3. Add top publication ribbon right after <body>
    top_ribbon = '''    <!-- 頂部學術出版與校務實證標註 Ribbon (Lieflat Editorial Standard) -->
    <div class="bg-[#18181b] text-[#fafaf7] px-4 py-2 border-b border-stone-800 text-[11px] font-mono tracking-widest uppercase no-print">
        <div class="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-1">
            <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-[#f05138]"></span>
                <span class="font-bold">NUTC ITM · 國立臺中科技大學 國際貿易與經營系</span>
                <span class="text-stone-500">|</span>
                <span class="text-stone-300 font-sans">校務分析與生源實證評估報告 (114學年度)</span>
            </div>
            <div class="text-stone-400">
                教育部大專校院校務資訊公開平台 (UDB) · 技專招聯會官方實證數據
            </div>
        </div>
    </div>\n'''

    # If ribbon is not already present, insert it before <header>
    if 'NUTC ITM · 國立臺中科技大學 國際貿易與經營系' not in content[:2500]:
        content = re.sub(
            r'(<header class="sticky top-0 z-50 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-\[0_1px_3px_rgba\(0,0,0,0\.03\)\]">)',
            top_ribbon + r'\1',
            content
        )

    # 4. Text & Vocabulary Replacements (Purge marketing hype, replace with IR precision)
    replacements = [
        # Title & Subtitles
        (
            '國立臺中科技大學 國際貿易與經營系 | 系務策略發展與生源海嘯動態決策戰情室',
            '國立臺中科技大學 國際貿易與經營系 · 系務分析與生源實證評估報告'
        ),
        (
            '114 最新決策戰情室',
            '114 學年度最新校務實證'
        ),
        (
            '<span>系務策略發展與生源海嘯動態決策戰情室</span>',
            '<span>系務發展分析與生源趨勢評估報告</span>'
        ),
        (
            'UDB & 技專招聯會官方實證硬數據連線',
            'UDB 教育部公開平台與技專招聯會交叉查榜數據'
        ),

        # Tabs
        (
            '<span>模組 1：北中南國立商管六強旗盤</span>',
            '<span>模組 1：公立國貿商務校系橫向指標評比</span>'
        ),
        (
            '<span>模組 2：中部大專商管大亂鬥</span>',
            '<span>模組 2：中部公私立商管校系競合分析</span>'
        ),
        (
            '<span>模組 3：國貿系所體質與深水區診斷</span>',
            '<span>模組 3：中科國貿學制結構與留存體質剖析</span>'
        ),
        (
            '<span>模組 4：113~128 少子化海嘯動態模擬器</span>',
            '<span>模組 4：少子化生源走勢與學制規模試算</span>'
        ),
        (
            '<span>模組 5：師資換血與五年轉型決策</span>',
            '<span>模組 5：專任師資結構演變與中長期規劃</span>'
        ),
        (
            '<span>模組 6：甄選生源流向與天敵情報</span>',
            '<span>模組 6：四技甄選交叉查榜與重疊錄取流向</span>'
        ),

        # Module 1 Headings
        (
            '全台國立商管/國貿六強戰略旗盤 (Regional Radar & Benchmarking)',
            '公立國貿、商務與海運物流校系橫向指標評比 (Regional Benchmarks)'
        ),

        # Module 2 Headings & Text
        (
            '中部大專商管大亂鬥 (Central Taiwan Competitive Landscape)',
            '中部區域公私立國貿商管校系競合分析 (Central Taiwan Regional Analysis)'
        ),
        (
            '中部大專國貿/商務大對決 (中科國貿 vs 逢甲國貿 vs 東海國貿 vs 嶺東/朝陽國企)',
            '中部大專國貿商管校系橫向競合 (中科國貿 vs 逢甲國貿 vs 東海國貿 vs 朝陽/嶺東)'
        ),
        (
            '主動壯士斷腕砍掉3成名額，註冊率立即由谷底強彈至 96.8%，搭配博雅書院與海外雙聯，成功築起精緻化護城河。',
            '主動縮減 30% 招生名額，註冊率立即回升至 96.8%，搭配博雅書院與海外雙聯學位，成功穩固精緻化辦學定位。'
        ),
        (
            '財務護城河 vs 招生生源健康度矩陣',
            '校系財務存量與註冊率分布矩陣'
        ),
        (
            '超高資金存量・但生源面臨斷崖雪崩',
            '資金存量充裕・但進修部與日間部面臨招生逆風'
        ),
        (
            '深水警戒區 (核定已砍25)',
            '重點觀察學制 (核定調減25名)'
        ),

        # Module 3 Headings & Text
        (
            '中科國貿系所體質與學制深水區診斷 (ITM Health & Retention)',
            '中科國貿各學制結構與在學生留存分析 (ITM Cohort Structure & Retention)'
        ),
        (
            '中科國貿學制結構與留存體質深水區診斷',
            '中科國貿各學制規模與在學生留存分析'
        ),
        (
            '國貿系退學與休學深水區解剖',
            '國貿系退學與休學原因結構剖析'
        ),
        (
            '113學年度 國貿系退學與休學深水區剖析',
            '113學年度 國貿系退學與休學原因分布剖析'
        ),
        (
            '在少子化浪潮下進修部生源首當其衝。',
            '進修部生源受少子化與就業市場變化影響較深，需持續優化課程吸引在職進修。'
        ),

        # Module 4 Headings & Text
        (
            '113~128 少子化海嘯動態模擬器 (Dynamic Fertility & Policy Simulator)',
            '少子化生源走勢與學制規模試算模型 (Demographic Projection & Simulation)'
        ),
        (
            '1.25x 嚴峻海嘯',
            '高遞減衝擊情境'
        ),
        (
            '虎年海嘯波谷 (谷底年份)',
            '117 虎年世代入學谷底'
        ),
        (
            '進修四技註冊率預估在 120~122 年跌入 35% 停招深水區。建議於 116 年前主動調減名額並轉型為高階在職證照專班。',
            '進修四技註冊率預估在 120~122 年面臨轉折點，建議提早研議招生名額最適化調整並強化在職實用模組。'
        ),
        (
            '擴大五專部護城河：中科大五專部防護力維持 98~100%，建議向教育部申請增設「五專國際雙語商務專班」，鎖定國中直升高素質生源。',
            '發揮五專部招生優勢：中科大五專部註冊率維持 98~100%，建議爭取增設「五專國際雙語商務專案」，向下扎根培育經貿基層人才。'
        ),

        # Module 5 Headings & Text
        (
            '師資換血與五年轉型決策戰情室 (Faculty & Strategic Transformation)',
            '專任師資結構演變與中長期課程發展規劃 (Faculty Succession & Planning)'
        ),
        (
            '師資換血與五年轉型決策戰情室',
            '專任師資結構演變與系所發展規劃'
        ),
        (
            '完成 5 年期 8 名師資全面年輕化換血',
            '完成 5 年期 8 名專任師資世代傳承與領域優化'
        ),
        (
            '挽救大一休退學率，打造就業護城河',
            '提升大一適應與留存率，強化就業實務競爭力'
        ),

        # Module 6 Headings & Text
        (
            '四技甄選交叉查榜與生源掠奪大數據 (Module 6)',
            '四技甄選交叉查榜與重疊錄取流向分析 (Module 6)'
        ),
        (
            '四技甄選交叉查榜與生源掠奪大數據',
            '四技甄選交叉查榜與重疊錄取流向分析'
        ),
        (
            '打破錄取分數迷思，直擊考生真實志願選擇心理：掌握中科國貿 113~115 三學年度共 504 位正備取考生的微觀分發去向（113年163人、114年172人、115年169人），精準診斷生源究竟被「高科大、逢甲大學、北商大」挖走幾名學生（含三年累計與單年拆解），以及 169 位正取生保衛戰中高達 58.0% (98人) 的拔尖留任實力。',
            '基於技專校院招生聯合會官方交叉查榜數據，掌握中科國貿 113~115 三學年度共 504 位正備取考生的微觀分發去向（113年163人、114年172人、115年169人），系統化分析生源錄取分發至「高科大、逢甲大學、北商大」等校之分布情況（含三年累計與單年拆解），以及 169 位正取生中高達 58.0% (98人) 的報到分發留任情形。'
        ),
        (
            '<span class="text-xs text-slate-400 font-medium">第一大外部掠奪黑洞</span>',
            '<span class="text-xs text-stone-500 font-semibold">外部錄取分發首位 (累計120人)</span>'
        ),
        (
            '<span class="text-xs text-slate-400 font-medium">正取生留任保衛戰</span>',
            '<span class="text-xs text-stone-500 font-semibold">正取生分發留任率</span>'
        ),
        (
            '掠奪中科國貿生源之「前十大天敵校系」排行榜 (3年累計)',
            '考生重疊錄取之「主要流向校系」排行 (113~115學年 3年累計 504 筆)'
        ),
        (
            '前十大天敵跨年度 (113~115) 逐年拆解與錄取身分剖析',
            '主要流向校系跨年度逐年拆解與錄取身分分析'
        ),
        (
            '<th class="p-2">天敵校系全名</th>',
            '<th class="p-2">競爭校系名稱</th>'
        ),
        (
            '169 位【正取生】最終去向與保衛戰',
            '169 位【正取生】最終分發去向與留任分析'
        ),
        (
            '三大天敵戰略情報剖析',
            '三大主要流失校系交叉分析'
        ),
        (
            "label: function(ctx) { return ' 遭掠奪: ' + ctx.raw + ' 名學生'; }",
            "label: function(ctx) { return ' 分發錄取: ' + ctx.raw + ' 名學生'; }"
        ),
        (
            '中科大五專部防護力維持 98~100%',
            '中科大五專部註冊率維持 98~100%'
        ),
        (
            '國中直升一中商圈名校，品牌護城河極深',
            '國中直升一中商圈名校，生源穩健優勢顯著'
        ),
        (
            "'# 國立臺中科技大學 國際貿易與經營系 113~128學年度少子化海嘯動態推估試算表'",
            "'# 國立臺中科技大學 國際貿易與經營系 113~128學年度少子化趨勢試算表'"
        ),
        (
            '"subtitle": "系務策略發展與生源海嘯動態決策戰情室"',
            '"subtitle": "系務分析與生源實證評估報告"'
        ),
        (
            '中科大國貿系「少子化海嘯」系務策略發展與動態決策戰情室',
            '中科大國貿系校務分析與生源趨勢評估報告'
        ),
        (
            '掌握退學流失深水區原因',
            '掌握退學與休學主要成因'
        ),
        (
            '模組 3（國貿系所體質診斷）：',
            '模組 3（國貿系所學制與留存分析）：'
        ),
        (
            '模組 4（少子化海嘯動態模擬器）：',
            '模組 4（少子化生源走勢模擬）：'
        ),
        (
            '模組 5（師資換血與五年轉型）：',
            '模組 5（專任師資結構與世代傳承）：'
        )
    ]

    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
        else:
            print(f"Notice: Old phrase not found: '{old[:40]}...'")

    # 5. Update Headings font class to font-serif-tc
    # Let's add font-serif-tc to major h1, h2, h3 in sections
    content = re.sub(r'(<h1 class="[^"]*)(")', r'\1 font-serif-tc\2', content)
    content = re.sub(r'(<h2 class="[^"]*)(")', r'\1 font-serif-tc\2', content)

    # 6. Update Active Tab class
    content = content.replace(
        'border-b-2 border-emerald-600 text-emerald-700 font-bold',
        'border-b-2 border-[#f05138] text-[#f05138] font-bold'
    )
    content = content.replace(
        'border-emerald-600 text-emerald-700',
        'border-[#f05138] text-[#f05138]'
    )

    # 7. Update JS switchTab active tab styling
    content = content.replace(
        "btn.classList.add('border-emerald-600', 'text-emerald-700', 'font-bold');",
        "btn.classList.add('border-[#f05138]', 'text-[#f05138]', 'font-bold');"
    )
    content = content.replace(
        "btn.classList.remove('border-emerald-600', 'text-emerald-700', 'font-bold');",
        "btn.classList.remove('border-[#f05138]', 'text-[#f05138]', 'font-bold');"
    )

    # Save to interactive_dashboard.html
    with open('interactive_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully updated interactive_dashboard.html!")

if __name__ == '__main__':
    main()
