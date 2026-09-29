# -*- coding: utf-8 -*-
"""
com.tw 21 校系頁面批次處理引擎 (含 Base64 提取、Apple Vision OCR 辨識與流向分析)
目標系所：
- 高科大國企 (105044, 105045, 105046)
- 高科大航運 (105075, 105076)
- 北商國商   (114004, 114005)
學年度：113, 114, 115
"""

import os
import sys
import re
import io
import json
import base64
import hashlib
import subprocess
import pandas as pd
from bs4 import BeautifulSoup
from PIL import Image

OCR_BIN = "/tmp/batch_ocr"
TMP_IMG_DIR = "/tmp/com_tw_ocr_imgs"
os.makedirs(TMP_IMG_DIR, exist_ok=True)

# 知名常數圖片 Hash 字典 (免 OCR 秒配對)
KNOWN_STATUS_HASHES = {
    "b3def82759d391758c4c90175e8d2a20": "正取",
}

DEPT_NAMES = {
    "105044": "國立高雄科技大學 國際企業系(一)",
    "105045": "國立高雄科技大學 國際企業系(二)",
    "105046": "國立高雄科技大學 國際企業系(三)",
    "105075": "國立高雄科技大學 航運管理系(一)",
    "105076": "國立高雄科技大學 航運管理系(二)",
    "114004": "國立臺北商業大學 國際商務系(一)",
    "114005": "國立臺北商業大學 國際商務系(二)",
}

def ensure_ocr_bin():
    if not os.path.exists(OCR_BIN):
        swift_code = r'''
import Cocoa
import Vision

func ocr(path: String) -> String {
    guard let image = NSImage(contentsOfFile: path),
          let cgImage = image.cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        return ""
    }
    var result = ""
    let request = VNRecognizeTextRequest { req, _ in
        guard let obs = req.results as? [VNRecognizedTextObservation] else { return }
        result = obs.compactMap { $0.topCandidates(1).first?.string }.joined()
    }
    request.recognitionLanguages = ["zh-Hant", "en-US"]
    request.recognitionLevel = .accurate
    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])
    try? handler.perform([request])
    return result
}

for arg in CommandLine.arguments.dropFirst() {
    print("\(arg)|||\\(ocr(path: arg))")
}
'''
        with open("/tmp/batch_ocr.swift", "w", encoding="utf-8") as f:
            f.write(swift_code)
        subprocess.run(["swiftc", "-O", "/tmp/batch_ocr.swift", "-o", OCR_BIN], check=True)

def run_batch_ocr(image_paths):
    """執行本機 Apple Vision OCR 辨識多張圖片"""
    if not image_paths:
        return {}
    results = {}
    chunk_size = 50
    for i in range(0, len(image_paths), chunk_size):
        chunk = image_paths[i:i+chunk_size]
        p = subprocess.run([OCR_BIN] + chunk, capture_output=True, text=True)
        for line in p.stdout.strip().split("\n"):
            if "|||" in line:
                fpath, text = line.split("|||", 1)
                results[fpath] = text.strip()
    return results

