from collections import defaultdict
# -*- coding: utf-8 -*-
"""
產出「國立高雄科技大學 國際企業系(所) 碩博士班歷年完整校務數據庫.xlsx」
完全對齊教育部大專校院校務資訊公開平台 (MOE UDB) 官方原始報表
"""

import os
import csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

CACHE_DIR = '/Users/chenchunchih/Downloads/校務資料/moe_udb_cache'
OUTPUT_XLSX = '/Users/chenchunchih/Downloads/校務資料/高科大國企系_碩博士班歷年完整校務數據庫.xlsx'

# 建立活頁簿
wb = openpyxl.Workbook()
# 移除預設 sheet
wb.remove(wb.active)

# 樣式定義
FONT_FAMILY = '微軟正黑體'
font_title = Font(name=FONT_FAMILY, size=16, bold=True, color='1E3A8A')
font_subtitle = Font(name=FONT_FAMILY, size=11, italic=True, color='475569')
font_section = Font(name=FONT_FAMILY, size=12, bold=True, color='0F172A')
font_header = Font(name=FONT_FAMILY, size=11, bold=True, color='FFFFFF')
font_data = Font(name=FONT_FAMILY, size=10, color='1E293B')
font_bold = Font(name=FONT_FAMILY, size=10, bold=True, color='0F172A')
font_kpi_num = Font(name=FONT_FAMILY, size=18, bold=True, color='1E3A8A')
font_kpi_label = Font(name=FONT_FAMILY, size=9, bold=True, color='64748B')
font_note = Font(name=FONT_FAMILY, size=9, italic=True, color='64748B')

fill_header_navy = PatternFill(start_color='1E3A8A', end_color='1E3A8A', fill_type='solid')
fill_header_slate = PatternFill(start_color='334155', end_color='334155', fill_type='solid')
fill_header_blue = PatternFill(start_color='2563EB', end_color='2563EB', fill_type='solid')
fill_zebra = PatternFill(start_color='F8FAFC', end_color='F8FAFC', fill_type='solid')
fill_highlight = PatternFill(start_color='FEF3C7', end_color='FEF3C7', fill_type='solid')
fill_kpi_bg = PatternFill(start_color='EFF6FF', end_color='EFF6FF', fill_type='solid')

border_thin = Border(
    left=Side(style='thin', color='E2E8F0'),
    right=Side(style='thin', color='E2E8F0'),
    top=Side(style='thin', color='E2E8F0'),
    bottom=Side(style='thin', color='E2E8F0')
)
border_header = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='medium', color='1E3A8A'),
    bottom=Side(style='medium', color='1E3A8A')
)

align_center = Alignment(horizontal='center', vertical='center')
align_left = Alignment(horizontal='left', vertical='center')
align_right = Alignment(horizontal='right', vertical='center')
align_wrap_left = Alignment(horizontal='left', vertical='center', wrap_text=True)

def style_table(ws, start_row, end_row, num_cols, num_formats=None):
    for col in range(1, num_cols + 1):
        cell_h = ws.cell(row=start_row, column=col)
        cell_h.font = font_header
        cell_h.fill = fill_header_navy
        cell_h.alignment = align_center
        cell_h.border = border_header
    ws.row_dimensions[start_row].height = 26

    for r in range(start_row + 1, end_row + 1):
        ws.row_dimensions[r].height = 22
        is_even = (r % 2 == 0)
        for col in range(1, num_cols + 1):
            cell = ws.cell(row=r, column=col)
            cell.font = font_data
            cell.border = border_thin
            if is_even:
                cell.fill = fill_zebra
            if num_formats and col in num_formats:
                cell.number_format = num_formats[col]
                cell.alignment = align_right
            elif isinstance(cell.value, (int, float)):
                cell.alignment = align_right
            else:
                if col == 1 or col == 2 or '學年' in str(cell.value):
                    cell.alignment = align_center

def autofit_cols(ws, max_len_dict=None):
    for col in ws.columns:
        col_letter = get_column_letter(col[0].column)
        max_len = 0
        for cell in col:
            val = str(cell.value or '')
            # 中文字算 2 個字元
            val_len = sum(2 if ord(c) > 127 else 1 for c in val)
            if val_len > max_len:
                max_len = val_len
        if max_len_dict and col_letter in max_len_dict:
            ws.column_dimensions[col_letter].width = max_len_dict[col_letter]
        else:
            ws.column_dimensions[col_letter].width = min(max(max_len + 3, 10), 50)

# =========================================================================
# Sheet 1: 00_決策總覽與關鍵情報
# =========================================================================
ws0 = wb.create_sheet(title='00_決策總覽與關鍵情報')
ws0.views.sheetView[0].showGridLines = True

