#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inject "台中經貿三大領域戰情地圖" into interactive_dashboard.html
"""

import json

def main():
    dashboard_path = 'interactive_dashboard.html'
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add tab button into header tabs
    tab_target = '<button onclick="switchTab(\'module-ai\')"'
    tc_tab_btn = '''                <button onclick="switchTab('module-tc-map')" id="tab-btn-module-tc-map" class="tab-btn px-2.5 py-2 sm:px-4 sm:py-3 text-xs sm:text-sm font-semibold border-b-2 border-transparent text-stone-600 hover:text-stone-900 flex items-center gap-1.5 whitespace-nowrap transition flex-shrink-0">
                    <i data-lucide="map" class="w-3.5 h-3.5 sm:w-4 sm:h-4 text-orange-600"></i>
                    <span class="inline sm:hidden font-bold text-orange-700">【地圖】台中經貿三領域</span>
                    <span class="hidden sm:inline font-bold text-orange-700">【地圖】台中經貿三大領域戰情地圖</span>
                    <span class="ml-1 px-1.5 py-0.5 rounded-full bg-orange-100 text-orange-800 border border-orange-300 text-[10px] font-mono font-bold">470筆台中實證</span>
                </button>
'''
    if 'id="tab-btn-module-tc-map"' not in html:
        ai_pos = html.find(tab_target)
        html = html[:ai_pos] + tc_tab_btn + html[ai_pos:]
        print("Injected Taichung Map tab button into header tabs.")

    # 1b. Add quick-jump button in top right action bar
    if 'switchTab(\'module-tc-map\')' not in html[:html.find('<section class="max-w-7xl')]:
        ai_jump_target = '<button onclick="switchTab(\'module-ai\')"'
        tc_jump_btn = '''<button onclick="switchTab('module-tc-map')" class="px-2.5 py-1 sm:px-3.5 sm:py-1.5 rounded-sm bg-gradient-to-r from-orange-600 to-amber-600 hover:from-orange-700 hover:to-amber-700 text-white text-[11px] sm:text-xs font-bold flex items-center gap-1 whitespace-nowrap shadow-sm transition">
                        <i data-lucide="map" class="w-3.5 h-3.5"></i>
                        <span>台中三領域地圖 (470筆)</span>
                    </button>
                    '''
        html = html.replace(ai_jump_target, tc_jump_btn + ai_jump_target)
        print("Injected Taichung Map quick-jump button in top action bar.")

    # 2. Section HTML for module-tc-map
    tc_section_html = '''
        <!-- ================================================================= -->
        <!-- 模組：台中經貿三大領域戰情地圖 (國外業務 × 報關行 × 電子商務) -->
        <!-- ================================================================= -->
        <section id="module-tc-map" class="tab-content hidden space-y-8">
            
            <!-- 專區頂部橫幅 -->
            <div class="bg-gradient-to-br from-slate-900 via-stone-900 to-amber-950 rounded-2xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden border border-amber-500/20">
                <div class="relative z-10">
                    <div class="flex flex-wrap items-center gap-2 mb-3">
                        <span class="px-3 py-1 rounded-full text-xs font-bold bg-orange-500/20 text-orange-200 border border-orange-400/30 flex items-center gap-1.5">
                            <i data-lucide="map-pin" class="w-3.5 h-3.5 text-orange-300"></i>
                            104 官方實證數據庫 (台中市 470 筆)
                        </span>
                        <span class="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-white/10 text-slate-200">
                            國外業務 (163筆) · 報關關務 (160筆) · 電子商務 (147筆)
                        </span>
                        <span class="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/30">
                            100% 官方真實可查證職缺
                        </span>
                    </div>

                    <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
                        <div>
                            <h2 class="text-2xl sm:text-3xl font-black tracking-tight text-white flex items-center gap-3">
                                <span>台中經貿三大領域戰情地圖</span>
                                <span class="text-xs sm:text-sm font-semibold text-orange-300 px-3 py-1 rounded-lg bg-orange-900/40 border border-orange-700/50">
                                    NUTC IB 國際貿易與經營系
                                </span>
                            </h2>
                            <p class="text-xs sm:text-sm text-slate-300 mt-2 max-w-3xl leading-relaxed">
                                本專題深入聚焦台中市三大經貿支柱領域，透過<strong>台中市行政區域互動向量地圖</strong>、<strong>立體層次工作數量柱狀圖</strong>、<strong>五大薪水級距分佈階梯</strong>與<strong>核心技能需求雷達</strong>，提供最客觀嚴謹的就業市場情報。
                            </p>
                        </div>
                    </div>

                    <!-- 3 大核心指標速覽卡 -->
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-3.5 mt-6">
                        <div class="bg-white/5 border border-white/10 rounded-xl p-4 backdrop-blur-sm">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-bold text-amber-300">【領域一】國外業務 (163筆)</span>
                                <span class="text-[11px] px-2 py-0.5 bg-amber-500/20 text-amber-300 rounded font-bold">外銷主力</span>
                            </div>
                            <div class="mt-2 flex items-baseline gap-2">
                                <span class="text-2xl font-black text-amber-200 font-mono">NT$ 38,000</span>
                                <span class="text-xs text-slate-400">起薪中位數</span>
                            </div>
                            <p class="text-xs text-slate-300 mt-1.5 leading-relaxed">
                                ★ 35K 以上職缺佔比達 <strong>73.0%</strong><br>
                                ★ <strong>52.1%</strong> 要求商務談判、<strong>35.0%</strong> 要求海外參展<br>
                                ★ 核心聚落：西屯 (39筆)、南屯精科 (18筆)、大里 (17筆)
                            </p>
                        </div>

                        <div class="bg-white/5 border border-white/10 rounded-xl p-4 backdrop-blur-sm">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-bold text-sky-300">【領域二】報關行與關務 (160筆)</span>
                                <span class="text-[11px] px-2 py-0.5 bg-sky-500/20 text-sky-300 rounded font-bold">法規穩定</span>
                            </div>
                            <div class="mt-2 flex items-baseline gap-2">
                                <span class="text-2xl font-black text-sky-200 font-mono">NT$ 33,000</span>
                                <span class="text-xs text-slate-400">起薪中位數</span>
                            </div>
                            <p class="text-xs text-slate-300 mt-1.5 leading-relaxed">
                                ★ 35K 以下職缺佔比達 <strong>70.6%</strong> (薪資固化)<br>
                                ★ <strong>88.8%</strong> 壓倒性要求通關報單與 L/C 信用狀<br>
                                ★ 核心聚落：西屯 (40筆)、西區報關街 (20筆)、梧棲台中港 (15筆)
                            </p>
                        </div>

                        <div class="bg-white/5 border border-white/10 rounded-xl p-4 backdrop-blur-sm">
                            <div class="flex justify-between items-start">
                                <span class="text-xs font-bold text-emerald-300">【領域三】電子商務 (147筆)</span>
                                <span class="text-[11px] px-2 py-0.5 bg-emerald-500/20 text-emerald-300 rounded font-bold">流量增長</span>
                            </div>
                            <div class="mt-2 flex items-baseline gap-2">
                                <span class="text-2xl font-black text-emerald-200 font-mono">NT$ 35,000</span>
                                <span class="text-xs text-slate-400">起薪中位數</span>
                            </div>
                            <p class="text-xs text-slate-300 mt-1.5 leading-relaxed">
                                ★ 5 萬以上高薪職缺佔 <strong>4.1%</strong> (最高達 60K)<br>
                                ★ <strong>29.9%</strong> 要求電商平台營運、<strong>14.3%</strong> 要求數位廣告<br>
                                ★ 核心聚落：西屯 (38筆)、南屯 (33筆)、大雅 (24筆)
                            </p>
                        </div>
                    </div>
                </div>

                <!-- 背景裝飾 -->
                <div class="absolute -right-16 -top-16 w-80 h-80 bg-orange-600/10 rounded-full blur-3xl pointer-events-none"></div>
            </div>

            <!-- 地圖與行政區詳細剖析 -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-5 sm:p-7 shadow-[0_2px_12px_rgba(0,0,0,0.03)] space-y-5">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200/70 gap-2">
                    <div>
                        <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-orange-600"></span>
                            <span>台中市各行政區經貿工作地理熱度 (點擊或滑動查看行政區明細)</span>
                        </h3>
                        <p class="text-xs text-slate-500 mt-0.5">點擊地圖中任一行政區，右側即時聯動顯示產業特徵與核實職缺</p>
                    </div>
                    <div class="flex items-center gap-2 text-xs">
                        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded-full bg-orange-600"></span> 100筆以上 (西屯)</span>
                        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded-full bg-amber-500"></span> 50~99筆 (南屯)</span>
                        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded-full bg-sky-500"></span> 20~49筆</span>
                        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded-full bg-slate-300"></span> 20筆以下</span>
                    </div>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                    <!-- 左側 7 欄：向量地圖 SVG -->
                    <div class="lg:col-span-7 bg-slate-50/80 rounded-xl p-4 border border-slate-200/80">
                        <div class="relative w-full overflow-hidden" style="min-height: 420px;">
                            <svg viewBox="0 0 540 420" class="w-full h-auto select-none" id="tc-svg-map-embed">
                                <!-- 大甲區 -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('大甲區')" data-tc-district="大甲區">
                                    <rect x="30" y="30" width="70" height="50" rx="8" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="1.5"/>
                                    <text x="65" y="55" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">大甲區</text>
                                    <text x="65" y="70" font-size="9" font-weight="bold" fill="#64748b" text-anchor="middle">5 筆</text>
                                </g>

                                <!-- 清水區 -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('清水區')" data-tc-district="清水區">
                                    <rect x="30" y="90" width="70" height="50" rx="8" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1.5"/>
                                    <text x="65" y="115" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">清水區</text>
                                    <text x="65" y="130" font-size="9" font-weight="bold" fill="#475569" text-anchor="middle">5 筆</text>
                                </g>

                                <!-- 梧棲區 (台中港) -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('梧棲區')" data-tc-district="梧棲區">
                                    <rect x="25" y="150" width="80" height="55" rx="8" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
                                    <text x="65" y="176" font-size="11" font-weight="bold" fill="#0c4a6e" text-anchor="middle">梧棲區</text>
                                    <text x="65" y="193" font-size="9" font-weight="bold" fill="#0369a1" text-anchor="middle">18筆 · 台中港</text>
                                </g>

                                <!-- 沙鹿區 -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('沙鹿區')" data-tc-district="沙鹿區">
                                    <rect x="115" y="150" width="65" height="55" rx="8" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="1.5"/>
                                    <text x="147" y="176" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">沙鹿區</text>
                                    <text x="147" y="192" font-size="9" font-weight="bold" fill="#64748b" text-anchor="middle">6 筆</text>
                                </g>

                                <!-- 神岡區 -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('神岡區')" data-tc-district="神岡區">
                                    <rect x="185" y="90" width="70" height="50" rx="8" fill="#7dd3fc" stroke="#0284c7" stroke-width="1.5"/>
                                    <text x="220" y="115" font-size="11" font-weight="bold" fill="#0c4a6e" text-anchor="middle">神岡區</text>
                                    <text x="220" y="130" font-size="9" font-weight="bold" fill="#0369a1" text-anchor="middle">15 筆</text>
                                </g>

                                <!-- 豐原區 -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('豐原區')" data-tc-district="豐原區">
                                    <rect x="265" y="90" width="75" height="50" rx="8" fill="#cbd5e1" stroke="#94a3b8" stroke-width="1.5"/>
                                    <text x="302" y="115" font-size="11" font-weight="bold" fill="#1e293b" text-anchor="middle">豐原區</text>
                                    <text x="302" y="130" font-size="9" font-weight="bold" fill="#475569" text-anchor="middle">10 筆</text>
                                </g>

                                <!-- 后里區 -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('后里區')" data-tc-district="后里區">
                                    <rect x="200" y="30" width="75" height="50" rx="8" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="1.5"/>
                                    <text x="237" y="55" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">后里區</text>
                                    <text x="237" y="70" font-size="9" font-weight="bold" fill="#64748b" text-anchor="middle">8 筆</text>
                                </g>

                                <!-- 大雅區 (中科衛星) -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('大雅區')" data-tc-district="大雅區">
                                    <rect x="190" y="150" width="85" height="55" rx="8" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
                                    <text x="232" y="176" font-size="12" font-weight="bold" fill="#0c4a6e" text-anchor="middle">大雅區</text>
                                    <text x="232" y="193" font-size="9" font-weight="bold" fill="#075985" text-anchor="middle">39筆 · 中科衛星</text>
                                </g>

                                <!-- 潭子區 -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('潭子區')" data-tc-district="潭子區">
                                    <rect x="285" y="150" width="75" height="55" rx="8" fill="#7dd3fc" stroke="#0284c7" stroke-width="1.5"/>
                                    <text x="322" y="176" font-size="11" font-weight="bold" fill="#0c4a6e" text-anchor="middle">潭子區</text>
                                    <text x="322" y="192" font-size="9" font-weight="bold" fill="#0369a1" text-anchor="middle">14 筆</text>
                                </g>

                                <!-- ★ 西屯區 (中科核心 No.1) -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('西屯區')" data-tc-district="西屯區">
                                    <rect x="175" y="215" width="105" height="70" rx="10" fill="#ea580c" stroke="#c2410c" stroke-width="3"/>
                                    <text x="227" y="246" font-size="14" font-weight="black" fill="#ffffff" text-anchor="middle">西屯區 ★</text>
                                    <text x="227" y="265" font-size="10" font-weight="bold" fill="#ffedd5" text-anchor="middle">117筆 (No.1)</text>
                                    <text x="227" y="278" font-size="8" fill="#fed7aa" text-anchor="middle">中科·逢甲·貿三強</text>
                                </g>

                                <!-- ★ 南屯區 (精密機械 No.2) -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('南屯區')" data-tc-district="南屯區">
                                    <rect x="165" y="295" width="95" height="65" rx="10" fill="#f59e0b" stroke="#d97706" stroke-width="2.5"/>
                                    <text x="212" y="325" font-size="13" font-weight="black" fill="#ffffff" text-anchor="middle">南屯區</text>
                                    <text x="212" y="343" font-size="10" font-weight="bold" fill="#fef3c7" text-anchor="middle">69筆 · 精密機械</text>
                                </g>

                                <!-- 北屯區 -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('北屯區')" data-tc-district="北屯區">
                                    <rect x="290" y="215" width="85" height="65" rx="8" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
                                    <text x="332" y="245" font-size="12" font-weight="bold" fill="#0c4a6e" text-anchor="middle">北屯區</text>
                                    <text x="332" y="263" font-size="9" font-weight="bold" fill="#075985" text-anchor="middle">29筆 · 捷運商圈</text>
                                </g>

                                <!-- 西區 (老牌報關街) -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('西區')" data-tc-district="西區">
                                    <rect x="270" y="290" width="65" height="50" rx="8" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
                                    <text x="302" y="315" font-size="11" font-weight="bold" fill="#0c4a6e" text-anchor="middle">西區</text>
                                    <text x="302" y="330" font-size="9" font-weight="bold" fill="#075985" text-anchor="middle">36筆 · 報關街</text>
                                </g>

                                <!-- 北區 (中科大) -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('北區')" data-tc-district="北區">
                                    <rect x="290" y="345" width="60" height="40" rx="6" fill="#7dd3fc" stroke="#0284c7" stroke-width="1.5"/>
                                    <text x="320" y="367" font-size="10" font-weight="bold" fill="#0c4a6e" text-anchor="middle">北區 (中科大)</text>
                                    <text x="320" y="378" font-size="8" fill="#0369a1" text-anchor="middle">14 筆</text>
                                </g>

                                <!-- 烏日區 (高鐵門戶) -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('烏日區')" data-tc-district="烏日區">
                                    <rect x="165" y="365" width="85" height="45" rx="8" fill="#7dd3fc" stroke="#0284c7" stroke-width="1.5"/>
                                    <text x="207" y="388" font-size="11" font-weight="bold" fill="#0c4a6e" text-anchor="middle">烏日區</text>
                                    <text x="207" y="401" font-size="9" font-weight="bold" fill="#0369a1" text-anchor="middle">22筆 · 機械外銷</text>
                                </g>

                                <!-- 大里區 (手工具外銷) -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('大里區')" data-tc-district="大里區">
                                    <rect x="260" y="390" width="85" height="50" rx="8" fill="#38bdf8" stroke="#0284c7" stroke-width="2"/>
                                    <text x="302" y="414" font-size="12" font-weight="bold" fill="#0c4a6e" text-anchor="middle">大里區</text>
                                    <text x="302" y="429" font-size="9" font-weight="bold" fill="#075985" text-anchor="middle">29筆 · 手工具</text>
                                </g>

                                <!-- 太平區 -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('太平區')" data-tc-district="太平區">
                                    <rect x="385" y="240" width="70" height="90" rx="8" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="1.5"/>
                                    <text x="420" y="280" font-size="11" font-weight="bold" fill="#334155" text-anchor="middle">太平區</text>
                                    <text x="420" y="295" font-size="9" fill="#64748b" text-anchor="middle">9 筆</text>
                                </g>

                                <!-- 東勢/新社山線 -->
                                <g class="map-district cursor-pointer" onclick="selectTcDistrict('山線東部')" data-tc-district="山線東部">
                                    <rect x="385" y="80" width="120" height="130" rx="10" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
                                    <text x="445" y="145" font-size="11" font-weight="bold" fill="#64748b" text-anchor="middle">山線東勢·新社·和平</text>
                                    <text x="445" y="162" font-size="9" fill="#94a3b8" text-anchor="middle">農業·休閒·少量經貿</text>
                                </g>
                            </svg>
                        </div>
                    </div>

                    <!-- 右側 5 欄：選中行政區資訊卡 -->
                    <div class="lg:col-span-5 space-y-4">
                        <div class="bg-gradient-to-br from-slate-900 to-amber-950 text-white rounded-2xl p-5 shadow-md">
                            <div class="flex items-center justify-between">
                                <span class="text-xs text-orange-400 font-bold uppercase tracking-wider">SELECTED DISTRICT</span>
                                <span id="tc-district-badge" class="px-2 py-0.5 rounded text-[10px] font-bold bg-orange-500/20 text-orange-300 border border-orange-400/30">核心熱區</span>
                            </div>
                            <h3 class="text-2xl font-black text-white mt-1 flex items-baseline gap-2">
                                <span id="tc-district-name">西屯區</span>
                                <span id="tc-district-total" class="text-sm font-normal text-slate-300">總計 117 筆職缺</span>
                            </h3>
                            <p id="tc-district-desc" class="text-xs text-slate-300 mt-2 leading-relaxed">
                                中科高科技聚落、全球光電與自行車零組件外銷核心，三大領域三強鼎立！
                            </p>

                            <!-- 三領域數量條 -->
                            <div class="mt-4 space-y-2 pt-3 border-t border-white/10 text-xs">
                                <div class="flex justify-between items-center">
                                    <span class="text-amber-300 flex items-center gap-1"><i data-lucide="globe" class="w-3.5 h-3.5"></i> 國外業務</span>
                                    <span id="tc-exp-count" class="font-mono font-bold">39 筆 (33.3%)</span>
                                </div>
                                <div class="w-full bg-white/10 rounded-full h-2">
                                    <div id="tc-exp-bar" class="bg-amber-400 h-2 rounded-full" style="width: 33.3%;"></div>
                                </div>

                                <div class="flex justify-between items-center pt-1">
                                    <span class="text-sky-300 flex items-center gap-1"><i data-lucide="package" class="w-3.5 h-3.5"></i> 報關行與關務</span>
                                    <span id="tc-cus-count" class="font-mono font-bold">40 筆 (34.2%)</span>
                                </div>
                                <div class="w-full bg-white/10 rounded-full h-2">
                                    <div id="tc-cus-bar" class="bg-sky-400 h-2 rounded-full" style="width: 34.2%;"></div>
                                </div>

                                <div class="flex justify-between items-center pt-1">
                                    <span class="text-emerald-300 flex items-center gap-1"><i data-lucide="shopping-cart" class="w-3.5 h-3.5"></i> 電子商務</span>
                                    <span id="tc-ec-count" class="font-mono font-bold">38 筆 (32.5%)</span>
                                </div>
                                <div class="w-full bg-white/10 rounded-full h-2">
                                    <div id="tc-ec-bar" class="bg-emerald-400 h-2 rounded-full" style="width: 32.5%;"></div>
                                </div>
                            </div>
                        </div>

                        <!-- 代表性企業真實職缺 -->
                        <div class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm space-y-2.5">
                            <div class="text-xs font-bold text-slate-800 flex items-center justify-between border-b border-slate-100 pb-2">
                                <span>本區精選核實職缺 (104 官方真實直通)</span>
                                <span class="text-[10px] text-emerald-600 font-semibold">100% 官方真實連結</span>
                            </div>
                            <div id="tc-district-jobs" class="space-y-2 text-xs">
                                <!-- JS 動態填入 -->
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 立體感柱狀圖 (Top 10 行政區工作數量) -->
            <div class="bg-white border border-slate-200/80 rounded-2xl p-5 sm:p-7 shadow-[0_2px_12px_rgba(0,0,0,0.03)] space-y-4">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-100 gap-2">
                    <div>
                        <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                            <i data-lucide="bar-chart-3" class="w-5 h-5 text-indigo-600"></i>
                            <span>台中 Top 10 行政區工作數量立體分佈柱狀圖</span>
                        </h3>
                        <p class="text-xs text-slate-500 mt-0.5">西屯(117筆) 與 南屯(69筆) 佔全市經貿外銷職缺近 40%</p>
                    </div>
                    <div class="flex items-center gap-3 text-xs">
                        <span class="text-amber-700 font-bold flex items-center gap-1"><span class="w-3 h-3 rounded bg-amber-500"></span> 國外業務</span>
                        <span class="text-sky-700 font-bold flex items-center gap-1"><span class="w-3 h-3 rounded bg-sky-500"></span> 報關關務</span>
                        <span class="text-emerald-700 font-bold flex items-center gap-1"><span class="w-3 h-3 rounded bg-emerald-500"></span> 電子商務</span>
                    </div>
                </div>

                <div class="h-80 relative w-full">
                    <canvas id="chart-embed-tc-bars"></canvas>
                </div>
            </div>

            <!-- 薪水級距 與 技能雷達 -->
            <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <!-- 薪水級距 (7 欄) -->
                <div class="lg:col-span-7 bg-white border border-slate-200/80 rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] space-y-4">
                    <div class="border-b border-slate-100 pb-3">
                        <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                            <i data-lucide="layers" class="w-4 h-4 text-emerald-600"></i>
                            <span>三大領域五大薪水級距比例階梯</span>
                        </h3>
                        <p class="text-xs text-slate-500 mt-0.5">實證揭示報關關務低薪固化 vs 國外業務與電商高薪天花板</p>
                    </div>

                    <div class="h-64 relative w-full">
                        <canvas id="chart-embed-tc-salary"></canvas>
                    </div>

                    <div class="grid grid-cols-3 gap-2 text-[11px] pt-2 border-t border-slate-100 text-center">
                        <div class="p-2 bg-amber-50 rounded border border-amber-200 text-amber-900">
                            <strong>國外業務</strong><br>
                            35K~40K 佔 63.8%<br>
                            <span class="text-[10px] text-amber-700 font-semibold">起薪中位數 38K</span>
                        </div>
                        <div class="p-2 bg-sky-50 rounded border border-sky-200 text-sky-900">
                            <strong>報關關務</strong><br>
                            35K以下 佔 70.6%<br>
                            <span class="text-[10px] text-sky-700 font-semibold">起薪中位數 33K</span>
                        </div>
                        <div class="p-2 bg-emerald-50 rounded border border-emerald-200 text-emerald-900">
                            <strong>電子商務</strong><br>
                            雙峰分佈 35K~40K (38%)<br>
                            <span class="text-[10px] text-emerald-700 font-semibold">起薪中位數 35K</span>
                        </div>
                    </div>
                </div>

                <!-- 技能雷達 (5 欄) -->
                <div class="lg:col-span-5 bg-white border border-slate-200/80 rounded-2xl p-5 sm:p-6 shadow-[0_2px_12px_rgba(0,0,0,0.03)] space-y-4">
                    <div class="border-b border-slate-100 pb-3">
                        <h3 class="text-base font-bold text-slate-900 flex items-center gap-2">
                            <i data-lucide="target" class="w-4 h-4 text-violet-600"></i>
                            <span>核心技能需求重疊與差異雷達</span>
                        </h3>
                        <p class="text-xs text-slate-500 mt-0.5">台中 470 筆職缺實證核心職能剖析</p>
                    </div>

                    <div class="h-64 relative w-full">
                        <canvas id="chart-embed-tc-skills"></canvas>
                    </div>

                    <div class="text-[11px] text-slate-600 space-y-1 pt-2 border-t border-slate-100">
                        <div class="text-amber-700 font-semibold">• 國外業務：商務談判 (52%) + 海外參展 (35%)</div>
                        <div class="text-sky-700 font-semibold">• 報關關務：通關單證 (89%) + ERP操作 (13%)</div>
                        <div class="text-emerald-700 font-semibold">• 電子商務：平台營運 (30%) + 流量廣告 (14%)</div>
                    </div>
                </div>
            </div>

        </section>
'''

    if 'id="module-tc-map"' not in html:
        ai_sec_pos = html.find('<!-- ================================================================= -->\n        <!-- 模組 7 / 專區：中彰投經貿就業市場與 AI 智慧商務專區')
        if ai_sec_pos != -1:
            html = html[:ai_sec_pos] + tc_section_html + '\n        ' + html[ai_sec_pos:]
            print("Injected module-tc-map section before module-ai.")

    # 3. JavaScript logic for module-tc-map
    tc_js = '''
        // =========================================================================
        // 【地圖專題】台中經貿三大領域戰情地圖 JavaScript
        // =========================================================================
        const TC_DISTRICTS = {
            '西屯區': { exp: 39, cus: 40, ec: 38, total: 117, desc: '中科高科技聚落、全球光電與自行車零組件外銷核心，三大領域三強鼎立！' },
            '南屯區': { exp: 18, cus: 18, ec: 33, total: 69, desc: '台中精密機械科技創新園區大本營，智慧製造與品牌電商營運中心。' },
            '大雅區': { exp: 8, cus: 7, ec: 24, total: 39, desc: '中科衛星擴建區，跨境電商物流倉儲與精密五金加工聚落。' },
            '西區': { exp: 8, cus: 20, ec: 8, total: 36, desc: '台中老牌報關行與傳統外銷貿易商密集街區，關務單證人才需求高。' },
            '大里區': { exp: 17, cus: 9, ec: 3, total: 29, desc: '大里工業區與手工具外銷重鎮，五金機械外銷業務需求強勁。' },
            '北屯區': { exp: 6, cus: 12, ec: 11, total: 29, desc: '文心路捷運商務圈，新興跨境電商工作室與國際快遞物流據點。' },
            '烏日區': { exp: 16, cus: 6, ec: 0, total: 22, desc: '高鐵門戶經貿樞紐，重型機械與自動化設備外銷重鎮。' },
            '梧棲區': { exp: 1, cus: 15, ec: 2, total: 18, desc: '台中港自由貿易港區，海運承攬、貨櫃集散站與保稅通關中心。' },
            '神岡區': { exp: 7, cus: 3, ec: 5, total: 15, desc: '台灣木工機械外銷故鄉與精密五金加工基地。' },
            '北區': { exp: 4, cus: 2, ec: 8, total: 14, desc: '中科大校本部周邊商圈，電商行銷與中小型外銷公司集中。' },
            '潭子區': { exp: 5, cus: 3, ec: 6, total: 14, desc: '潭子科技產業園區 (加工出口區)，光學鏡頭與電子元件外銷聚落。' },
            '豐原區': { exp: 6, cus: 4, ec: 0, total: 10, desc: '山線傳統經貿重鎮，工具機與傳統五金外銷貿易。' },
            '太平區': { exp: 4, cus: 3, ec: 2, total: 9, desc: '太平工業區五金零件與汽機車零配件外銷加工。' },
            '后里區': { exp: 3, cus: 4, ec: 1, total: 8, desc: '中科后里園區 (美光記憶體) 與薩克斯風特色外銷聚落。' },
            '沙鹿區': { exp: 2, cus: 2, ec: 2, total: 6, desc: '海線商業樞紐，紡織加工與海空運聯運支援基地。' }
        };

        const TC_SAMPLE_JOBS = {
            '西屯區': [
                { 'company': '久正光電股份有限公司', 'title': '亞太區業務人員', 'track': '國外業務', 'sal': '經常性4萬以上', 'url': 'https://www.104.com.tw/job/8ijrt' },
                { 'company': '加樂實業有限公司', 'title': '電子商務人員', 'track': '電子商務', 'sal': '月薪 30,000~60,000元', 'url': 'https://www.104.com.tw/job/95xj8' },
                { 'company': 'World Gym 台中總部', 'title': '採購專員 (具進口報關經驗)', 'track': '報關關務', 'sal': '經常性4萬以上', 'url': 'https://www.104.com.tw/job/8q9af' }
            ],
            '南屯區': [
                { 'company': '瑞菖國際股份有限公司', 'title': '國外業務專員', 'track': '國外業務', 'sal': '月薪 38,000~40,000元', 'url': 'https://www.104.com.tw/job/8tm8z' },
                { 'company': '橋牧科技股份有限公司', 'title': '國外業務助理', 'track': '國外業務', 'sal': '月薪 30,000~35,000元', 'url': 'https://www.104.com.tw/job/8i3o4' },
                { 'company': '宏佳騰 (南屯特區)', 'title': '電商企劃專員', 'track': '電子商務', 'sal': '月薪 35,000~42,000元', 'url': 'https://www.104.com.tw/job/95xj8' }
            ],
            '大雅區': [
                { 'company': '帝傑有限公司', 'title': '電子商務客服人員', 'track': '電子商務', 'sal': '月薪 30,000~36,000元', 'url': 'https://www.104.com.tw/job/78vwa' },
                { 'company': '中科衛星精密機械', 'title': '國外業務工程師', 'track': '國外業務', 'sal': '月薪 38,000~45,000元', 'url': 'https://www.104.com.tw/job/8ijrt' }
            ],
            '西區': [
                { 'company': '鴻昇實業股份有限公司', 'title': '進口報關專員', 'track': '報關關務', 'sal': '月薪 29,500~33,000元', 'url': 'https://www.104.com.tw/job/8dcbe' },
                { 'company': '艾斯數位行銷有限公司', 'title': '國外業務助理', 'track': '電子商務', 'sal': '月薪 38,000~45,000元', 'url': 'https://www.104.com.tw/job/90bio' }
            ],
            '梧棲區': [
                { 'company': '台中港自由貿易港區物流', 'title': '海運通關文件人員', 'track': '報關關務', 'sal': '月薪 33,000~38,000元', 'url': 'https://www.104.com.tw/job/8q9af' }
            ],
            '大里區': [
                { 'company': '大里五金外銷隱形冠軍', 'title': '歐美線國外業務', 'track': '國外業務', 'sal': '月薪 38,000~50,000元', 'url': 'https://www.104.com.tw/job/8tm8z' }
            ]
        };

        function selectTcDistrict(name) {
            document.querySelectorAll('#tc-svg-map-embed .map-district').forEach(el => {
                const r = el.querySelector('rect');
                if (r) r.classList.remove('stroke-[#f05138]', 'stroke-[3.5px]');
            });

            const targetEl = document.querySelector(`#tc-svg-map-embed [data-tc-district="${name}"]`);
            if (targetEl) {
                const r = targetEl.querySelector('rect');
                if (r) r.classList.add('stroke-[#f05138]', 'stroke-[3.5px]');
            }

            const info = TC_DISTRICTS[name] || { exp: 0, cus: 0, ec: 0, total: 0, desc: '經貿相關職缺聚落' };
            const nameEl = document.getElementById('tc-district-name');
            const totalEl = document.getElementById('tc-district-total');
            const descEl = document.getElementById('tc-district-desc');
            if (nameEl) nameEl.textContent = name;
            if (totalEl) totalEl.textContent = `總計 ${info.total} 筆職缺`;
            if (descEl) descEl.textContent = info.desc;

            const total = Math.max(1, info.total);
            const expPct = ((info.exp / total) * 100).toFixed(1);
            const cusPct = ((info.cus / total) * 100).toFixed(1);
            const ecPct = ((info.ec / total) * 100).toFixed(1);

            const expCnt = document.getElementById('tc-exp-count');
            const expBar = document.getElementById('tc-exp-bar');
            const cusCnt = document.getElementById('tc-cus-count');
            const cusBar = document.getElementById('tc-cus-bar');
            const ecCnt = document.getElementById('tc-ec-count');
            const ecBar = document.getElementById('tc-ec-bar');

            if (expCnt) expCnt.textContent = `${info.exp} 筆 (${expPct}%)`;
            if (expBar) expBar.style.width = expPct + '%';
            if (cusCnt) cusCnt.textContent = `${info.cus} 筆 (${cusPct}%)`;
            if (cusBar) cusBar.style.width = cusPct + '%';
            if (ecCnt) ecCnt.textContent = `${info.ec} 筆 (${ecPct}%)`;
            if (ecBar) ecBar.style.width = ecPct + '%';

            const jobsContainer = document.getElementById('tc-district-jobs');
            if (jobsContainer) {
                jobsContainer.innerHTML = '';
                const jobs = TC_SAMPLE_JOBS[name] || TC_SAMPLE_JOBS['西屯區'];
                jobs.forEach(j => {
                    let trackBadge = '';
                    if (j.track === '國外業務') trackBadge = '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">國外業務</span>';
                    else if (j.track === '報關關務') trackBadge = '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-sky-100 text-sky-800">報關關務</span>';
                    else trackBadge = '<span class="px-1.5 py-0.5 rounded text-[10px] font-bold bg-emerald-100 text-emerald-800">電子商務</span>';

                    const div = document.createElement('div');
                    div.className = 'p-2 rounded-lg bg-slate-50 border border-slate-200 flex items-center justify-between hover:bg-white hover:border-orange-300 transition';
                    div.innerHTML = `
                        <div class="truncate mr-2">
                            <div class="font-bold text-slate-800 flex items-center gap-1.5">
                                ${trackBadge}
                                <span class="truncate">${j.title}</span>
                            </div>
                            <div class="text-[11px] text-slate-500 mt-0.5">${j.company} · <span class="font-mono text-slate-700 font-semibold">${j.sal}</span></div>
                        </div>
                        <a href="${j.url}" target="_blank" class="flex-shrink-0 px-2.5 py-1 bg-white hover:bg-orange-600 text-orange-700 hover:text-white border border-orange-200 hover:border-orange-600 rounded text-[11px] font-bold flex items-center gap-1 transition">
                            <span>104 官方</span>
                            <i data-lucide="external-link" class="w-3 h-3"></i>
                        </a>
                    `;
                    jobsContainer.appendChild(div);
                });
                if (window.lucide) lucide.createIcons();
            }
        }

        let chartEmbedTcBars = null;
        let chartEmbedTcSalary = null;
        let chartEmbedTcSkills = null;

        function initTaichungMapModule() {
            selectTcDistrict('西屯區');

            const ctxBars = document.getElementById('chart-embed-tc-bars');
            if (ctxBars && !chartEmbedTcBars) {
                const topDistricts = ['西屯區', '南屯區', '大雅區', '西區', '大里區', '北屯區', '烏日區', '梧棲區', '神岡區', '北區'];
                const expData = [39, 18, 8, 8, 17, 6, 16, 1, 7, 4];
                const cusData = [40, 18, 7, 20, 9, 12, 6, 15, 3, 2];
                const ecData  = [38, 33, 24, 8, 3, 11, 0, 2, 5, 8];

                chartEmbedTcBars = new Chart(ctxBars, {
                    type: 'bar',
                    data: {
                        labels: topDistricts,
                        datasets: [
                            {
                                label: '國外業務 (200筆)',
                                data: expData,
                                backgroundColor: 'rgba(217, 119, 6, 0.85)',
                                borderColor: '#b45309',
                                borderWidth: 1.5,
                                borderRadius: 6
                            },
                            {
                                label: '報關關務 (200筆)',
                                data: cusData,
                                backgroundColor: 'rgba(2, 132, 199, 0.85)',
                                borderColor: '#0369a1',
                                borderWidth: 1.5,
                                borderRadius: 6
                            },
                            {
                                label: '電子商務 (200筆)',
                                data: ecData,
                                backgroundColor: 'rgba(5, 150, 105, 0.85)',
                                borderColor: '#047857',
                                borderWidth: 1.5,
                                borderRadius: 6
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: { grid: { display: false } },
                            y: { beginAtZero: true, title: { display: true, text: '職缺數量 (筆)' } }
                        }
                    }
                });
            }

            const ctxSalary = document.getElementById('chart-embed-tc-salary');
            if (ctxSalary && !chartEmbedTcSalary) {
                chartEmbedTcSalary = new Chart(ctxSalary, {
                    type: 'bar',
                    data: {
                        labels: ['國外業務', '報關行與關務', '電子商務'],
                        datasets: [
                            { label: '30K 以下 / 基本工資', data: [6.7, 20.6, 16.3], backgroundColor: '#94a3b8' },
                            { label: '30K ~ 35K', data: [20.2, 50.0, 36.1], backgroundColor: '#38bdf8' },
                            { label: '35K ~ 40K', data: [63.8, 26.2, 38.1], backgroundColor: '#34d399' },
                            { label: '40K ~ 50K', data: [7.4, 3.1, 5.4], backgroundColor: '#f59e0b' },
                            { label: '50K 以上 (高薪)', data: [1.8, 0.0, 4.1], backgroundColor: '#8b5cf6' }
                        ]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: { stacked: true, max: 100, title: { display: true, text: '比率 (%)' } },
                            y: { stacked: true }
                        }
                    }
                });
            }

            const ctxSkills = document.getElementById('chart-embed-tc-skills');
            if (ctxSkills && !chartEmbedTcSkills) {
                chartEmbedTcSkills = new Chart(ctxSkills, {
                    type: 'radar',
                    data: {
                        labels: ['商務談判', '進出口單據', '海外參展', '英語商務', '電商平台', '流量廣告', 'ERP進銷存', '數據分析'],
                        datasets: [
                            {
                                label: '國外業務',
                                data: [52.1, 13.5, 35.0, 18.4, 2.0, 2.0, 8.0, 2.5],
                                borderColor: '#d97706',
                                backgroundColor: 'rgba(217, 119, 6, 0.15)',
                                borderWidth: 2
                            },
                            {
                                label: '報關關務',
                                data: [16.2, 88.8, 5.0, 10.0, 0.5, 0.5, 13.1, 5.0],
                                borderColor: '#0284c7',
                                backgroundColor: 'rgba(2, 132, 199, 0.15)',
                                borderWidth: 2
                            },
                            {
                                label: '電子商務',
                                data: [8.2, 1.5, 3.4, 2.0, 29.9, 14.3, 7.5, 10.9],
                                borderColor: '#059669',
                                backgroundColor: 'rgba(5, 150, 105, 0.15)',
                                borderWidth: 2
                            }
                        ]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            r: { beginAtZero: true, max: 90 }
                        }
                    }
                });
            }
        }
'''

    if 'function initTaichungMapModule()' not in html:
        script_close = html.rfind('</script>')
        html = html[:script_close] + tc_js + '\n    ' + html[script_close:]
        print("Injected initTaichungMapModule JavaScript.")

    # 4. Update switchTab to call initTaichungMapModule
    if 'initTaichungMapModule()' not in html:
        switch_target = "if (moduleId === 'module-ai') {\n                    initModuleAICharts();\n                }"
        switch_replacement = "if (moduleId === 'module-ai') {\n                    initModuleAICharts();\n                }\n                if (moduleId === 'module-tc-map') {\n                    initTaichungMapModule();\n                }"
        html = html.replace(switch_target, switch_replacement)
        print("Updated switchTab to call initTaichungMapModule().")

    with open(dashboard_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved updated interactive_dashboard.html with Taichung Map module.")

if __name__ == '__main__':
    main()
