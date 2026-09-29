import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

# Set font for Chinese display
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang TC', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

# 1. Load Data
df_tc = pd.read_csv('/Users/chenchunchih/Downloads/校務資料/104_taichung_ai_enriched_jobs.csv')
df_tp = pd.read_csv('/Users/chenchunchih/Downloads/校務資料/104_taipei_ai_noncoding_jobs.csv')

print(f"Loaded Taichung: {len(df_tc)} rows")
print(f"Loaded Taipei: {len(df_tp)} rows")

# Harmonize Taichung
df_tc['region'] = '台中'
df_tc['is_taipei'] = 0
df_tc['min_monthly_salary'] = pd.to_numeric(df_tc['monthly_min'], errors='coerce')
df_tc['max_monthly_salary'] = pd.to_numeric(df_tc['monthly_max'], errors='coerce')
df_tc['is_negotiable'] = df_tc['min_monthly_salary'].apply(lambda x: 1 if pd.isna(x) or x <= 0 else 0)

# Standardize requirement_type in Taichung
def clean_req(x):
    s = str(x)
    if '必備' in s or '具備' in s:
        return '必備條件'
    elif '加分' in s or '優先' in s:
        return '加分/優先'
    else:
        return '工作內容應用'
df_tc['requirement_type'] = df_tc['requirement_type'].apply(clean_req)

# Standardize industry in Taichung
def clean_ind(x):
    s = str(x)
    if '生技' in s or '醫療' in s:
        return '生技/醫療保健'
    elif '電商' in s or '零售' in s:
        return '電子商務/數位零售'
    elif '製造' in s or '精密' in s:
        return '傳統製造/精密工業'
    elif '補教' in s or '文教' in s:
        return '文教/補教培訓'
    elif '廣告' in s or '行銷' in s:
        return '廣告行銷/公關顧問'
    elif '軟體' in s or '網路' in s or '資訊' in s:
        return '資訊科技/軟體網路'
    else:
        return '其他服務/工商貿易'
df_tc['target_industry'] = df_tc['target_industry'].apply(clean_ind)

# Compute missing flags in Taichung
def get_flags(row):
    text = (str(row['job_name']) + ' ' + str(row['description_snippet'])).lower()
    has_lang = 1 if any(w in text for w in ['英文', '英語', 'toeic', '多益', '外語', '外銷', '日文', '日語']) else 0
    has_trade = 1 if any(w in text for w in ['國貿', '貿易', '海外業務', '跨境', '進出口', '報關', '船務', 'rfq', 'incoterms']) else 0
    has_auto = 1 if any(w in text for w in ['自動化', '流程優化', 'api', 'make', 'zapier', 'n8n', 'webhook', '串接']) else 0
    return pd.Series([has_lang, has_trade, has_auto])

df_tc[['has_foreign_language', 'has_international_trade', 'has_workflow_automation']] = df_tc.apply(get_flags, axis=1)

# Harmonize Taipei
df_tp['region'] = '雙北'
df_tp['is_taipei'] = 1
df_tp['min_monthly_salary'] = pd.to_numeric(df_tp['min_monthly_salary'], errors='coerce')
df_tp['max_monthly_salary'] = pd.to_numeric(df_tp['max_monthly_salary'], errors='coerce')
df_tp['is_negotiable'] = df_tp['min_monthly_salary'].apply(lambda x: 1 if pd.isna(x) or x <= 0 else 0)
df_tp['requirement_type'] = df_tp['requirement_type'].apply(clean_req)
df_tp['target_industry'] = df_tp['target_industry'].apply(clean_ind)

# Select standardized columns
cols = [
    'job_id', 'job_name', 'company', 'region', 'is_taipei', 'target_industry',
    'salary_raw', 'is_negotiable', 'min_monthly_salary', 'max_monthly_salary',
    'requirement_type', 'ai_tools', 'has_foreign_language', 'has_international_trade',
    'has_workflow_automation', 'description_snippet'
]

df_merged = pd.concat([df_tc[cols], df_tp[cols]], ignore_index=True)
df_merged.to_csv('/Users/chenchunchih/Downloads/校務資料/104_north_central_ai_jobs_merged.csv', index=False, encoding='utf-8-sig')
print(f"Merged dataset saved: {len(df_merged)} rows.")

# 2. Key Descriptive Statistics
print("\n" + "="*50)
print("--- 雙北 vs 台中 非工程 AI 職缺總體指標 ---")
print("="*50)

# Disclosed salary subset
disclosed = df_merged[df_merged['is_negotiable'] == 0].copy()

