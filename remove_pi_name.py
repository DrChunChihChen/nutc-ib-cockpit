with open("interactive_dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Header (Line 86-88)
text = text.replace(
    '<span class="text-slate-600">|</span>\n                            <span class="text-emerald-600 font-medium">主持人：陳俊智 副教授 (Dr. Elvis Chen)</span>\n                            <span class="text-slate-600">|</span>',
    '<span class="text-slate-400">|</span>'
)
text = text.replace(
    '<span class="text-emerald-600 font-medium">主持人：陳俊智 副教授 (Dr. Elvis Chen)</span>',
    ''
)

# 2. Modal Persona
text = text.replace(
    '<strong class="text-slate-900">主責使用者：Dr. Elvis Chen (陳俊智副教授)</strong>',
    '<strong class="text-slate-900">主責單位：國際貿易與經營系 策略小組</strong>'
)
text = text.replace(
    '國立臺中科技大學 國際貿易與經營系 資深學者，主持系務策略發展、校務研究 (IR) 及少子化避險轉型工程。需具備精確數值佐證之動態模型以說服系所同仁與校級決策層。',
    '國立臺中科技大學 國際貿易與經營系，主責系務策略發展、校務研究 (IR) 及少子化避險轉型工程。具備精確數值佐證之動態模型以支持系務發展與校級策略決策。'
)

# 3. Footer
text = text.replace(
    '<span class="text-emerald-600 font-semibold">Dr. Elvis Chen</span>',
    '<span class="text-slate-500 font-medium">NUTC ITM Strategy Group</span>'
)

# 4. DB Metadata
text = text.replace(
    '"principal_investigator": "陳俊智 副教授 (Dr. Elvis Chen)"',
    '"principal_investigator": "國立臺中科技大學 國際貿易與經營系"'
)

with open("interactive_dashboard.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully removed PI name references!")