def process_single_html(html_str, dept_code, year, img_hash_cache, ocr_tasks):
    soup = BeautifulSoup(html_str, "html.parser")
    page_title = soup.title.string if soup.title else ""
    dept_desc = DEPT_NAMES.get(dept_code, page_title)

    # 尋找考生表格
    target_table = None
    for t in soup.find_all("table"):
        txt = t.get_text()
        if "准考證號碼" in txt and "校系名稱" in txt:
            target_table = t
            break

    if not target_table:
        return []

    rows = target_table.find_all("tr")
    candidates = []
    current_cand = None

    for r in rows:
        cells = r.find_all(["td", "th"])
        if len(cells) < 3:
            continue
        row_text = r.get_text(separator=" ", strip=True)
        imgs = r.find_all("img")
        b64_imgs = [img for img in imgs if img.get("src", "").startswith("data:image/png;base64,")]

        # 檢查是否為新考生起始列：通常含有 3~4 個 Base64 圖檔 (准考證、姓名第1字、姓名第2字、錄取狀態)
        has_id_img = any("check_" in a.get("href", "") for a in r.find_all("a")) or len(b64_imgs) >= 2

        if has_id_img and ("正取" in row_text or "備取" in row_text or len(b64_imgs) >= 3):
            if current_cand:
                candidates.append(current_cand)

            # 提取圖片並指派 OCR / Hash 任務
            status_token = None
            exam_no_token = None
            name_first_token = None
            name_last_token = None

            # 解析准考證號 (通常是第 1 或第 2 個含有寬度特徵的圖片)
            # 在 com.tw 中：
            # td scope=row 裡面常有錄取狀態與准考證
            for img in b64_imgs:
                src = img["src"]
                b64_data = src.split(",", 1)[1]
                md5 = hashlib.md5(b64_data.encode()).hexdigest()
                h = int(img.get("height", 0) or 0)
                w = int(img.get("width", 0) or 0)

                # 錄取狀態圖 (height=16, leftred / leftgreen)
                if img.parent and ("leftred" in img.parent.get("class", []) or "leftgreen" in img.parent.get("class", [])):
                    status_token = md5
                    if md5 not in img_hash_cache and md5 not in KNOWN_STATUS_HASHES:
                        fpath = os.path.join(TMP_IMG_DIR, f"{md5}.png")
                        if not os.path.exists(fpath):
                            with open(fpath, "wb") as f:
                                f.write(base64.b64decode(b64_data))
                        ocr_tasks[md5] = (fpath, False)

                # 准考證號圖 (寬度長、無星號)
                elif img.find_next_sibling("a") and "check_" in img.find_next_sibling("a").get("href", ""):
                    exam_no_token = md5
                    if md5 not in img_hash_cache:
                        fpath = os.path.join(TMP_IMG_DIR, f"{md5}.png")
                        if not os.path.exists(fpath):
                            with open(fpath, "wb") as f:
                                f.write(base64.b64decode(b64_data))
                        ocr_tasks[md5] = (fpath, False)

                # 姓名中文字形圖 (通常位於含有 '*' 文字的 td 內部)
                elif "*" in row_text:
                    if not name_first_token:
                        name_first_token = md5
                    else:
                        name_last_token = md5
                    if md5 not in img_hash_cache:
                        fpath = os.path.join(TMP_IMG_DIR, f"{md5}_scaled.png")
                        if not os.path.exists(fpath):
                            raw_data = base64.b64decode(b64_data)
                            im = Image.open(io.BytesIO(raw_data)).convert("RGBA")
                            bg = Image.new("RGBA", (im.width + 40, im.height + 40), (255, 255, 255, 255))
                            bg.paste(im, (20, 20), im)
                            bg = bg.convert("L")
                            bg = bg.resize((bg.width * 4, bg.height * 4), Image.Resampling.LANCZOS)
                            bg.save(fpath)
                        ocr_tasks[md5] = (fpath, True)

            current_cand = {
                "學年度": year,
                "系所代碼": dept_code,
                "系所名稱": dept_desc,
                "status_hash": status_token,
                "exam_hash": exam_no_token,
                "name_first_hash": name_first_token,
                "name_last_hash": name_last_token,
                "本校系狀態": "正取" if "正取" in row_text else "備取",
                "最終分發學校": None,
                "最終分發系所": None,
                "去向分類": "未分發/放棄",
                "錄取志願清單": []
            }

        # 志願列解析
        if current_cand:
            has_putdep = ("putdep1.png" in str(r)) or ("分發錄取" in row_text)
            depts = re.findall(r'[\u4e00-\u9fa5A-Za-z0-9()（）]{4,}(?:大學|學院|科大)[\u4e00-\u9fa5A-Za-z0-9()（）]{3,}(?:系|所|學士學位學程)', row_text)
            for d in depts:
                clean_d = d.strip()
                if clean_d not in [x["系所"] for x in current_cand["錄取志願清單"]]:
                    is_enrolled = has_putdep and (clean_d in row_text)
                    current_cand["錄取志願清單"].append({
                        "系所": clean_d,
                        "分發": is_enrolled
                    })
                    if is_enrolled:
                        current_cand["最終分發系所"] = clean_d
                        # 提煉學校名稱
                        m_sch = re.search(r'([\u4e00-\u9fa5]+(?:大學|學院|科大))', clean_d)
                        current_cand["最終分發學校"] = m_sch.group(1) if m_sch else clean_d

                        # 分類
                        target_kw = "高雄科技" if "高雄科技" in dept_desc else ("臺北商業" if "臺北商業" in dept_desc else "")
                        if target_kw and target_kw in clean_d:
                            current_cand["去向分類"] = "原校系/本校留任"
                        else:
                            current_cand["去向分類"] = "其他學校錄取"

    if current_cand:
        candidates.append(current_cand)

    return candidates

