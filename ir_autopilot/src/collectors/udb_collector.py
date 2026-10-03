"""
UDB Collector: 負責解析並索引教育部大專校院校務資訊公開平台 (UDB) 8 大系所級報表。
"""

import os
import glob
import pandas as pd
from typing import Dict, List, Optional, Any

class UDBCollector:
    def __init__(self, cache_dir: str = "moe_udb_cache"):
        self.cache_dir = cache_dir
        self.tables: Dict[str, pd.DataFrame] = {}
        self._load_cache()

    def _load_cache(self):
        """讀取本機快取之 8 大 UDB 報表"""
        file_mapping = {
            "students": "學1-1.正式學籍在學學生人數-以「系(所)」統計.csv",
            "enrollment": "學12-1.新生(含境外生)註冊率-以「系(所)」統計.csv",
            "suspension": "學13-1.於學年底處於休學狀態之人數-以「系(所)」統計(111學年度起).csv",
            "dropout": "學14-1.退學人數-以「系(所)」統計(111學年度起).csv",
            "faculty": "教1-1.專任教師數-以「系(所)」統計.csv",
            "graduates": "學2-1.畢業生數及其取得輔系、雙主修資格人數-以「系(所)」統計.csv",
            "foreign": "學3-2.外國學生數及其在學比率-以「系(所)」統計.csv",
            "theses": "學2-4.畢業碩、博士學位論文資料-以「系(所)」統計.csv",
        }

        for key, fname in file_mapping.items():
            fpath = os.path.join(self.cache_dir, fname)
            if os.path.exists(fpath):
                try:
                    df = pd.read_csv(fpath, low_memory=False)
                    # 統一學校代碼與系所代碼為字串
                    if "學校統計處代碼" in df.columns:
                        df["學校統計處代碼"] = df["學校統計處代碼"].astype(str).str.zfill(4)
                    if "系所代碼" in df.columns:
                        df["系所代碼"] = df["系所代碼"].astype(str).str.zfill(8)
                    if "單位代碼" in df.columns:
                        df["單位代碼"] = df["單位代碼"].astype(str).str.zfill(8)
                    self.tables[key] = df
                except Exception as e:
                    print(f"Warning: Failed to load {fpath}: {e}")

    def get_department_udb_profile(self, school_name: str, dept_name: str, dept_code: Optional[str] = None) -> Dict[str, Any]:
        """
        取得特定系所的完整 UDB 指標快照
        """
        profile: Dict[str, Any] = {
            "school_name": school_name,
            "dept_name": dept_name,
            "dept_code": dept_code or "",
            "latest_year": 113,
            "students_total": 0,
            "freshmen_capacity": 0,
            "freshmen_registered": 0,
            "enrollment_rate": 100.0,
            "enrollment_history": [],
            "dropout_count": 0,
            "dropout_rate": 0.0,
            "suspension_count": 0,
            "suspension_rate": 0.0,
            "faculty_count": 1,
            "faculty_ratio": 0.0,
            "foreign_count": 0,
            "foreign_ratio": 0.0,
            "graduates_count": 0
        }

        # 1. 學生數 (學1-1)
        if "students" in self.tables:
            df = self.tables["students"]
            mask = df["學校名稱"].astype(str).str.contains(school_name[:4]) & (df["系所名稱"] == dept_name)
            sub = df[mask]
            if not sub.empty:
                max_year = sub["學年度"].max()
                latest_sub = sub[sub["學年度"] == max_year]
                profile["latest_year"] = int(max_year)
                # 累加各學制在學人數
                if "在學學生數小計" in latest_sub.columns:
                    val = pd.to_numeric(latest_sub["在學學生數小計"], errors="coerce").fillna(0).sum()
                    profile["students_total"] = int(val)
                if not profile["dept_code"] and "系所代碼" in latest_sub.columns:
                    profile["dept_code"] = str(latest_sub["系所代碼"].iloc[0])

        # 2. 註冊率 (學12-1)
        if "enrollment" in self.tables:
            df = self.tables["enrollment"]
            mask = df["學校名稱"].astype(str).str.contains(school_name[:4]) & (df["系所名稱"] == dept_name)
            sub = df[mask]
            if not sub.empty:
                # 優先抓純日間部四技或五專
                day_sub = sub[sub["日間/進修"].astype(str).str.contains("日")]
                target_sub = day_sub if not day_sub.empty else sub
                
                # 歷年註冊率歷史
                years = sorted(target_sub["學年度"].unique())
                history = []
                for y in years:
                    y_df = target_sub[target_sub["學年度"] == y]
                    rate_col = [c for c in y_df.columns if "註冊率" in c]
                    cap_col = [c for c in y_df.columns if "核定新生" in c]
                    reg_col = [c for c in y_df.columns if "實際註冊" in c]
                    
                    r_val = pd.to_numeric(y_df[rate_col[0]], errors="coerce").mean() if rate_col else 100.0
                    c_val = pd.to_numeric(y_df[cap_col[0]], errors="coerce").sum() if cap_col else 0
                    reg_val = pd.to_numeric(y_df[reg_col[0]], errors="coerce").sum() if reg_col else 0
                    
                    history.append({
                        "year": int(y),
                        "rate": round(float(r_val), 2),
                        "capacity": int(c_val),
                        "registered": int(reg_val)
                    })
                profile["enrollment_history"] = history
                if history:
                    latest_h = history[-1]
                    profile["enrollment_rate"] = latest_h["rate"]
                    profile["freshmen_capacity"] = latest_h["capacity"]
                    profile["freshmen_registered"] = latest_h["registered"]

        # 3. 退學人數 (學14-1)
        if "dropout" in self.tables:
            df = self.tables["dropout"]
            mask = df["學校名稱"].astype(str).str.contains(school_name[:4]) & (df["系所名稱"] == dept_name)
            sub = df[mask]
            if not sub.empty:
                max_year = sub["學年度"].max()
                y_sub = sub[sub["學年度"] == max_year]
                cnt_col = [c for c in y_sub.columns if "退學人數-總計" in c or "退學人數" in c]
                if cnt_col:
                    d_cnt = pd.to_numeric(y_sub[cnt_col[0]], errors="coerce").fillna(0).sum()
                    profile["dropout_count"] = int(d_cnt)
                    if profile["students_total"] > 0:
                        profile["dropout_rate"] = round((d_cnt / profile["students_total"]) * 100, 2)

        # 4. 休學人數 (學13-1)
        if "suspension" in self.tables:
            df = self.tables["suspension"]
            mask = df["學校名稱"].astype(str).str.contains(school_name[:4]) & (df["系所名稱"] == dept_name)
            sub = df[mask]
            if not sub.empty:
                max_year = sub["學年度"].max()
                y_sub = sub[sub["學年度"] == max_year]
                cnt_col = [c for c in y_sub.columns if "休學狀態之人數-總計" in c or "休學人數" in c]
                if cnt_col:
                    s_cnt = pd.to_numeric(y_sub[cnt_col[0]], errors="coerce").fillna(0).sum()
                    profile["suspension_count"] = int(s_cnt)
                    if profile["students_total"] > 0:
                        profile["suspension_rate"] = round((s_cnt / profile["students_total"]) * 100, 2)

        # 5. 專任教師數 (教1-1)
        if "faculty" in self.tables:
            df = self.tables["faculty"]
            mask = df["學校名稱"].astype(str).str.contains(school_name[:4]) & (df["單位名稱"].astype(str).str.contains(dept_name[:4]))
            sub = df[mask]
            if not sub.empty:
                max_year = sub["學年度"].max()
                y_sub = sub[sub["學年度"] == max_year]
                f_col = [c for c in y_sub.columns if "教師總數總計" in c or "專任教師數" in c]
                if f_col:
                    f_cnt = pd.to_numeric(y_sub[f_col[0]], errors="coerce").fillna(0).sum()
                    profile["faculty_count"] = max(1, int(f_cnt))
                    if profile["students_total"] > 0:
                        profile["faculty_ratio"] = round(profile["students_total"] / profile["faculty_count"], 1)

        # 6. 外國學生數 (學3-2)
        if "foreign" in self.tables:
            df = self.tables["foreign"]
            mask = df["學校名稱"].astype(str).str.contains(school_name[:4]) & (df["系所名稱"].astype(str).str.contains(dept_name[:4]))
            sub = df[mask]
            if not sub.empty:
                max_year = sub["學年度"].max()
                y_sub = sub[sub["學年度"] == max_year]
                fo_col = [c for c in y_sub.columns if "外國學生小計" in c or "外國學生數" in c]
                if fo_col:
                    fo_cnt = pd.to_numeric(y_sub[fo_col[0]], errors="coerce").fillna(0).sum()
                    profile["foreign_count"] = int(fo_cnt)
                    if profile["students_total"] > 0:
                        profile["foreign_ratio"] = round((fo_cnt / profile["students_total"]) * 100, 2)

        return profile