stats_summary = []
for reg in ['雙北', '台中']:
    sub_all = df_merged[df_merged['region'] == reg]
    sub_disc = disclosed[disclosed['region'] == reg]
    
    n_total = len(sub_all)
    n_disc = len(sub_disc)
    pct_nego = (n_total - n_disc) / n_total * 100
    
    mean_sal = sub_disc['min_monthly_salary'].mean()
    med_sal = sub_disc['min_monthly_salary'].median()
    q25 = sub_disc['min_monthly_salary'].quantile(0.25)
    q75 = sub_disc['min_monthly_salary'].quantile(0.75)
    
    pct_req_mandatory = (sub_all['requirement_type'] == '必備條件').mean() * 100
    pct_req_bonus = (sub_all['requirement_type'] == '加分/優先').mean() * 100
    pct_req_work = (sub_all['requirement_type'] == '工作內容應用').mean() * 100
    
    pct_lang = sub_all['has_foreign_language'].mean() * 100
    pct_trade = sub_all['has_international_trade'].mean() * 100
    pct_auto = sub_all['has_workflow_automation'].mean() * 100
    
    stats_summary.append({
        '地區': reg,
        '總樣本數': n_total,
        '公開薪資樣本數': n_disc,
        '面議比例(%)': f"{pct_nego:.1f}%",
        '起薪平均值': f"${mean_sal:,.0f}",
        '起薪中位數': f"${med_sal:,.0f}",
        '起薪IQR(25%-75%)': f"${q25:,.0f} ~ ${q75:,.0f}",
        'AI必備條件佔比(%)': f"{pct_req_mandatory:.1f}%",
        '外語要求佔比(%)': f"{pct_lang:.1f}%",
        '貿易/跨境佔比(%)': f"{pct_trade:.1f}%",
        '自動化/API佔比(%)': f"{pct_auto:.1f}%"
    })

df_stats = pd.DataFrame(stats_summary)
print(df_stats.to_string(index=False))

# 3. Industry Comparison
print("\n" + "="*50)
print("--- 產業結構分佈比較 (%) ---")
print("="*50)
ind_comp = pd.crosstab(df_merged['target_industry'], df_merged['region'], normalize='columns') * 100
print(ind_comp.round(1))

# 4. Salary Tiers Comparison
print("\n" + "="*50)
print("--- 起薪級距分佈比較 (公開薪資職缺, %) ---")
print("="*50)
bins = [0, 30000, 35000, 40000, 50000, 999999]
labels = ['< 3.0萬', '3.0萬 ~ 3.5萬', '3.5萬 ~ 4.0萬', '4.0萬 ~ 5.0萬', '5.0萬以上']
disclosed['salary_tier'] = pd.cut(disclosed['min_monthly_salary'], bins=bins, labels=labels, right=False)
tier_comp = pd.crosstab(disclosed['salary_tier'], disclosed['region'], normalize='columns') * 100
print(tier_comp.round(1))

# 5. Econometric OLS Regression Model
print("\n" + "="*50)
print("--- 計量經濟學多元迴歸模型 (OLS) ---")
print("應變數: 起薪 (min_monthly_salary, 元/月)")
print("="*50)

# Create dummy variables for regression
reg_df = disclosed.copy()
reg_df['ai_mandatory'] = (reg_df['requirement_type'] == '必備條件').astype(int)
reg_df['ai_bonus'] = (reg_df['requirement_type'] == '加分/優先').astype(int)

# Clean industry names for formula
reg_df['industry_clean'] = reg_df['target_industry'].apply(
    lambda x: '軟體網路' if '軟體' in str(x) or '資訊' in str(x)
    else ('生技醫療' if '生技' in str(x)
    else ('電商零售' if '電商' in str(x)
    else ('傳統製造' if '製造' in str(x)
    else ('文教補教' if '文教' in str(x)
    else ('廣告行銷' if '廣告' in str(x) else '其他服務')))))
)

model = smf.ols(
    'min_monthly_salary ~ is_taipei + ai_mandatory + ai_bonus + has_foreign_language + has_international_trade + has_workflow_automation + C(industry_clean, Treatment(reference="傳統製造"))',
    data=reg_df
).fit()

print(model.summary())

# 6. Generate 4-Panel Comparative Visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 11), dpi=300)

# Panel A: Salary Boxplot Comparison
sns.boxplot(x='region', y='min_monthly_salary', hue='region', data=disclosed, ax=axes[0, 0], palette=['#7c3aed', '#059669'], width=0.45, showfliers=False)
# Overlay mean points
means = disclosed.groupby('region')['min_monthly_salary'].mean()
axes[0, 0].scatter([0, 1], [means.get('雙北', np.nan), means.get('台中', np.nan)], color='red', s=70, zorder=5, label='平均值 (Mean)')
axes[0, 0].set_title('A. 雙北 vs 台中 非工程 AI 職缺起薪分佈 (盒鬚圖)', fontsize=12, fontweight='bold', pad=10)
axes[0, 0].set_ylabel('月薪起薪 (新台幣元)', fontsize=10)
axes[0, 0].set_xlabel('')
axes[0, 0].legend()
axes[0, 0].grid(axis='y', linestyle='--', alpha=0.5)

