# -*- coding: utf-8 -*-
with open('/Users/chenchunchih/Downloads/校務資料/update_dashboard_with_raw_data_center.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace dot access with bracket access for numeric-starting keys
code = code.replace(
    "s.學校代碼, `\"${s.學校名稱}\"`, s.公私立, s.學校類型, s.縣市, s.113全校總人數, s.113大一新生實招, s.日間大一生, s.進修大一生, `\"${s.117存活分層}\"`, s.117預估存活率, `\"${s.117命運與因應策略推估}\"`",
    "s['學校代碼'], `\"${s['學校名稱']}\"`, s['公私立'], s['學校類型'], s['縣市'], s['113全校總人數'], s['113大一新生實招'], s['日間大一生'], s['進修大一生'], `\"${s['117存活分層']}\"`, s['117預估存活率'], `\"${s['117命運與因應策略推估']}\"`"
)

code = code.replace(
    "u.學校代碼, `\"${u.學校名稱}\"`, u.公私立, u.縣市, u.113全校總人數, u.113大一新生實招, u.日間大一生, u.進修大一生, `\"${u.117存活分層}\"`, u.117預估存活率, `\"${u.117命運與因應策略推估}\"`",
    "u['學校代碼'], `\"${u['學校名稱']}\"`, u['公私立'], u['縣市'], u['113全校總人數'], u['113大一新生實招'], u['日間大一生'], u['進修大一生'], `\"${u['117存活分層']}\"`, u['117預估存活率'], `\"${u['117命運與因應策略推估']}\"`"
)

with open('/Users/chenchunchih/Downloads/校務資料/update_dashboard_with_raw_data_center.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Fixed update_dashboard_with_raw_data_center.py")
