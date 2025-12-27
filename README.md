# tw-institutional-stocker

台股三大法人持股比重追蹤（上市 + 上櫃），自動每日更新並發佈到 GitHub Pages。

## 專案特色

- 支援多個時間視窗：`WINDOWS = [5, 20, 60, 120]`
- 三大法人模型升級：外資使用官方數據，投信/自營商支援基準點校正
- 自動化數據更新：GitHub Actions 每日自動執行
- Docker 容器化部署：一鍵啟動完整服務

## 專案結構

```
tw-institutional-stocker/
├── build/                    # Docker 建置相關
│   ├── Dockerfile           # Docker 映像檔定義
│   ├── .dockerignore        # Docker 忽略檔案
│   └── docker-compose.yml   # Docker Compose 設定
├── deployment/               # 部署腳本
│   ├── start.sh            # 啟動服務（build + run）
│   └── stop.sh             # 停止服務
├── data/                     # 數據目錄
│   ├── *_flows.csv         # 三大法人買賣超數據
│   ├── *_foreign.csv       # 外資持股數據
│   └── inst_baseline.csv   # 投信/自營商基準點（選用）
├── docs/                     # 前端靜態檔案
│   ├── index.html
│   ├── script.js
│   ├── style.css
│   └── data/               # 前端使用的 JSON 數據
│       ├── timeseries/     # 個股時間序列
│       └── top_three_inst_change_*.json  # 排名榜單
├── .github/workflows/       # GitHub Actions
│   └── update.yml          # 自動更新工作流程
├── update_all.py           # 主程式：數據抓取與處理
├── requirements.txt        # Python 相依套件
└── README.md
```

## 快速開始

### 使用 Docker（推薦）

1. **啟動服務**
   ```bash
   ./deployment/start.sh
   ```

   這個指令會：
   - 建置 Docker 映像檔
   - 抓取最新三大法人數據
   - 啟動網頁伺服器（port 8000）

2. **訪問網頁**

   開啟瀏覽器訪問：http://localhost:8000

3. **停止服務**
   ```bash
   ./deployment/stop.sh
   ```

### 本地開發

```bash
# 安裝相依套件
pip install -r requirements.txt

# 執行數據更新
python update_all.py

# 啟動網頁伺服器（在 docs 目錄）
cd docs
python -m http.server 8000
```

## 功能說明

### 數據來源

- **三大法人買賣超**：TWSE T86 + TPEX 3itrade_hedge_result
- **外資持股統計**：TWSE MI_QFIIS + TPEX QFII

### 三大法人模型

- **外資**：直接採用官方 `foreign_ratio`
- **投信/自營商**：支援基準點校正模型
  - 若有提供 `data/inst_baseline.csv`，則從基準點開始累加淨買超
  - 若無基準點，則使用純 cumsum 模型

### 輸出檔案

- **時間序列數據**：`docs/data/timeseries/{code}.json`
- **排名榜單**：
  - `docs/data/top_three_inst_change_5_up.json` / `_down.json`
  - `docs/data/top_three_inst_change_20_up.json` / `_down.json`
  - `docs/data/top_three_inst_change_60_up.json` / `_down.json`
  - `docs/data/top_three_inst_change_120_up.json` / `_down.json`

### 前端功能

- 輸入股票代碼查看三大法人持股趨勢圖
- 以 5/20/60/120 日變化排序的排名表
- 市場過濾（全部/上市/上櫃）
- Log scale 切換

## GitHub Actions 自動化

專案使用 GitHub Actions 每天 00:10 UTC 自動執行數據更新：

1. 執行 `python update_all.py`
2. 若 `data/` 或 `docs/data/` 有變動，自動 commit + push

## 基準點校正（選用）

若要啟用投信/自營商的基準點校正：

1. 整理出某幾個日期的實際持股股數
2. 填入 `data/inst_baseline.csv`：
   ```csv
   date,code,trust_shares_base,dealer_shares_base
   2025-01-31,2330,100000000,20000000
   2025-01-31,0050,50000000,0
   ```
3. 重新執行 `python update_all.py`

## Docker 指令參考

```bash
# 查看服務狀態
docker-compose -f build/docker-compose.yml ps

# 查看網頁伺服器日誌
docker-compose -f build/docker-compose.yml logs -f web

# 只執行數據更新（不啟動網頁伺服器）
docker-compose -f build/docker-compose.yml run --rm updater

# 停止並清理所有容器
docker-compose -f build/docker-compose.yml down
```

## 授權

MIT License