# Add text labels on boxplot
for idx, reg in enumerate(['雙北', '台中']):
    if reg in disclosed['region'].values:
        med = disclosed[disclosed['region'] == reg]['min_monthly_salary'].median()
        avg = disclosed[disclosed['region'] == reg]['min_monthly_salary'].mean()
        axes[0, 0].text(idx, med + 800, f"中位: ${med:,.0f}\n平均: ${avg:,.0f}", ha='center', fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))

# Panel B: Industry Distribution Comparison
ind_pct = ind_comp.loc[['資訊科技/軟體網路', '廣告行銷/公關顧問', '電子商務/數位零售', '傳統製造/精密工業', '生技/醫療保健', '文教/補教培訓']]
ind_pct.plot(kind='barh', ax=axes[0, 1], color=['#7c3aed', '#059669'], width=0.7)
axes[0, 1].set_title('B. 雙北 vs 台中 核心產業結構分佈 (%)', fontsize=12, fontweight='bold', pad=10)
axes[0, 1].set_xlabel('佔該地區職缺比例 (%)', fontsize=10)
axes[0, 1].set_ylabel('')
axes[0, 1].legend(['雙北 (N=1,974)', '台中 (N=631)'])
axes[0, 1].grid(axis='x', linestyle='--', alpha=0.5)

# Panel C: Requirement Type & Skill Premium Comparison
req_data = pd.DataFrame({
    '雙北': [
        (df_merged[df_merged['region'] == '雙北']['requirement_type'] == '必備條件').mean() * 100,
        (df_merged[df_merged['region'] == '雙北']['has_foreign_language']).mean() * 100,
        (df_merged[df_merged['region'] == '雙北']['has_workflow_automation']).mean() * 100,
        (df_merged[df_merged['region'] == '雙北']['has_international_trade']).mean() * 100
    ],
    '台中': [
        (df_merged[df_merged['region'] == '台中']['requirement_type'] == '必備條件').mean() * 100,
        (df_merged[df_merged['region'] == '台中']['has_foreign_language']).mean() * 100,
        (df_merged[df_merged['region'] == '台中']['has_workflow_automation']).mean() * 100,
        (df_merged[df_merged['region'] == '台中']['has_international_trade']).mean() * 100
    ]
}, index=['AI列為必備條件', '外語能力要求', '流程自動化/API', '國貿/跨境業務'])

req_data.plot(kind='bar', ax=axes[1, 0], color=['#7c3aed', '#059669'], width=0.65)
axes[1, 0].set_title('C. 職能要求強度與進階技能滲透率 (%)', fontsize=12, fontweight='bold', pad=10)
axes[1, 0].set_ylabel('佔比 (%)', fontsize=10)
axes[1, 0].set_xticklabels(req_data.index, rotation=15, ha='right', fontsize=9)
axes[1, 0].legend(['雙北', '台中'])
axes[1, 0].grid(axis='y', linestyle='--', alpha=0.5)

# Panel D: Regression Premium Coefficients (Bar plot with error bars)
reg_coefs = pd.Series({
    '雙北地域淨溢價': model.params['is_taipei'],
    'AI列為必備溢價': model.params['ai_mandatory'],
    '外語能力溢價': model.params['has_foreign_language'],
    '國貿/跨境溢價': model.params['has_international_trade'],
    '流程自動化溢價': model.params['has_workflow_automation']
})
reg_errs = pd.Series({
    '雙北地域淨溢價': model.bse['is_taipei'],
    'AI列為必備溢價': model.bse['ai_mandatory'],
    '外語能力溢價': model.bse['has_foreign_language'],
    '國貿/跨境溢價': model.bse['has_international_trade'],
    '流程自動化溢價': model.bse['has_workflow_automation']
})

bars = axes[1, 1].bar(reg_coefs.index, reg_coefs.values, yerr=reg_errs.values, capsize=5, color=['#4338ca', '#7c3aed', '#0284c7', '#059669', '#d97706'], alpha=0.85)
axes[1, 1].set_title('D. 計量迴歸控制變數後之「淨薪資溢價」(新台幣元/月)', fontsize=12, fontweight='bold', pad=10)
axes[1, 1].set_ylabel('薪資淨增額 (元/月)', fontsize=10)
axes[1, 1].set_xticklabels(reg_coefs.index, rotation=20, ha='right', fontsize=9)
axes[1, 1].axhline(0, color='black', linewidth=0.8, linestyle='--')
axes[1, 1].grid(axis='y', linestyle='--', alpha=0.5)

for bar in bars:
    yval = bar.get_height()
    axes[1, 1].text(bar.get_x() + bar.get_width()/2.0, yval + 200, f"+${yval:,.0f}", ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
chart_path = '/Users/chenchunchih/Downloads/校務資料/taipei_vs_taichung_ai_jobs_comparison.png'
plt.savefig(chart_path, dpi=300)
print(f"\nComparative Chart saved: {chart_path}")
