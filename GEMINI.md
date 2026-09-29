# Project Guidelines & Design Rules

## Web & Frontend UI Design Standards (Impeccable)

當為本專案設計、建置或優化任何網站、前端網頁（如 HTML/CSS/JS、Tailwind、Vue、React 等）、儀表板或 UI 元件時，**必須全面參考並嚴格遵從 `impeccable` 設計系統規範**（參見 [craft-floor.md](file:///Users/chenchunchih/Downloads/校務資料/.agents/skills/impeccable/reference/craft-floor.md)）：

### 1. 堅決摒棄 AI 生成的常見低質感通病（Anti-Patterns）
- **禁止使用漸層文字（Gradient Text）**：強調文字請使用字重（Weight）或字級（Size），而非廉價漸層。
- **禁止浮濫的毛玻璃與模糊（Glassmorphism / Blur）**：除非有明確的多層抽屜或模態需求，否則不將 blur 作為隨意的裝飾。
- **禁止色塊側邊框（Colored border-left / border-right）**：卡片、引用塊或提示框不使用大於 1px 的粗色條邊框。
- **禁止重複刻板的卡片堆疊（Nested Cards / Repetitive Cards）**：不要所有內容都塞在千篇一律的「小圖示 + 標題 + 內文」卡片裡，善用無邊框排版、留白與對齊。
- **禁止在標題上方加裝飾性小標籤（Eyebrows / Kickers）**：讓真正的主標題自己承擔視覺份量。
- **禁止使用 Emoji 充當圖示系統**：圖示一律採用專業向量圖示庫（如 FontAwesome、Lucide、Heroicons 或專屬 SVG），並維持線條粗細與風格一致。
- **禁止僵硬的無模糊陰影（Hard Offset Shadows）**：除非是真正的像素復古風格，否則使用自然柔和的漫射陰影（Soft blur with subtle Y-offset）。

### 2. 嚴格落實工藝底線（Craft Floor）
- **對比度標準**：內文與主要文字對比度 ≥ 4.5:1，大標題 ≥ 3:1。有色背景上的次要文字請使用同色系淺/深階，嚴禁粗糙的灰階。
- **字體排印（Typography）**：段落行寬維持在 65–75 字元（characters）；標題與內文層級階梯分明；字距（tracking）微調（-0.02em ~ -0.03em 更具質感）。
- **留白節奏（Spacing Rhythm）**：內部緊湊、外部大氣；標題上方的間距必須大於標題下方的間距。
- **完整互動狀態（States）**：所有可操作元件必須具備優雅的 Hover、Focus（鍵盤無障礙）、Active、Disabled 與 Loading 狀態。
- **瀏覽器原生細節修飾**：文字選取（`::selection`）、聚焦框（Focus rings）、自訂捲軸等，皆應融入網站色彩體系。
