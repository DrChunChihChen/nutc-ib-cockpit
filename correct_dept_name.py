#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Correct Department English Name and Acronym:
From ITM to Department of International Business (IB).
"""

def update_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        c = f.read()

    # Logo stamp
    c = c.replace(
        '<span class="relative z-10 tracking-tight">ITM</span>',
        '<span class="relative z-10 tracking-tight">IB</span>'
    )

    # Top ribbon
    c = c.replace(
        'NUTC ITM · 國立臺中科技大學 國際貿易與經營系',
        'NUTC IB · 國立臺中科技大學 國際貿易與經營系 (Department of International Business)'
    )

    # Header subtitle
    c = c.replace(
        '<p class="text-xs text-slate-600 font-medium tracking-wide mt-0.5 flex items-center gap-2">\n                            <span>系務發展分析與生源趨勢評估報告</span>',
        '<p class="text-xs text-slate-600 font-medium tracking-wide mt-0.5 flex flex-wrap items-center gap-2">\n                            <span class="font-mono text-stone-500 font-semibold">Department of International Business (IB)</span>\n                            <span class="text-slate-300">|</span>\n                            <span>系務發展分析與生源趨勢評估報告</span>'
    )

    # Module 3 comment
    c = c.replace('ITM Cohort Structure & Retention', 'IB Cohort Structure & Retention')

    # Footer
    c = c.replace('NUTC ITM', 'NUTC IB')
    c = c.replace('NUTC ITM Strategy Group', 'NUTC Department of International Business (IB)')

    # JSON DB english_title
    c = c.replace(
        '"english_title": "NUTC ITM Academic Intelligence & Admissions Analysis Report"',
        '"english_title": "NUTC Department of International Business (IB) Academic Intelligence & Admissions Analysis Report"'
    )

    # CSV headers and download filenames
    c = c.replace('NUTC_ITM_Cross_Admission_Poaching_113_115_Full_504.csv', 'NUTC_IB_Cross_Admission_113_115_Full_504.csv')
    c = c.replace('NUTC_ITM_Comprehensive_Master_Dataset_114.csv', 'NUTC_IB_Comprehensive_Master_Dataset_114.csv')
    c = c.replace('NUTC_ITM_Simulated_Projection_113_128', 'NUTC_IB_Simulated_Projection_113_128')

    with open(filename, 'w', encoding='utf-8') as f:
        f.write(c)
    print(f"Updated {filename}")

if __name__ == '__main__':
    for fn in ['interactive_dashboard.html', 'preview_lieflat_editorial.html']:
        update_file(fn)