ws0['A1'] = '國立高雄科技大學 國際企業系(所) 碩博士班完整校務數據決策總覽'
ws0['A1'].font = font_title
ws0['A2'] = '資料來源：教育部大專校院校務資訊公開平台 (MOE UDB) 學生類與教職類官方報表 (106 ~ 114 學年度)'
ws0['A2'].font = font_subtitle

# KPI 卡片列
kpis = [
    ('114 博士在學生', '30 人', '外國生 9 人 (30.0%)'),
    ('114 日碩在學生', '30 人', '實註 15 人 (註冊率 85.0%)'),
    ('114 碩專在學生', '52 人', '實註 26 人 (註冊率 100%)'),
    ('專任師資總數', '13 位', '教授 8 / 副教 2 / 助教 3'),
    ('研究生生師比', '8.69', '113名研究生 / 13位專任')
]

col_start = 1
for label, val, sub in kpis:
    c_l = get_column_letter(col_start)
    c_r = get_column_letter(col_start + 1)
    ws0.merge_cells(f'{c_l}4:{c_r}4')
    ws0.merge_cells(f'{c_l}5:{c_r}5')
    ws0.merge_cells(f'{c_l}6:{c_r}6')
    
    ws0[f'{c_l}4'] = label
    ws0[f'{c_l}4'].font = font_kpi_label
    ws0[f'{c_l}4'].alignment = align_center
    ws0[f'{c_l}4'].fill = fill_kpi_bg
    
    ws0[f'{c_l}5'] = val
    ws0[f'{c_l}5'].font = font_kpi_num
    ws0[f'{c_l}5'].alignment = align_center
    ws0[f'{c_l}5'].fill = fill_kpi_bg
    
    ws0[f'{c_l}6'] = sub
    ws0[f'{c_l}6'].font = font_note
    ws0[f'{c_l}6'].alignment = align_center
    ws0[f'{c_l}6'].fill = fill_kpi_bg

    for r in range(4, 7):
        for c in range(col_start, col_start + 2):
            ws0.cell(row=r, column=c).border = border_thin
    col_start += 2

ws0['A8'] = '【高科大國企系 碩博士體系 114 學年度現況對照矩陣】'
ws0['A8'].font = font_section

headers_0 = ['學制班別', '日夜別', '核定名額(A)', '實註人數(C)', '境外外加(E)', '新生註冊率(%)', '在學學生數', '外國在學生', '外國生比率(%)', '專任師資(系)', '生師比', '官方佐證報表']
for c_idx, h in enumerate(headers_0, 1):
    ws0.cell(row=9, column=c_idx, value=h)

matrix_data = [
    ['博士班', '日間', 4, 3, 0, 0.7500, 30, 9, 0.3000, 13, 2.31, '教育部 UDB 學12-1, 學1-1, 學3-2, 教1-1'],
    ['碩士班 (日間碩士班)', '日間', 18, 15, 2, 0.8500, 30, 2, 0.0667, 13, 2.31, '教育部 UDB 學12-1, 學1-1, 學3-2, 教1-1'],
    ['碩士在職專班 (EMBA)', '在職', 26, 26, 0, 1.0000, 52, 0, 0.0000, 13, 4.00, '教育部 UDB 學12-1, 學1-1, 教1-1'],
    ['珠寶行銷產業碩士專班', '日間', 0, 0, 0, None, 1, 0, 0.0000, 13, 0.08, '教育部 UDB 學1-1 (歷史產碩留校生)'],
    ['碩博士研究生全體合計', '全體', 48, 44, 2, 0.9167, 113, 11, 0.0973, 13, 8.69, '教育部 UDB 全體研究生整合統計']
]

for r_idx, row in enumerate(matrix_data, 10):
    for c_idx, val in enumerate(row, 1):
        ws0.cell(row=r_idx, column=c_idx, value=val)

style_table(ws0, 9, 14, len(headers_0), {
    3: '#,##0', 4: '#,##0', 5: '#,##0', 6: '0.00%', 7: '#,##0', 8: '#,##0', 9: '0.00%', 10: '#,##0', 11: '0.00'
})

ws0['A16'] = '【高科大國企系 碩博士班 關鍵戰略情報分析】'
ws0['A16'].font = font_section

