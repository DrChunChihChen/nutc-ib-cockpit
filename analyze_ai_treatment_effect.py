import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'PingFang TC', 'Heiti TC', 'sans-serif']
plt.rcParams['axes.unicode_minus'] = False

def run_treatment_analysis():
    treat_path = '/Users/chenchunchih/Downloads/校務資料/104_north_central_ai_jobs_merged.csv'
    ctrl_path = '/Users/chenchunchih/Downloads/校務資料/104_control_non_ai_jobs.csv'
    
    df_treat = pd.read_csv(treat_path)
    df_ctrl = pd.read_csv(ctrl_path)
    
    print(f"Loaded Treatment (AI jobs): {len(df_treat)} rows")
    print(f"Loaded Control (Non-AI jobs): {len(df_ctrl)} rows")
    
    # Standardize treatment columns
    df_treat['is_ai_job'] = 1
    if 'category' not in df_treat.columns and 'job_category' in df_treat.columns:
        df_treat['category'] = df_treat['job_category']
        
    common_cols = [
        'job_id', 'job_name', 'company', 'region', 'target_industry',
        'salary_raw', 'is_negotiable', 'min_monthly_salary', 'max_monthly_salary',
        'is_ai_job', 'requirement_type', 'ai_tools',
        'has_foreign_language', 'has_international_trade', 'has_workflow_automation',
        'description_snippet'
    ]
    
    # Ensure all columns exist
    for c in common_cols:
        if c not in df_treat.columns:
            df_treat[c] = np.nan
        if c not in df_ctrl.columns:
            df_ctrl[c] = np.nan
            
    df_combined = pd.concat([df_treat[common_cols], df_ctrl[common_cols]], ignore_index=True)
    df_combined['is_taipei'] = df_combined['region'].apply(lambda x: 1 if '雙北' in str(x) or '台北' in str(x) else 0)
    df_combined['min_monthly_salary'] = pd.to_numeric(df_combined['min_monthly_salary'], errors='coerce')
    df_combined['max_monthly_salary'] = pd.to_numeric(df_combined['max_monthly_salary'], errors='coerce')
    df_combined['is_negotiable'] = df_combined['min_monthly_salary'].apply(lambda x: 1 if pd.isna(x) or x <= 0 else 0)
    
    combined_path = '/Users/chenchunchih/Downloads/校務資料/104_ai_vs_non_ai_combined.csv'
    df_combined.to_csv(combined_path, index=False, encoding='utf-8-sig')
    print(f"Combined Dataset Saved ({len(df_combined)} rows) to {combined_path}\n")
    
    # 1. Descriptive Comparison
    print("="*60)
    print("【第一部分：整體樣本與薪資統計對比】")
    print("="*60)
    
    disc = df_combined[df_combined['is_negotiable'] == 0].copy()
    
    for label, is_ai in [('傳統無 AI 職缺 (對照組)', 0), ('提及 AI 職缺 (實驗組)', 1)]:
        sub_all = df_combined[df_combined['is_ai_job'] == is_ai]
        sub_disc = disc[disc['is_ai_job'] == is_ai]
        
        n_all = len(sub_all)
        n_disc = len(sub_disc)
        pct_nego = (n_all - n_disc) / n_all * 100
        
        sal_mean = sub_disc['min_monthly_salary'].mean()
        sal_std = sub_disc['min_monthly_salary'].std()
        sal_med = sub_disc['min_monthly_salary'].median()
        q25 = sub_disc['min_monthly_salary'].quantile(0.25)
        q75 = sub_disc['min_monthly_salary'].quantile(0.75)
        pct_50k = (sub_disc['min_monthly_salary'] >= 50000).mean() * 100
        
        print(f"--- {label} ---")
        print(f"  總樣本數: {n_all:,} 筆 | 公開薪資數: {n_disc:,} 筆 (面議率: {pct_nego:.1f}%)")
        print(f"  起薪平均值: ${sal_mean:,.0f} (標準差: ${sal_std:,.0f})")
        print(f"  起薪中位數: ${sal_med:,.0f} (IQR: ${q25:,.0f} ~ ${q75:,.0f})")
        print(f"  高薪起薪 (≥5萬/月) 佔比: {pct_50k:.1f}%\n")
        
    # Statistical Hypothesis Testing
    sal_ctrl = disc[disc['is_ai_job'] == 0]['min_monthly_salary']
    sal_treat = disc[disc['is_ai_job'] == 1]['min_monthly_salary']
    
    t_stat, p_val_t = stats.ttest_ind(sal_treat, sal_ctrl, equal_var=False)
    u_stat, p_val_u = stats.mannwhitneyu(sal_treat, sal_ctrl, alternative='two-sided')
    
    diff_mean = sal_treat.mean() - sal_ctrl.mean()
    diff_pct = (sal_treat.mean() - sal_ctrl.mean()) / sal_ctrl.mean() * 100
    diff_med = sal_treat.median() - sal_ctrl.median()
    
    print(f"【雙樣本假設檢定結果】:")
    print(f"  起薪平均差異: +${diff_mean:,.0f} (+{diff_pct:.2f}%)")
    print(f"  起薪中位差異: +${diff_med:,.0f}")
    print(f"  Welch's t-test: t = {t_stat:.4f}, p = {p_val_t:.4e} {'(顯著差異)' if p_val_t < 0.05 else '(不顯著)'}")
    print(f"  Mann-Whitney U: U = {u_stat:.1f}, p = {p_val_u:.4e} {'(顯著差異)' if p_val_u < 0.05 else '(不顯著)'}\n")
    
    # 2. Breakdown by Target Industry
    print("="*60)
    print("【第二部分：各產業 AI 起薪溢價矩陣】")
    print("="*60)
    
    ind_rows = []
    for ind in disc['target_industry'].dropna().unique():
        sub_c = disc[(disc['target_industry'] == ind) & (disc['is_ai_job'] == 0)]['min_monthly_salary']
        sub_t = disc[(disc['target_industry'] == ind) & (disc['is_ai_job'] == 1)]['min_monthly_salary']
        if len(sub_c) >= 15 and len(sub_t) >= 15:
            med_c = sub_c.median()
            med_t = sub_t.median()
            mean_c = sub_c.mean()
            mean_t = sub_t.mean()
            diff_m = mean_t - mean_c
            diff_p = (mean_t - mean_c) / mean_c * 100
            ind_rows.append({
                '產業類別': ind,
                '無AI起薪中位': f"${med_c:,.0f}",
                'AI起薪中位': f"${med_t:,.0f}",
                '起薪平均差額': f"+${diff_m:,.0f}",
                'AI溢價率(%)': f"+{diff_p:.1f}%",
                '樣本數(對照/實驗)': f"{len(sub_c)} / {len(sub_t)}"
            })
            
    df_ind_comp = pd.DataFrame(ind_rows).sort_values(by='AI溢價率(%)', ascending=False)
    print(df_ind_comp.to_string(index=False))
    
    # 3. Econometric OLS Regression on Salary
    print("\n" + "="*60)
    print("【第三部分：計量特徵薪資迴歸模型 (Hedonic OLS Regression)】")
    print("應變數: 起薪 (min_monthly_salary, 元/月)")
    print("="*60)
    
    # Clean industry
    disc['industry_clean'] = disc['target_industry'].apply(
        lambda x: '軟體網路' if '軟體' in str(x) or '資訊' in str(x)
        else ('生技醫療' if '生技' in str(x)
        else ('電商零售' if '電商' in str(x)
        else ('傳統製造' if '製造' in str(x)
        else ('文教補教' if '文教' in str(x)
        else ('廣告行銷' if '廣告' in str(x) else '其他服務')))))
    )
    
    model_ols = smf.ols(
        'min_monthly_salary ~ is_ai_job + is_taipei + has_foreign_language + has_international_trade + has_workflow_automation + C(industry_clean, Treatment(reference="傳統製造"))',
        data=disc
    ).fit()
    
    print(model_ols.summary())
    
    # 4. Logistic Regression on Negotiable Probability
    print("\n" + "="*60)
    print("【第四部分：開出『薪資面議(高階職位)』機率 Logit 迴歸】")
    print("應變數: 是否為面議 (is_negotiable: 1=面議, 0=公開)")
    print("="*60)
    
    df_combined['industry_clean'] = df_combined['target_industry'].apply(
        lambda x: '軟體網路' if '軟體' in str(x) or '資訊' in str(x)
        else ('生技醫療' if '生技' in str(x)
        else ('電商零售' if '電商' in str(x)
        else ('傳統製造' if '製造' in str(x)
        else ('文教補教' if '文教' in str(x)
        else ('廣告行銷' if '廣告' in str(x) else '其他服務')))))
    )
    
    model_logit = smf.logit(
        'is_negotiable ~ is_ai_job + is_taipei + has_foreign_language + has_international_trade + C(industry_clean, Treatment(reference="傳統製造"))',
        data=df_combined
    ).fit()
    print(model_logit.summary())
    
    # 5. Generate Publication-Quality 4-Panel Visualization
    fig, axes = plt.subplots(2, 2, figsize=(14, 11), dpi=300)
    
    # Panel A: KDE Density Curve Comparison
    sns.kdeplot(sal_ctrl, ax=axes[0, 0], fill=True, color='#64748b', alpha=0.35, linewidth=2, label=f'傳統無 AI 職缺 (中位: ${sal_ctrl.median():,.0f})')
    sns.kdeplot(sal_treat, ax=axes[0, 0], fill=True, color='#7c3aed', alpha=0.45, linewidth=2.5, label=f'提及 AI 職缺 (中位: ${sal_treat.median():,.0f})')
    axes[0, 0].axvline(sal_ctrl.median(), color='#64748b', linestyle='--', linewidth=1.5)
    axes[0, 0].axvline(sal_treat.median(), color='#7c3aed', linestyle='--', linewidth=1.5)
    axes[0, 0].set_xlim(25000, 75000)
    axes[0, 0].set_title('A. 起薪機率密度分佈對比 (KDE 核密度估計)', fontsize=12, fontweight='bold', pad=10)
    axes[0, 0].set_xlabel('月薪起薪 (新台幣元)', fontsize=10)
    axes[0, 0].set_ylabel('機率密度', fontsize=10)
    axes[0, 0].legend(loc='upper right', fontsize=9)
    axes[0, 0].grid(axis='x', linestyle='--', alpha=0.5)
    
    # Panel B: Industry Wage Premium Horizontal Bar Chart
    ind_plot_df = pd.DataFrame(ind_rows)
    ind_plot_df['prem_num'] = ind_plot_df['AI溢價率(%)'].apply(lambda x: float(x.replace('%', '').replace('+', '')))
    ind_plot_df = ind_plot_df.sort_values(by='prem_num', ascending=True)
    
    colors = ['#059669' if p > 5 else '#3b82f6' for p in ind_plot_df['prem_num']]
    bars = axes[0, 1].barh(ind_plot_df['產業類別'], ind_plot_df['prem_num'], color=colors, height=0.6)
    axes[0, 1].set_title('B. 各主要產業 AI 薪資溢價率 (%)', fontsize=12, fontweight='bold', pad=10)
    axes[0, 1].set_xlabel('起薪平均溢價百分比 (%)', fontsize=10)
    axes[0, 1].grid(axis='x', linestyle='--', alpha=0.5)
    
    for bar in bars:
        w = bar.get_width()
        axes[0, 1].text(w + 0.3, bar.get_y() + bar.get_height()/2.0, f"+{w:.1f}%", va='center', fontsize=9, fontweight='bold')
        
    # Panel C: 4-Subgroup Boxplot (Region x AI)
    disc['subgroup'] = disc.apply(lambda r: f"{r['region']} · {'AI賦能' if r['is_ai_job']==1 else '傳統無AI'}", axis=1)
    subgroup_order = ['台中 · 傳統無AI', '台中 · AI賦能', '雙北 · 傳統無AI', '雙北 · AI賦能']
    
    palette = ['#94a3b8', '#10b981', '#cbd5e1', '#7c3aed']
    sns.boxplot(x='subgroup', y='min_monthly_salary', data=disc, order=subgroup_order, ax=axes[1, 0], palette=palette, width=0.5, showfliers=False)
    axes[1, 0].set_title('C. 地域 × AI 賦能 四象限起薪級距對比 (盒鬚圖)', fontsize=12, fontweight='bold', pad=10)
    axes[1, 0].set_ylabel('月薪起薪 (新台幣元)', fontsize=10)
    axes[1, 0].set_xlabel('')
    axes[1, 0].set_xticklabels(subgroup_order, rotation=15, ha='right', fontsize=9)
    axes[1, 0].grid(axis='y', linestyle='--', alpha=0.5)
    
    for idx, g in enumerate(subgroup_order):
        sub_g = disc[disc['subgroup'] == g]['min_monthly_salary']
        if len(sub_g) > 0:
            axes[1, 0].text(idx, sub_g.median() + 800, f"中位: ${sub_g.median():,.0f}", ha='center', fontsize=8.5, fontweight='bold', bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8))
            
    # Panel D: Regression Forest Plot (Coefficients with 95% CI)
    coef_labels = {
        'is_ai_job': 'AI 職缺處置效應 (ATE)',
        'is_taipei': '雙北地域效應',
        'has_workflow_automation': '流程自動化 / API',
        'has_foreign_language': '外語溝通能力',
        'has_international_trade': '國貿 / 跨境業務'
    }
    
    coef_vals = [model_ols.params[k] for k in coef_labels.keys()]
    err_vals = [model_ols.bse[k] * 1.96 for k in coef_labels.keys()] # 95% CI
    y_pos = np.arange(len(coef_labels))
    
    axes[1, 1].errorbar(coef_vals, y_pos, xerr=err_vals, fmt='o', color='#4338ca', ecolor='#6366f1', elinewidth=2.5, capsize=5, markersize=7)
    axes[1, 1].axvline(0, color='red', linestyle='--', linewidth=1)
    axes[1, 1].set_yticks(y_pos)
    axes[1, 1].set_yticklabels(coef_labels.values(), fontsize=9.5)
    axes[1, 1].set_title('D. 迴歸模型變數之淨薪資影響 (95% 信賴區間森林圖)', fontsize=12, fontweight='bold', pad=10)
    axes[1, 1].set_xlabel('月薪淨影響金額 (新台幣元/月)', fontsize=10)
    axes[1, 1].grid(axis='x', linestyle='--', alpha=0.5)
    
    for idx, (val, err) in enumerate(zip(coef_vals, err_vals)):
        axes[1, 1].text(val, idx + 0.25, f"{'+' if val>0 else ''}${val:,.0f}", ha='center', fontsize=9, fontweight='bold', color='#1e1b4b')
        
    plt.tight_layout()
    chart_out = '/Users/chenchunchih/Downloads/校務資料/ai_vs_non_ai_salary_comparison.png'
    plt.savefig(chart_out, dpi=300)
    print(f"\nPublication-Grade Comparative Chart saved to: {chart_out}")

if __name__ == '__main__':
    run_treatment_analysis()
