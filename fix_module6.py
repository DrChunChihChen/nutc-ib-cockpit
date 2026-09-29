# -*- coding: utf-8 -*-
import re

html_path = '/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 確保 DOMContentLoaded 呼叫 initModule6Charts()
if "initModule6Charts();" not in html:
    html = html.replace("initModule5Charts();", "initModule5Charts();\n                initModule6Charts();")

# 2. 定義 initModule6Charts() 函數
m6_fn_code = """
        function initModule6Charts() {
            const ctxPoachers = document.getElementById('chart-m6-top-poachers');
            if (ctxPoachers && !Chart.getChart(ctxPoachers)) {
                charts.m6Poachers = new Chart(ctxPoachers.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: [
                            '高科 航運管理系', '高科 國際企業系', '逢甲 國際經營與貿易', 
                            '高科 行銷與流通', '高科 運籌管理系', '北商 國際商務系', 
                            '中原 國際經營與貿易', '雲科 國際管理學程', '北護 健康事業管理', '銘傳 國際企業學系'
                        ],
                        datasets: [{
                            label: '遭搶走人數',
                            data: [37, 22, 20, 12, 12, 10, 9, 8, 6, 6],
                            backgroundColor: [
                                '#f43f5e', '#fb7185', '#f59e0b', '#06b6d4', '#38bdf8', 
                                '#6366f1', '#818cf8', '#a855f7', '#ec4899', '#64748b'
                            ],
                            borderRadius: 6
                        }]
                    },
                    options: {
                        indexAxis: 'y',
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) { return ' 遭掠奪: ' + ctx.raw + ' 名學生'; }
                                }
                            }
                        },
                        scales: {
                            x: { grid: { color: '#334155' }, ticks: { color: '#94a3b8', font: { size: 11 } } },
                            y: { grid: { display: false }, ticks: { color: '#e2e8f0', font: { size: 11 } } }
                        }
                    }
                });
            }

            const ctxDonut = document.getElementById('chart-m6-dest-donut');
            if (ctxDonut && !Chart.getChart(ctxDonut)) {
                charts.m6Donut = new Chart(ctxDonut.getContext('2d'), {
                    type: 'doughnut',
                    data: {
                        labels: ['原系留任就讀', '流失至他校', '未分發/放棄'],
                        datasets: [{
                            data: [168, 229, 107],
                            backgroundColor: ['#10b981', '#f43f5e', '#64748b'],
                            borderWidth: 2,
                            borderColor: '#1e293b'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { position: 'bottom', labels: { color: '#cbd5e1', font: { size: 11 } } },
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) {
                                        const total = 504;
                                        const pct = ((ctx.raw / total) * 100).toFixed(1);
                                        return ` ${ctx.label}: ${ctx.raw} 人 (${pct}%)`;
                                    }
                                }
                            }
                        },
                        cutout: '65%'
                    }
                });
            }

            const ctxDuel = document.getElementById('chart-m6-itm-vs-ba');
            if (ctxDuel && !Chart.getChart(ctxDuel)) {
                charts.m6Duel = new Chart(ctxDuel.getContext('2d'), {
                    type: 'bar',
                    data: {
                        labels: ['選擇中科國貿', '選擇中科企管', '轉向其他學校'],
                        datasets: [{
                            label: '雙榜考生就讀人數',
                            data: [34, 11, 70],
                            backgroundColor: ['#10b981', '#f59e0b', '#64748b'],
                            borderRadius: 6
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: {
                            legend: { display: false },
                            tooltip: {
                                callbacks: {
                                    label: function(ctx) { return ` 就讀人數: ${ctx.raw} 人`; }
                                }
                            }
                        },
                        scales: {
                            y: { grid: { color: '#334155' }, ticks: { color: '#94a3b8', font: { size: 11 } } },
                            x: { grid: { display: false }, ticks: { color: '#e2e8f0' } }
                        }
                    }
                });
            }
        }
"""

if "function initModule6Charts()" not in html:
    html = html.replace("function renderModule5Retire()", m6_fn_code + "\n        function renderModule5Retire()")

# 3. 在 switchTab 確保切換至 module6 時觸發圖表初始化與尺寸重繪
switch_enhancement = """
            requestAnimationFrame(() => {
                if (window.lucide && typeof lucide.createIcons === 'function') {
                    lucide.createIcons();
                }
                if (moduleId === 'module6') {
                    initModule6Charts();
                }
                if (typeof Chart !== 'undefined') {
                    const activeCanvases = document.querySelectorAll('#' + moduleId + ' canvas');
                    activeCanvases.forEach(canvas => {
                        const chartInstance = Chart.getChart(canvas);
                        if (chartInstance) chartInstance.resize();
                    });
                }
            });
"""

html = re.sub(r'requestAnimationFrame\(\(\)\s*=>\s*\{.*?\}\);', switch_enhancement.strip(), html, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("修復完成！檔案大小:", len(html))