insights = [
    '1. 博士班結構高度依賴外國生：110~114學年度博士班外國學生佔比長期維持在 30%~38%（114學年度在學30人中有9名外國生），顯示其博士班生源極大比重由境外生支撐。',
    '2. 日間碩士班自112年谷底反彈：112學年度日間碩士班核定20人僅實註6人（註冊率崩跌至33.33%）；系所迅速於113~114主動調減名額至18人，114學年實註15人+外加2人，註冊率強勁回彈至85.00%。',
    '3. 碩士在職專班 (EMBA) 招生表現亮眼：114學年度核定26名全數滿招（實註26人，註冊率100%），在學人數達52人，展現大高雄經貿產業在職進修之剛性需求。',
    '4. 專任師資結構高度資深：系所專任教師13位，正教授達8位（佔比 61.5%），副教授2位，助理教授3位，無講師，全體師資具備極高指導能量與研究資歷。',
    '5. 休退學深水區剖析：112學年日碩與碩專曾出現較高退學潮（各有7人退學），主因集中於「逾期未註冊」與「休學逾期未復學」，顯示在職生與研究生工作壓力對就學穩定度之衝擊。',
    '6. 產業碩士專班完成歷史使命：過去開辦之「國際企業營運與理財」、「國際貴金屬與珠寶行銷」產碩專班已陸續畢業結案，114學年度僅餘珠寶專班1名延畢生。'
]

for idx, ins in enumerate(insights, 17):
    ws0.cell(row=idx, column=1, value=ins).font = font_data

autofit_cols(ws0, {'A': 22, 'B': 10, 'C': 12, 'D': 12, 'E': 12, 'F': 14, 'G': 12, 'H': 12, 'I': 14, 'J': 12, 'K': 10, 'L': 38})

# =========================================================================
# Sheet 2: 01_新生招生與註冊率消長 (學12-1)
# =========================================================================
ws1 = wb.create_sheet(title='01_新生招生與註冊率')
ws1.views.sheetView[0].showGridLines = True
ws1['A1'] = '國立高雄科技大學 國際企業系(所) 歷年碩博士班招生與註冊率消長 (107 ~ 114學年度)'
ws1['A1'].font = font_title
ws1['A2'] = '官方報表來源：教育部 UDB 學12-1「新生(含境外生)註冊率-以「系(所)」統計」'
ws1['A2'].font = font_subtitle

headers_1 = ['學年度', '系所名稱', '日夜別', '學制班別', '核定名額(A)', '保留入學(B)', '總量內實註(C)', '境外外加(E)', '新生註冊率(%)', '系所招生特色說明', '官方網址']
for c_idx, h in enumerate(headers_1, 1):
    ws1.cell(row=4, column=c_idx, value=h)