def parse_bundle_json(json_path, output_excel, output_csv):
    ensure_ocr_bin()
    print(f"📖 讀取頁面打包檔案: {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        bundle = json.load(f)

    print(f"共包含 {len(bundle)} 個頁面，開始前置分析與 OCR 特徵提取...")

    img_hash_cache = dict(KNOWN_STATUS_HASHES)
    ocr_tasks = {} # md5 -> (filepath, is_chinese)
    all_raw_candidates = []

    for key, html_content in bundle.items():
        # key 格式: {dept_code}_{year}
        parts = key.split("_")
        dept_code = parts[0]
        year = parts[1] if len(parts) > 1 else "115"

        cands = process_single_html(html_content, dept_code, year, img_hash_cache, ocr_tasks)
        all_raw_candidates.extend(cands)
        print(f"  [✓] 已解析 {dept_code} ({year}學年度): {len(cands)} 位考生")

    # 執行批次 OCR
    pending_fpaths = [info[0] for md5, info in ocr_tasks.items() if md5 not in img_hash_cache]
    print(f"啟動 Apple Vision OCR 辨識，需辨識影像數: {len(pending_fpaths)} 張...")
    ocr_results = run_batch_ocr(pending_fpaths)

    for md5, (fpath, is_chinese) in ocr_tasks.items():
        if fpath in ocr_results:
            text = ocr_results[fpath]
            img_hash_cache[md5] = text

    # 組裝最終結構化明細
    final_rows = []
    for idx, c in enumerate(all_raw_candidates, 1):
        exam_no = img_hash_cache.get(c["exam_hash"], "")
        first_c = img_hash_cache.get(c["name_first_hash"], "")
        last_c = img_hash_cache.get(c["name_last_hash"], "")

        if first_c and last_c:
            cand_name = f"{first_c}*{last_c}"
        elif first_c:
            cand_name = f"{first_c}*"
        elif last_c:
            cand_name = f"*{last_c}"
        else:
            cand_name = "—"

        status_text = img_hash_cache.get(c["status_hash"], c["本校系狀態"])
        offers_str = "; ".join([x["系所"] for x in c["錄取志願清單"]])

        final_rows.append({
            "序號": idx,
            "學年度": c["學年度"],
            "系所代碼": c["系所代碼"],
            "系所名稱": c["系所名稱"],
            "准考證號": exam_no if exam_no else "—",
            "考生姓名": cand_name,
            "本系錄取狀態": status_text if status_text else c["本校系狀態"],
            "最終分發學校": c["最終分發學校"] if c["最終分發學校"] else "—",
            "最終分發系所": c["最終分發系所"] if c["最終分發系所"] else "—",
            "去向分類": c["去向分類"],
            "二階錄取校系數": len(c["錄取志願清單"]),
            "全部錄取校系": offers_str if offers_str else "—"
        })

    df_all = pd.DataFrame(final_rows)
    print(f"🎉 資料庫建置完成，總考生筆數: {len(df_all)} 筆")

    # 輸出 CSV
    df_all.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"已儲存 CSV: {output_csv}")

    # 輸出多工作表 Excel
    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        df_all.to_excel(writer, sheet_name="全量考生流向明細", index=False)

        # 彙整工作表 1：各系歷年指標統計
        summary_rows = []
        for (sch, yr), group in df_all.groupby(["系所名稱", "學年度"]):
            total = len(group)
            mains = len(group[group["本系錄取狀態"].str.contains("正取", na=False)])
            reserves = total - mains
            enrolled = len(group[group["去向分類"] == "原校系/本校留任"])
            poached = len(group[group["去向分類"] == "其他學校錄取"])
            unplaced = len(group[group["去向分類"] == "未分發/放棄"])

            summary_rows.append({
                "系所名稱": sch,
                "學年度": yr,
                "榜單總人數": total,
                "正取人數": mains,
                "備取人數": reserves,
                "最終留任報到數": enrolled,
                "被他校搶走數": poached,
                "未分發或放棄數": unplaced,
                "留任報到率": f"{(enrolled/total*100):.1f}%" if total else "0.0%"
            })
        df_sum = pd.DataFrame(summary_rows)
        df_sum.to_excel(writer, sheet_name="歷年指標彙整", index=False)

        # 彙整工作表 2：搶走學生的外校排行 (Poaching Matrix)
        poached_df = df_all[df_all["去向分類"] == "其他學校錄取"]
        if not poached_df.empty:
            matrix = poached_df.groupby(["系所名稱", "最終分發學校"]).size().reset_index(name="被掠奪人數")
            matrix = matrix.sort_values(by=["系所名稱", "被掠奪人數"], ascending=[True, False])
            matrix.to_excel(writer, sheet_name="外校掠奪去向排行", index=False)

    print(f"已儲存 Master Excel: {output_excel}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
    else:
        json_file = "/Users/chenchunchih/Downloads/com_tw_21_pages.json"

    out_xlsx = "/Users/chenchunchih/Downloads/校務資料/高科大_北商_113_115四技二專交叉查榜資料庫.xlsx"
    out_csv = "/Users/chenchunchih/Downloads/校務資料/高科大_北商_113_115四技二專交叉查榜資料庫.csv"

    if os.path.exists(json_file):
        parse_bundle_json(json_file, out_xlsx, out_csv)
    else:
        print(f"等待頁面打包檔案: {json_file}")
