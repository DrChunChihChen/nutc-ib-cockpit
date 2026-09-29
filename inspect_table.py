from bs4 import BeautifulSoup

with open("/Users/chenchunchih/Downloads/國立臺中科技大學國際貿易與經營系 - 115年四技二專甄選入學交叉查榜-www.com.tw.html", "r", encoding="utf-8", errors="ignore") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")
tables = soup.find_all("table")
for i, t in enumerate(tables):
    txt = t.get_text()
    if "准考證" in txt:
        rows = t.find_all("tr")
        print(f"Table {i} has 准考證! Total rows: {len(rows)}")
        for r_idx, r in enumerate(rows[:10]):
            cells = [td.get_text(strip=True) for td in r.find_all(["td", "th"])]
            print(f"  Row {r_idx}: {cells}")
