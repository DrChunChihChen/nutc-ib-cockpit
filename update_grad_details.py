# -*- coding: utf-8 -*-
with open('/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update DB.regional_six
old_reg_six = '"regional_six": [{"code": "北商-國商", "school": "臺北商業大學", "dept": "國際商務系/科", "region": "北部", "total_stu": 919, "five_year": 266, "undergrad_day": 439, "undergrad_eve": 160, "grad": 54,'
new_reg_six = '"regional_six": [{"code": "北商-國商", "school": "臺北商業大學", "dept": "國際商務系/科", "region": "北部", "total_stu": 919, "five_year": 266, "undergrad_day": 439, "undergrad_eve": 160, "grad": 54, "grad_detail": "日碩32 · 電商產碩12 · 文創產碩10", "grad_tooltip": "日間碩士班 32人、跨境電商產碩 12人、文創產碩 10人 (無獨立博士與碩專)",'

assert old_reg_six in content, 'old_reg_six not found'
content = content.replace(old_reg_six, new_reg_six, 1)

old_itm = '{"code": "中科-國貿", "school": "臺中科技大學", "dept": "國際貿易與經營系/科", "region": "中部", "total_stu": 1044, "five_year": 248, "undergrad_day": 482, "undergrad_eve": 314, "grad": 0,'
new_itm = '{"code": "中科-國貿", "school": "臺中科技大學", "dept": "國際貿易與經營系/科", "region": "中部", "total_stu": 1044, "five_year": 248, "undergrad_day": 482, "undergrad_eve": 314, "grad": 0, "grad_detail": "統整於商學院碩士班", "grad_tooltip": "系所專注培育大學部，研究所名額由商學院統整統籌",'
assert old_itm in content, 'old_itm not found'
content = content.replace(old_itm, new_itm, 1)

old_yun = '{"code": "雲科-國管", "school": "雲林科技大學", "dept": "國際管理學士學位學程", "region": "中部", "total_stu": 104, "five_year": 0, "undergrad_day": 104, "undergrad_eve": 0, "grad": 0,'
new_yun = '{"code": "雲科-國管", "school": "雲林科技大學", "dept": "國際管理學士學位學程", "region": "中部", "total_stu": 104, "five_year": 0, "undergrad_day": 104, "undergrad_eve": 0, "grad": 0, "grad_detail": "統整於管院企管碩班", "grad_tooltip": "系所專注全英語學士班，研究所名額統整於管院國際企管碩班",'
assert old_yun in content, 'old_yun not found'
content = content.replace(old_yun, new_yun, 1)

old_ship = '{"code": "高科-航管", "school": "高雄科技大學", "dept": "航運管理系", "region": "南部", "total_stu": 595, "five_year": 0, "undergrad_day": 415, "undergrad_eve": 101, "grad": 79,'
new_ship = '{"code": "高科-航管", "school": "高雄科技大學", "dept": "航運管理系", "region": "南部", "total_stu": 595, "five_year": 0, "undergrad_day": 415, "undergrad_eve": 101, "grad": 79, "grad_detail": "在職41 · 日碩20 · 博士18", "grad_tooltip": "碩士在職專班 41人、日間碩士班 20人、博士班 18人",'
assert old_ship in content, 'old_ship not found'
content = content.replace(old_ship, new_ship, 1)

old_ib = '{"code": "高科-國企", "school": "高雄科技大學", "dept": "國際企業系", "region": "南部", "total_stu": 554, "five_year": 0, "undergrad_day": 251, "undergrad_eve": 190, "grad": 113,'
new_ib = '{"code": "高科-國企", "school": "高雄科技大學", "dept": "國際企業系", "region": "南部", "total_stu": 554, "five_year": 0, "undergrad_day": 251, "undergrad_eve": 190, "grad": 113, "grad_detail": "在職52 · 日碩30 · 博士30 · 產碩1", "grad_tooltip": "碩士在職專班 52人、日間碩士班 30人、博士班 30人、珠寶產碩延畢 1人",'
assert old_ib in content, 'old_ib not found'
content = content.replace(old_ib, new_ib, 1)

old_scm = '{"code": "高科-供應鏈", "school": "高雄科技大學", "dept": "供應鏈管理系", "region": "南部", "total_stu": 306, "five_year": 0, "undergrad_day": 240, "undergrad_eve": 40, "grad": 26,'
new_scm = '{"code": "高科-供應鏈", "school": "高雄科技大學", "dept": "供應鏈管理系", "region": "南部", "total_stu": 306, "five_year": 0, "undergrad_day": 240, "undergrad_eve": 40, "grad": 26, "grad_detail": "日碩17 · 在職9", "grad_tooltip": "日間碩士班 17人、碩士在職專班 9人",'
assert old_scm in content, 'old_scm not found'
content = content.replace(old_scm, new_scm, 1)

# 2. Update table rendering
old_td = '<td class="p-3 lg:p-3.5 text-right font-mono text-slate-600 whitespace-nowrap min-w-[75px]">${item.grad > 0 ? item.grad : \'0\'}</td>'
new_td = '''<td class="p-3 lg:p-3.5 text-right font-mono text-slate-600 whitespace-nowrap min-w-[105px]" title="${item.grad_tooltip || ''}">
                            <span class="font-bold text-slate-900">${item.grad > 0 ? item.grad : '0'}</span>
                            ${item.grad_detail ? `<span class="text-[10px] text-slate-500 block font-normal tracking-tight leading-tight mt-0.5">(${item.grad_detail})</span>` : ''}
                        </td>'''
assert old_td in content, 'old_td not found'
content = content.replace(old_td, new_td, 1)

# 3. Update card rendering
old_card = '''                                    <div class="flex justify-between py-0.5 border-b border-slate-100">
                                        <span class="text-slate-400">碩博士在學:</span>
                                        <span class="font-mono font-semibold text-slate-800">${item.grad > 0 ? item.grad + '人' : '0人'}</span>
                                    </div>'''
new_card = '''                                    <div class="flex justify-between items-start py-0.5 border-b border-slate-100">
                                        <span class="text-slate-400">碩博士在學:</span>
                                        <div class="text-right">
                                            <span class="font-mono font-semibold text-slate-800">${item.grad > 0 ? item.grad + '人' : '0人'}</span>
                                            ${item.grad_detail ? `<span class="text-[10px] text-slate-500 block font-normal leading-tight mt-0.5">(${item.grad_detail})</span>` : ''}
                                        </div>
                                    </div>'''
assert old_card in content, 'old_card not found'
content = content.replace(old_card, new_card, 1)

with open('/Users/chenchunchih/Downloads/校務資料/interactive_dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Successfully updated interactive_dashboard.html!')