# 讀取學12-1數據
f_reg = os.path.join(CACHE_DIR, '學12-1.新生(含境外生)註冊率-以「系(所)」統計.csv')
rows_1 = []
with open(f_reg, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            if '碩士' in r['學制班別'] or '博士' in r['學制班別'] or '碩士' in r['系所名稱'] or '博士' in r['系所名稱']:
                yr = int(r['學年度'])
                name = r['系所名稱']
                dy = r['日間/進修']
                prog = r['學制班別']
                a = int(r['當學年度總量內核定新生招生名額(A)']) if r['當學年度總量內核定新生招生名額(A)'].isdigit() else 0
                b = int(r['當學年度新生保留入學資格人數(B)']) if r['當學年度新生保留入學資格人數(B)'].isdigit() else 0
                c = int(r['當學年度總量內新生招生核定名額之實際註冊人數(C)']) if r['當學年度總量內新生招生核定名額之實際註冊人數(C)'].isdigit() else 0
                e = int(r['當學年度各學系境外(新生)學生實際註冊人數 (E)']) if r['當學年度各學系境外(新生)學生實際註冊人數 (E)'].isdigit() else 0
                rate_str = r['當學年度新生註冊率(%)D=〔(C+E)/(A-B+E)〕＊100％'].strip()
                rate = float(rate_str) / 100.0 if rate_str.replace('.','',1).isdigit() else 0.0
                desc = r['當學年度系所招生特色說明'].strip()
                url = r['當學年度招生特色說明資訊網'].strip()
                rows_1.append([yr, name, dy, prog, a, b, c, e, rate, desc, url])

rows_1.sort(key=lambda x: (x[0], x[3]), reverse=True)
for r_idx, row in enumerate(rows_1, 5):
    for c_idx, val in enumerate(row, 1):
        ws1.cell(row=r_idx, column=c_idx, value=val)

style_table(ws1, 4, 4 + len(rows_1), len(headers_1), {
    1: '0', 5: '#,##0', 6: '#,##0', 7: '#,##0', 8: '#,##0', 9: '0.00%'
})
autofit_cols(ws1, {'A': 10, 'B': 22, 'C': 10, 'D': 14, 'E': 12, 'F': 12, 'G': 14, 'H': 12, 'I': 14, 'J': 45, 'K': 28})

# =========================================================================
# Sheet 3: 02_歷年在學學生與性別結構 (學1-1)
# =========================================================================
ws2 = wb.create_sheet(title='02_在學學生與性別結構')
ws2.views.sheetView[0].showGridLines = True
ws2['A1'] = '國立高雄科技大學 國際企業系(所) 歷年碩博士在學生與男女比例 (107 ~ 114學年度)'
ws2['A1'].font = font_title
ws2['A2'] = '官方報表來源：教育部 UDB 學1-1「正式學籍在學學生人數-以「系(所)」統計」'
ws2['A2'].font = font_subtitle

headers_2 = ['學年度', '系所名稱', '學制班別', '在學學生總數', '男性在學人數', '女性在學人數', '女性佔比(%)']
for c_idx, h in enumerate(headers_2, 1):
    ws2.cell(row=4, column=c_idx, value=h)

f_stu = os.path.join(CACHE_DIR, '學1-1.正式學籍在學學生人數-以「系(所)」統計.csv')
rows_2 = []
with open(f_stu, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            if '碩士' in r['學制班別'] or '博士' in r['學制班別']:
                yr = int(r['學年度'])
                name = r['系所名稱']
                prog = r['學制班別']
                tot = int(r['在學學生數小計']) if r['在學學生數小計'].isdigit() else 0
                m = int(r['在學學生數男']) if r['在學學生數男'].isdigit() else 0
                w = int(r['在學學生數女']) if r['在學學生數女'].isdigit() else 0
                pct = (w / tot) if tot > 0 else 0.0
                rows_2.append([yr, name, prog, tot, m, w, pct])

rows_2.sort(key=lambda x: (x[0], x[2]), reverse=True)
for r_idx, row in enumerate(rows_2, 5):
    for c_idx, val in enumerate(row, 1):
        ws2.cell(row=r_idx, column=c_idx, value=val)

style_table(ws2, 4, 4 + len(rows_2), len(headers_2), {
    1: '0', 4: '#,##0', 5: '#,##0', 6: '#,##0', 7: '0.00%'
})
autofit_cols(ws2, {'A': 10, 'B': 30, 'C': 16, 'D': 14, 'E': 14, 'F': 14, 'G': 14})

# =========================================================================
# Sheet 4: 03_外國研究生人數與佔比 (學3-2)
# =========================================================================
ws3 = wb.create_sheet(title='03_外國研究生人數與比率')
ws3.views.sheetView[0].showGridLines = True
ws3['A1'] = '國立高雄科技大學 國際企業系(所) 外國研究生人數與在學比率 (107 ~ 114學年度)'
ws3['A1'].font = font_title
ws3['A2'] = '官方報表來源：教育部 UDB 學3-2「外國學生數及其在學比率-以「系(所)」統計」'
ws3['A2'].font = font_subtitle

headers_3 = ['學年度', '系所名稱', '學制班別(日間)', '外國在學生總數', '外國男生數', '外國女生數', '外國學生在學比率(%)']
for c_idx, h in enumerate(headers_3, 1):
    ws3.cell(row=4, column=c_idx, value=h)

f_for = os.path.join(CACHE_DIR, '學3-2.外國學生數及其在學比率-以「系(所)」統計.csv')
rows_3 = []
with open(f_for, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            if '碩士' in r['學制班別(日間)'] or '博士' in r['學制班別(日間)']:
                yr = int(r['學年度'])
                name = r['系所名稱']
                prog = r['學制班別(日間)']
                tot = int(r['外國學生小計']) if r['外國學生小計'].isdigit() else 0
                m = int(r['外國學生數男']) if r['外國學生數男'].isdigit() else 0
                w = int(r['外國學生女']) if r['外國學生女'].isdigit() else 0
                rate_str = r['外國學生數之在學比率(%)'].strip()
                rate = float(rate_str) / 100.0 if rate_str.replace('.','',1).isdigit() else 0.0
                rows_3.append([yr, name, prog, tot, m, w, rate])

rows_3.sort(key=lambda x: (x[0], x[2]), reverse=True)
for r_idx, row in enumerate(rows_3, 5):
    for c_idx, val in enumerate(row, 1):
        ws3.cell(row=r_idx, column=c_idx, value=val)

style_table(ws3, 4, 4 + len(rows_3), len(headers_3), {
    1: '0', 4: '#,##0', 5: '#,##0', 6: '#,##0', 7: '0.00%'
})
autofit_cols(ws3, {'A': 10, 'B': 24, 'C': 16, 'D': 16, 'E': 14, 'F': 14, 'G': 20})

# =========================================================================
# Sheet 5: 04_歷年畢業生與論文公開 (學2-1 & 學2-4)
# =========================================================================
ws4 = wb.create_sheet(title='04_畢業生與論文資料')
ws4.views.sheetView[0].showGridLines = True
ws4['A1'] = '國立高雄科技大學 國際企業系(所) 歷年碩博士畢業人數與學位論文公開狀況'
ws4['A1'].font = font_title
ws4['A2'] = '官方報表來源：教育部 UDB 學2-1「畢業生數」與 學2-4「畢業碩、博士學位論文資料」'
ws4['A2'].font = font_subtitle

headers_4 = ['學年度', '系所名稱', '學制班別', '畢業生總數', '畢業男性', '畢業女性', '女性畢業比率(%)', '學位論文不公開件數']
for c_idx, h in enumerate(headers_4, 1):
    ws4.cell(row=4, column=c_idx, value=h)

# 讀取學2-4論文不公開
f_the = os.path.join(CACHE_DIR, '學2-4.畢業碩、博士學位論文資料-以「系(所)」統計.csv')
thesis_dict = {}
with open(f_the, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            key = (r['學年度'], r['學制班別'])
            thesis_dict[key] = float(r['學位論文不公開件數']) if r['學位論文不公開件數'] else 0.0

f_grad = os.path.join(CACHE_DIR, '學2-1.畢業生數及其取得輔系、雙主修資格人數-以「系(所)」統計.csv')
rows_4 = []
with open(f_grad, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            if '碩士' in r['學制班別'] or '博士' in r['學制班別']:
                yr = int(r['學年度'])
                name = r['系所名稱']
                prog = r['學制班別']
                tot = int(r['畢業生數小計']) if r['畢業生數小計'].isdigit() else 0
                m = int(r['畢業生數男']) if r['畢業生數男'].isdigit() else 0
                w = int(r['畢業生數女']) if r['畢業生數女'].isdigit() else 0
                pct = (w / tot) if tot > 0 else 0.0
                unpub = int(thesis_dict.get((str(yr), prog), 0))
                rows_4.append([yr, name, prog, tot, m, w, pct, unpub])

rows_4.sort(key=lambda x: (x[0], x[2]), reverse=True)
for r_idx, row in enumerate(rows_4, 5):
    for c_idx, val in enumerate(row, 1):
        ws4.cell(row=r_idx, column=c_idx, value=val)

style_table(ws4, 4, 4 + len(rows_4), len(headers_4), {
    1: '0', 4: '#,##0', 5: '#,##0', 6: '#,##0', 7: '0.00%', 8: '#,##0'
})
autofit_cols(ws4, {'A': 10, 'B': 30, 'C': 16, 'D': 14, 'E': 12, 'F': 12, 'G': 16, 'H': 18})

# =========================================================================
# Sheet 6: 05_休學分析與原因診斷 (學13-1)
# =========================================================================
ws5 = wb.create_sheet(title='05_休學人數與原因分析')
ws5.views.sheetView[0].showGridLines = True
ws5['A1'] = '國立高雄科技大學 國際企業系(所) 碩博士班休學人數與原因細項診斷 (111 ~ 113學年度)'
ws5['A1'].font = font_title
ws5['A2'] = '官方報表來源：教育部 UDB 學13-1「於學年底處於休學狀態之人數-以「系(所)」統計(111學年度起)」'
ws5['A2'].font = font_subtitle

headers_5 = ['學年度', '學期', '系所名稱', '學制班別', '性別', '在學學生數', '休學總人數', '休學率(%)', '工作需求', '志趣不合', '傷病', '經濟困難', '論文撰寫', '出國', '兵役', '其他原因']
for c_idx, h in enumerate(headers_5, 1):
    ws5.cell(row=4, column=c_idx, value=h)

f_susp = os.path.join(CACHE_DIR, '學13-1.於學年底處於休學狀態之人數-以「系(所)」統計(111學年度起).csv')
rows_5 = []
with open(f_susp, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            if '碩士' in r['學制班別'] or '博士' in r['學制班別']:
                yr = int(r['學年度'])
                sem = int(r.get('學期', '1')) if '學期' in r and r['學期'].isdigit() else 1
                name = r['系所名稱']
                prog = r['學制班別']
                gender = r['性別']
                tot = int(r['在學學生數']) if r['態度' if '態度' in r else '在學學生數'].isdigit() else 0
                susp = int(r['於學年底處於休學狀態之人數-總計']) if r['於學年底處於休學狀態之人數-總計'].isdigit() else 0
                rate = (susp / tot) if tot > 0 else 0.0
                work = int(r['於學年底處於休學狀態之人數-學生自請休學原因-工作']) if r['於學年底處於休學狀態之人數-學生自請休學原因-工作'].isdigit() else 0
                mismatch = int(r['於學年底處於休學狀態之人數-學生自請休學原因-就讀學校、科系不符期待']) if r['於學年底處於休學狀態之人數-學生自請休學原因-就讀學校、科系不符期待'].isdigit() else 0
                sick = int(r['於學年底處於休學狀態之人數-學生自請休學原因-傷病']) if r['於學年底處於休學狀態之人數-學生自請休學原因-傷病'].isdigit() else 0
                econ = int(r['於學年底處於休學狀態之人數-學生自請休學原因-經濟困難']) if r['於學年底處於休學狀態之人數-學生自請休學原因-經濟困難'].isdigit() else 0
                thesis = int(r['於學年底處於休學狀態之人數-學生自請休學原因-論文撰寫']) if r['於學年底處於休學狀態之人數-學生自請休學原因-論文撰寫'].isdigit() else 0
                abroad = int(r['於學年底處於休學狀態之人數-學生自請休學原因-出國']) if r['於學年底處於休學狀態之人數-學生自請休學原因-出國'].isdigit() else 0
                military = int(r['於學年底處於休學狀態之人數-學生自請休學原因-兵役']) if r['於學年底處於休學狀態之人數-學生自請休學原因-兵役'].isdigit() else 0
                other = int(r['於學年底處於休學狀態之人數-學生自請休學原因-其他']) if r['於學年底處於休學狀態之人數-學生自請休學原因-其他'].isdigit() else 0
                rows_5.append([yr, sem, name, prog, gender, tot, susp, rate, work, mismatch, sick, econ, thesis, abroad, military, other])

rows_5.sort(key=lambda x: (x[0], x[3], x[4]), reverse=True)
for r_idx, row in enumerate(rows_5, 5):
    for c_idx, val in enumerate(row, 1):
        ws5.cell(row=r_idx, column=c_idx, value=val)

style_table(ws5, 4, 4 + len(rows_5), len(headers_5), {
    1: '0', 2: '0', 6: '#,##0', 7: '#,##0', 8: '0.00%', 9: '#,##0', 10: '#,##0', 11: '#,##0', 12: '#,##0', 13: '#,##0', 14: '#,##0', 15: '#,##0', 16: '#,##0'
})
autofit_cols(ws5, {'A': 10, 'B': 8, 'C': 26, 'D': 16, 'E': 8, 'F': 12, 'G': 12, 'H': 12, 'I': 10, 'J': 10, 'K': 8, 'L': 10, 'M': 10, 'N': 8, 'O': 8, 'P': 10})

# =========================================================================
# Sheet 7: 06_退學分析與原因診斷 (學14-1)
# =========================================================================
ws6 = wb.create_sheet(title='06_退學人數與原因分析')
ws6.views.sheetView[0].showGridLines = True
ws6['A1'] = '國立高雄科技大學 國際企業系(所) 碩博士班退學人數與原因細項診斷 (111 ~ 113學年度)'
ws6['A1'].font = font_title
ws6['A2'] = '官方報表來源：教育部 UDB 學14-1「退學人數-以「系(所)」統計(111學年度起)」'
ws6['A2'].font = font_subtitle

headers_6 = ['學年度', '學期', '系所名稱', '學制班別', '性別', '在學學生數', '退學總人數', '退學率(%)', '逾期未註冊', '休學逾期未復學', '志趣不合', '工作需求', '傷病', '經濟困難', '成績不佳曠課']
for c_idx, h in enumerate(headers_6, 1):
    ws6.cell(row=4, column=c_idx, value=h)

f_drop = os.path.join(CACHE_DIR, '學14-1.退學人數-以「系(所)」統計(111學年度起).csv')
rows_6 = []
with open(f_drop, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            if '碩士' in r['學制班別'] or '博士' in r['學制班別']:
                yr = int(r['學年度'])
                sem = int(r.get('學期', '1')) if '學期' in r and r['學期'].isdigit() else 1
                name = r['系所名稱']
                prog = r['學制班別']
                gender = r['性別']
                tot = int(r['在學學生數']) if r['在學學生數'].isdigit() else 0
                drop = int(r['學期間退學人數-總計']) if r['學期間退學人數-總計'].isdigit() else 0
                rate = (drop / tot) if tot > 0 else 0.0
                unreg = int(r['學期間退學人數-學校勒令退學-因逾期未註冊']) if r['學期間退學人數-學校勒令退學-因逾期未註冊'].isdigit() else 0
                unreturn = int(r['學期間退學人數-學校勒令退學-休學逾期未復學']) if r['學期間退學人數-學校勒令退學-休學逾期未復學'].isdigit() else 0
                mismatch = int(r['學期間退學人數-學生自請退學-就讀學校、科系不符期待']) if r['學期間退學人數-學生自請退學-就讀學校、科系不符期待'].isdigit() else 0
                work = int(r['學期間退學人數-學生自請退學-工作']) if r['學期間退學人數-學生自請退學-工作'].isdigit() else 0
                sick = int(r['學期間退學人數-學生自請退學-傷病']) if r['學期間退學人數-學生自請退學-傷病'].isdigit() else 0
                econ = int(r['學期間退學人數-學生自請退學-經濟困難']) if r['學期間退學人數-學生自請退學-經濟困難'].isdigit() else 0
                grades = int(r['學期間退學人數-學校勒令退學-成績不佳或曠課時數過多']) if r['學期間退學人數-學校勒令退學-成績不佳或曠課時數過多'].isdigit() else 0
                rows_6.append([yr, sem, name, prog, gender, tot, drop, rate, unreg, unreturn, mismatch, work, sick, econ, grades])

rows_6.sort(key=lambda x: (x[0], x[3], x[4]), reverse=True)
for r_idx, row in enumerate(rows_6, 5):
    for c_idx, val in enumerate(row, 1):
        ws6.cell(row=r_idx, column=c_idx, value=val)

style_table(ws6, 4, 4 + len(rows_6), len(headers_6), {
    1: '0', 2: '0', 6: '#,##0', 7: '#,##0', 8: '0.00%', 9: '#,##0', 10: '#,##0', 11: '#,##0', 12: '#,##0', 13: '#,##0', 14: '#,##0', 15: '#,##0'
})
autofit_cols(ws6, {'A': 10, 'B': 8, 'C': 26, 'D': 16, 'E': 8, 'F': 12, 'G': 12, 'H': 12, 'I': 12, 'J': 14, 'K': 10, 'L': 10, 'M': 8, 'N': 10, 'O': 14})

# =========================================================================
# Sheet 8: 07_專任師資與生師比 (教1-1)
# =========================================================================
ws7 = wb.create_sheet(title='07_專任師資與生師比')
ws7.views.sheetView[0].showGridLines = True
ws7['A1'] = '國立高雄科技大學 國際企業系 專任師資結構與碩博生師比消長 (107 ~ 114學年度)'
ws7['A1'].font = font_title
ws7['A2'] = '官方報表來源：教育部 UDB 教1-1「專任教師數」與 學1-1「在學學生數」'
ws7['A2'].font = font_subtitle

headers_7 = ['學年度', '專任教師總數', '正教授', '副教授', '助理教授', '講師', '男教師', '女教師', '碩博在學生總數', '系所全體在學生', '研究生生師比', '全系總生師比']
for c_idx, h in enumerate(headers_7, 1):
    ws7.cell(row=4, column=c_idx, value=h)

# 整理歷年碩博在學與全體在學
grad_tot_by_yr = defaultdict(int)
all_tot_by_yr = defaultdict(int)
with open(f_stu, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['系所代碼'] == '04141023':
            yr = int(r['學年度'])
            tot = int(r['在學學生數小計']) if r['在學學生數小計'].isdigit() else 0
            all_tot_by_yr[yr] += tot
            if '碩士' in r['學制班別'] or '博士' in r['學制班別']:
                grad_tot_by_yr[yr] += tot

f_tea = os.path.join(CACHE_DIR, '教1-1.專任教師數-以「系(所)」統計.csv')
rows_7 = []
with open(f_tea, 'r', encoding='utf-8-sig', errors='ignore') as fp:
    reader = csv.DictReader(fp)
    for r in reader:
        if r['學校統計處代碼'] == '0053' and r['單位代碼'] == '04141023':
            yr = int(r['學年度'])
            tot = int(r['專任教師數-教師總數總計'])
            m = int(r['專任教師數-教師總數男'])
            w = int(r['專任教師數-教師總數女'])
            prof = int(r['專任教師數-教授男']) + int(r['專任教師數-教授女'])
            assoc = int(r['專任教師數-副教授男']) + int(r['專任教師數-副教授女'])
            asst = int(r['專任教師數-助理教授男']) + int(r['專任教師數-助理教授女'])
            lect = int(r['專任教師數-講師男']) + int(r['專任教師數-講師女'])
            grad_stu = grad_tot_by_yr[yr]
            all_stu = all_tot_by_yr[yr]
            r_grad = (grad_stu / tot) if tot > 0 else 0.0
            r_all = (all_stu / tot) if tot > 0 else 0.0
            rows_7.append([yr, tot, prof, assoc, asst, lect, m, w, grad_stu, all_stu, r_grad, r_all])

rows_7.sort(key=lambda x: x[0], reverse=True)
for r_idx, row in enumerate(rows_7, 5):
    for c_idx, val in enumerate(row, 1):
        ws7.cell(row=r_idx, column=c_idx, value=val)

style_table(ws7, 4, 4 + len(rows_7), len(headers_7), {
    1: '0', 2: '#,##0', 3: '#,##0', 4: '#,##0', 5: '#,##0', 6: '#,##0', 7: '#,##0', 8: '#,##0', 9: '#,##0', 10: '#,##0', 11: '0.00', 12: '0.00'
})
autofit_cols(ws7, {'A': 10, 'B': 14, 'C': 10, 'D': 10, 'E': 12, 'F': 8, 'G': 10, 'H': 10, 'I': 16, 'J': 16, 'K': 14, 'L': 14})

# =========================================================================
# Sheet 9: 08_國立四強國貿商管研所對照
# =========================================================================
ws8 = wb.create_sheet(title='08_國立四強國貿研所對比')
ws8.views.sheetView[0].showGridLines = True
ws8['A1'] = '全國國立四大商管體系 國際貿易/企業/管理系所 114學年度碩博士體系對照矩陣'
ws8['A1'].font = font_title
ws8['A2'] = '比較對象：高科大國企系、北商大國商系、中科大國貿系(所)、雲科大國管學程'
ws8['A2'].font = font_subtitle

headers_8 = ['學校名稱', '系所名稱', '獨立碩士班', '碩士在職專班', '獨立博士班', '114碩博在學人數', '114碩博核定名額', '114碩博實註人數', '114碩博註冊率(%)', '系專任師資', '研究生生師比', '學制特色說明']
for c_idx, h in enumerate(headers_8, 1):
    ws8.cell(row=4, column=c_idx, value=h)

comp_rows = [
    ['國立高雄科技大學', '國際企業系', '有 (日碩18名)', '有 (碩專26名)', '有 (博士4名)', 113, 48, 44, 0.9167, 13, 8.69, '技職唯一完整貫通學士、碩士、碩專、博士之國企系，博士班境外生比例達30%'],
    ['國立臺北商業大學', '國際商務系', '有 (日碩15名)', '有 (碩專18名)', '無', 28, 33, 31, 0.9394, 23, 1.22, '位處台北首都圈，日碩與碩專規模精緻，生師比極低(1.22)，師資研究量能充沛'],
    ['國立臺中科技大學', '國際貿易與經營系', '無 (統整於商學院碩士班)', '無 (統整於商學院高階EMBA)', '無', 0, 0, 0, None, 21, 0.00, '純技職學士貫通體系(四技、二技、五專、進修部)，無獨立系所碩博班，碩士名額由商學院統整'],
    ['國立雲林科技大學', '國際管理學士學位學程', '無 (統整於管院國際企管碩班)', '無', '無', 0, 0, 0, None, 3, 0.00, '聚焦全英語日間學士班(含外加境外生)，無獨立系所碩博士班']
]

for r_idx, row in enumerate(comp_rows, 5):
    for c_idx, val in enumerate(row, 1):
        ws8.cell(row=r_idx, column=c_idx, value=val)

style_table(ws8, 4, 4 + len(comp_rows), len(headers_8), {
    6: '#,##0', 7: '#,##0', 8: '#,##0', 9: '0.00%', 10: '#,##0', 11: '0.00'
})
autofit_cols(ws8, {'A': 20, 'B': 22, 'C': 16, 'D': 16, 'E': 14, 'F': 16, 'G': 16, 'H': 16, 'I': 16, 'J': 12, 'K': 14, 'L': 45})

# 儲存 Excel
wb.save(OUTPUT_XLSX)
print(f"✅ 成功產出: {OUTPUT_XLSX} ({os.path.getsize(OUTPUT_XLSX)} bytes)")

# 同步複製到 raw_data 與 dist/raw_data
import shutil
shutil.copy2(OUTPUT_XLSX, '/Users/chenchunchih/Downloads/校務資料/raw_data/高科大國企系_碩博士班歷年完整校務數據庫.xlsx')
shutil.copy2(OUTPUT_XLSX, '/Users/chenchunchih/Downloads/校務資料/dist/raw_data/高科大國企系_碩博士班歷年完整校務數據庫.xlsx')
print("✅ 已同步至 raw_data 與 dist/raw_data 資料夾")
