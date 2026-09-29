import re

with open("interactive_dashboard.html", "r", encoding="utf-8") as f:
    html = f.read()

dark_bgs = set(re.findall(r"bg-slate-[789]00[^\s\"'>]*", html))
print("Dark backgrounds found:", len(dark_bgs), dark_bgs)

light_texts = set(re.findall(r"text-slate-[123]00[^\s\"'>]*", html))
print("Light texts found:", len(light_texts), light_texts)

dark_borders = set(re.findall(r"border-slate-[678]00[^\s\"'>]*", html))
print("Dark borders found:", len(dark_borders), dark_borders)
