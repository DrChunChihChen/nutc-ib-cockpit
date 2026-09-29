import re

with open("interactive_dashboard.html", "r", encoding="utf-8") as f:
    text = f.read()

for i in range(1, 7):
    pattern = rf'<section id="module{i}"[\s\S]*?</section>'
    m = re.search(pattern, text)
    if m:
        content = m.group(0)
        dark_bgs = set(re.findall(r'bg-slate-[789]00[^\s"\'>]*', content))
        print(f"Module {i} dark bgs: {len(dark_bgs)}", dark_bgs)
        light_txts = set(re.findall(r'text-slate-[123]00[^\s"\'>]*', content))
        print(f"Module {i} light texts: {len(light_txts)}", light_txts)
