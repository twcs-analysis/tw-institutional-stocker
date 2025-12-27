# Changelog

All notable changes to this project will be documented in this file.

## [2025-12-27] - 專案重組與 Docker 容器化

### Added
- Docker 容器化部署
  - 新增 [build/Dockerfile](build/Dockerfile) - Docker 映像檔定義
  - 新增 [build/.dockerignore](build/.dockerignore) - Docker 忽略檔案
  - 新增 [build/docker-compose.yml](build/docker-compose.yml) - Docker Compose 設定
    - `updater` 服務：一次性執行數據更新
    - `web` 服務：持續運行 HTTP server (port 8000)
- 部署腳本自動化
  - 新增 [deployment/start.sh](deployment/start.sh) - 一鍵啟動服務（build + run）
  - 新增 [deployment/stop.sh](deployment/stop.sh) - 停止所有 Docker 服務
- 完整的專案文檔
  - 更新 [README.md](README.md) - 包含專案結構、快速開始、Docker 指令參考
  - 新增 [CHANGELOG.md](CHANGELOG.md) - 變更記錄

### Changed
- 專案結構重組
  - 建置相關檔案移至 `build/` 目錄
  - 部署腳本移至 `deployment/` 目錄
  - 改善專案可維護性與清晰度

### Technical Details
- Docker Compose 採用雙服務架構：
  - updater 服務先執行並退出（數據更新）
  - web 服務等待 updater 完成後啟動（網頁伺服器）
  - 使用 `depends_on.condition: service_completed_successfully` 確保執行順序
- 部署腳本特性：
  - 自動切換到專案根目錄（支援從任意位置執行）
  - 背景運行模式（啟動後立即返回 shell）
  - 智能等待機制（等待 updater 完成，不阻塞 UI）

## [Prior] - 歷史版本

### Features
- 三大法人持股追蹤系統
- 支援上市與上櫃股票
- 多時間視窗分析 (5, 20, 60, 120 日)
- 基準點校正模型（投信/自營商）
- GitHub Actions 自動每日更新
- GitHub Pages 前端介面
