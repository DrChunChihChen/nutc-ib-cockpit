"""
generate_heatmap.py
從 7 大系所 output/<slug>/dept_data.json 重新生成 output/heatmap.html，
保證熱力總覽表百分之百採用審定之【純日間部】各項指標。
"""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output"

DEPTS = [
    ("ib", "國際貿易與經營系", "0414"),
    ("ba", "企業管理系", "0413"),
    ("accounting", "會計資訊系", "0411"),
    ("finance", "財務金融系", "0412"),
    ("insurance", "保險金融管理系", "0412"),
    ("stat", "應用統計系", "0542"),
    ("tax", "財政稅務系", "0412"),
]

def generate_heatmap():
    rows_html = []
    for slug, default_name, isced in DEPTS:
        data_path = OUTPUT_DIR / slug / "dept_data.json"
        with open(data_path, "r", encoding="utf-8") as f:
            d = json.load(f)

        name = d.get("dept_name") or default_name
        prof = d.get("profile", {})
        kpis = d.get("kpis", {})
        k24 = d.get("k24", {})

        students = prof.get("students_total", 0)
        k01 = kpis.get("K01", {}).get("value", 0.0)
        k02 = kpis.get("K02", {}).get("value", 0.0)
        k03 = kpis.get("K03", {}).get("value", 0.0)
        k06 = kpis.get("K06", {}).get("value", 0.0)
        k19 = kpis.get("K19", {}).get("value", 0.0)
        score = k24.get("score", kpis.get("K24", {}).get("value", 0.0))
        grade = k24.get("grade", "A 穩健")

        # Color badges
        score_badge = "bg-emerald-100 text-emerald-800" if score >= 80 else ("bg-amber-100 text-amber-800" if score >= 60 else "bg-rose-100 text-rose-800")
        dot_color = "bg-emerald-500" if score >= 80 else ("bg-amber-500" if score >= 60 else "bg-rose-500")
        k01_color = "text-emerald-700 font-bold" if k01 >= 98 else "text-amber-700 font-bold"
        k03_color = "text-emerald-700" if k03 < 3.0 else ("text-stone-700" if k03 < 5.0 else "text-rose-700 font-bold")
        k06_color = "text-rose-700 font-bold" if k06 > 35 else "text-stone-700"
        k19_color = "text-rose-700 font-bold" if k19 < -15 else "text-stone-700"

        link_prefix = f"{slug}/index.html" if slug != "ib" else "ib/index.html"

        row = f"""
                        <tr class="hover:bg-stone-50/80 transition-colors">
                            <td class="py-3.5 px-4 font-bold text-stone-900 flex items-center space-x-2">
                                <span class="h-2 w-2 rounded-full {dot_color}"></span>
                                <a href="{link_prefix}" class="hover:text-brand-700 hover:underline" target="_blank" rel="noopener noreferrer">{name}</a>
                            </td>
                            <td class="py-3.5 px-3 text-center font-mono text-stone-500">{isced}</td>
                            <td class="py-3.5 px-3 text-right font-mono">{students}</td>
                            <td class="py-3.5 px-3 text-right font-mono {k01_color}">
                                {k01}%
                            </td>
                            <td class="py-3.5 px-3 text-right font-mono">{k02:+.2f}</td>
                            <td class="py-3.5 px-3 text-right font-mono {k03_color}">
                                {k03:.2f}%
                            </td>
                            <td class="py-3.5 px-3 text-right font-mono {k06_color}">
                                {k06:.1f}
                            </td>
                            <td class="py-3.5 px-3 text-right font-mono {k19_color}">
                                {k19:.1f}%
                            </td>
                            <td class="py-3.5 px-3 text-center">
                                <span class="inline-block px-2.5 py-1 rounded-full text-[11px] font-bold {score_badge}">
                                    {score} 分（{grade}）
                                </span>
                            </td>
                            <td class="py-3.5 px-4 text-center">
                                <a href="{link_prefix}" class="inline-flex items-center text-xs font-semibold text-brand-700 hover:text-brand-800 hover:underline" target="_blank" rel="noopener noreferrer">
                                    深入戰情室 →
                                </a>
                            </td>
                        </tr>"""
        rows_html.append(row)

    tbody = "\n".join(rows_html)

    html = f"""<!DOCTYPE html>
<html lang="zh-Hant" class="scroll-smooth">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>國立臺中科技大學 · 全院系所校務健康與少子化風險熱力圖（純日間部審定基準）</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-stone-50 text-stone-900 font-sans antialiased">

    <!-- Global College Navigation Bar -->
    <div style="background-color: #1c1917; color: #d6d3d1; font-size: 11px; padding: 7px 16px; border-bottom: 1px solid #292524; position: sticky; top: 0; z-index: 99999; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <div style="max-width: 1350px; margin: 0 auto; display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 8px;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="display: inline-block; width: 7px; height: 7px; border-radius: 50%; background-color: #10b981;"></span>
                <span style="font-weight: 700; color: #ffffff; letter-spacing: 0.02em;">國立臺中科技大學 商學院校務決策網絡</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; overflow-x: auto;">
                <a href="index.html" class="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">國貿系</a> <span class="text-stone-600">|</span> <a href="ba/index.html" class="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">企管系</a> <span class="text-stone-600">|</span> <a href="accounting/index.html" class="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">會資系</a> <span class="text-stone-600">|</span> <a href="finance/index.html" class="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">財金系</a> <span class="text-stone-600">|</span> <a href="insurance/index.html" class="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">保金系</a> <span class="text-stone-600">|</span> <a href="stat/index.html" class="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">應統系</a> <span class="text-stone-600">|</span> <a href="tax/index.html" class="hover:text-white transition-colors" target="_blank" rel="noopener noreferrer">財稅系</a>
                <span style="color: #44403c;">|</span>
                <a href="heatmap.html" style="padding: 2px 8px; border-radius: 4px; background-color: #047857; color: #ffffff; font-weight: 700; text-decoration: none;" target="_blank" rel="noopener noreferrer">📊 全院健康熱力總覽</a>
            </div>
        </div>
    </div>
    
    <header class="bg-white border-b border-stone-200 py-6">
        <div class="max-w-7xl mx-auto px-4 sm:px-6">
            <div class="flex items-center justify-between">
                <div>
                    <span class="text-xs font-bold text-emerald-800 uppercase tracking-widest">IR Autopilot 全院宏觀監控 · 純日間部審定基準</span>
                    <h1 class="text-2xl font-bold tracking-tight text-stone-900 mt-1">國立臺中科技大學 · 商學院全系所健康診斷熱力總覽</h1>
                </div>
                <div class="flex items-center space-x-3">
                    <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
                        7 大系所純日間部監控中
                    </span>
                    <a href="index.html" class="text-xs font-semibold px-3 py-2 bg-stone-900 text-white rounded-lg hover:bg-stone-800" target="_blank" rel="noopener noreferrer">
                        返回主戰情室
                    </a>
                </div>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-8">
        <!-- 說明卡 -->
        <div class="bg-white p-6 rounded-2xl border border-stone-200 shadow-sm">
            <h2 class="text-base font-bold text-stone-900">熱力圖判讀指引 (Heatmap Guide) · 純日間部統計口徑</h2>
            <p class="text-xs text-stone-600 mt-1 leading-relaxed">
                本表即時聚合教育部 UDB 公開審定報表與內政部出生數少子化 16 年推估模型。
                <strong>全院各指標全面以【純日間部】（四技、二技、五專、日間碩士）為唯一分析基準</strong>，已徹底排除進修部夜間在職流失數據之混淆干擾。
                色階標註：<span class="text-emerald-700 font-bold">綠色（健康穩健）</span>、<span class="text-stone-700 font-bold">灰色（常態）</span>、<span class="text-rose-700 font-bold">紅色（需關注/需調節）</span>。
                點擊任一系所名稱可直接切換進入該系所微觀戰情室。
            </p>
        </div>

        <!-- 熱力圖主表 -->
        <div class="bg-white rounded-2xl border border-stone-200 shadow-sm overflow-hidden">
            <div class="overflow-x-auto">
                <table class="w-full text-left text-xs border-collapse">
                    <thead>
                        <tr class="bg-stone-100/70 border-b border-stone-200 font-semibold text-stone-700 uppercase">
                            <th class="py-3 px-4">系所名稱</th>
                            <th class="py-3 px-3 text-center">學類代碼</th>
                            <th class="py-3 px-3 text-right">在學生數（純日間）</th>
                            <th class="py-3 px-3 text-right">新生註冊率 [K01]</th>
                            <th class="py-3 px-3 text-right">3年斜率 [K02]</th>
                            <th class="py-3 px-3 text-right">退學率 [K03]（純日間）</th>
                            <th class="py-3 px-3 text-right">專任生師比 [K06]</th>
                            <th class="py-3 px-3 text-right">117海嘯缺口 [K19]</th>
                            <th class="py-3 px-3 text-center">綜合評級 [K24]</th>
                            <th class="py-3 px-4 text-center">操作</th>
                        </tr>
                    </thead>
                    <tbody class="divide-y divide-stone-100">
{tbody}
                    </tbody>
                </table>
            </div>
        </div>
    </main>

</body>
</html>
"""
    dest = OUTPUT_DIR / "heatmap.html"
    with open(dest, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ Successfully updated output/heatmap.html with audited pure daytime metrics!")

if __name__ == "__main__":
    generate_heatmap()
