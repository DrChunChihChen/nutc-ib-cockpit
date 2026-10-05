# 國立臺中科技大學 國際貿易與經營系 (NUTC ITM)<br>校務研究與招生決策戰情室系統 (IR Decision Cockpit)

[![Netlify Status](https://api.netlify.com/api/v1/badges/d7811e12-2648-4180-bb02-ea0edb982c8b/deploy-status)](https://app.netlify.com/projects/nutc-ib-cockpit/deploys)
[![Live Site](https://img.shields.io/badge/Production-Live%20Cockpit-10b981.svg)](https://nutc-ib-cockpit.netlify.app)
[![Data Audit](https://img.shields.io/badge/MOE%20UDB-100%25%20Pure%20Daytime%20Audited-blue.svg)](https://udb.moe.edu.tw/)

> 本專案為國立臺中科技大學國際貿易與經營系（NUTC ITM）打造之高階校務研究（Institutional Research, IR）決策戰情室與招生戰略沙盤。透過教育部大專校院校務資訊公開平台（UDB）、技專聯招與交叉查榜全量數據、104 人力銀行 700+ 筆外銷職缺實證，建構全面量化之系所經營與生源防禦體系。

---

## 🌐 線上正式站台 (Live Production)

* **官方戰情室**：[https://nutc-ib-cockpit.netlify.app](https://nutc-ib-cockpit.netlify.app)
* **決策閉環視覺化**：[`nutc_performance_loop.html`](./nutc_performance_loop.html)
* **戰情室主頁面**：[`output/index.html`](./output/index.html)
* **完整原始數據庫**：`raw_data/` 及 `NUTC_ITM_Comprehensive_IR_Raw_Data_Pack.xlsx`

---

## 📊 核心戰情模組 (7 大面向)

1. **模組 1：公立國貿、商務與海運物流校系橫向指標評比**
   * 納入全國國立商管六強：北商國商、中科國貿、雲科國管、高科航管、高科國企、高科行流。
   * 100% 純日間部審計：中科國貿純日間學生 708 人（四技 382 + 二技 74 + 五專 252），退學率僅 2.82%，專任生師比 33.7:1，114 日間註冊率 99.40%。
   * 國際深化度指標：境外生/日四技比率達 **15.18%**（58 / 382），居公立國貿第二。

2. **模組 2：中部大專國貿商管校系橫向競合**
   * 深度對決中區競校：中科國貿 vs 逢甲國貿 vs 東海國貿 vs 朝陽國企 vs 嶺東國企。
   * 解析私立學費補貼政策後之生源吸磁效應、各校財務現金存量、以及主動減招防禦策略。

3. **模組 3：中科國貿各學制結構與在學生留存分析**
   * 歷年統測 09商管群最低錄取分與單科均分走勢（中科國貿以 71.78 分領先中區公立商管）。
   * 純日間部休學（4.10%）與退學（2.82%）極低流失深水區診斷。

4. **模組 4：少子化生源走勢與學制規模試算模型**
   * 介接教育部 113~128 學年度少子化預測，內建 4 支動態滑桿即時推演 117 虎年谷底與日四技滿招防護邊界。

5. **模組 5：四技甄選考生交叉查榜流向與天敵情報**
   * 採集 113~115 三學年度 525 筆交叉查榜全量考生母體。
   * 精準繪製正取生報到率（33.3%）、備取遞補深度，以及流失至高科大（120人次）與跨系至中科企管（34:11）之微觀流向。

6. **模組 6：台中經貿三大領域戰情地圖**
   * 實地探勘中彰投三大經貿支柱：國外業務、報關行與跨境電商聚落。

7. **模組 7：經貿就業市場與 AI 智慧商務技能矩陣**
   * 實時採集 104 人力銀行 700+ 筆真實職缺。
   * 實證生成式 AI（ChatGPT/Prompt）在外銷職缺中帶來 +15%~20% 起薪溢價，多益門檻要求與技能共現網路。

---

## 🛠️ 技術架構與資料管線

* **前端架構**：單頁式響應式架構（SPA）、Tailwind CSS、Chart.js (UMD)、FontAwesome 6、Lucide Icons。
* **設計規範**：遵從 `impeccable` 工藝底線（高對比度、無粗糙漸層、無多餘裝飾、精準排印節奏）。
* **資料處理**：Python (Pandas, BeautifulSoup, Requests, OpenPyXL) 進行教育部 UDB 爬取、交叉查榜解析與 104 API 數據清洗。
* **雲端部署**：Netlify 邊緣 CDN 自動化持續部署。

---

## 👨‍🏫 計畫主持人 / 專案負責人

* **陳俊智 副教授 (Dr. Elvis Chun-Chih Chen)**
* 國立臺中科技大學 國際貿易與經營系 (Department of International Trade & Management, NUTC)
* 研究專長：校務研究 (IR)、國際貿易實務、高等教育政策、計量經濟分析
