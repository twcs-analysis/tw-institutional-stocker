#!/bin/bash

# 台股三大法人持股追蹤系統 - Docker 啟動腳本

set -e

# 切換到專案根目錄
cd "$(dirname "$0")/.."

echo "=========================================="
echo "台股三大法人持股追蹤系統 - Docker 啟動"
echo "=========================================="
echo ""

# 建置 Docker 映像檔
echo "[1/3] 正在建置 Docker 映像檔..."
docker-compose -f build/docker-compose.yml build

echo ""
echo "[2/3] 正在啟動服務..."
echo ""

# 啟動所有服務（updater 會先執行並退出，web 會持續運行）
docker-compose -f build/docker-compose.yml up -d

echo ""
echo "[3/3] 等待數據更新完成..."
echo ""

# 等待 updater 完成（但不阻塞顯示）
while [ "$(docker-compose -f build/docker-compose.yml ps -q updater 2>/dev/null)" != "" ]; do
  sleep 2
done

echo ""
echo "=========================================="
echo "✅ 啟動完成！"
echo "=========================================="
echo ""
echo "🌐 服務網址: http://localhost:8000"
echo "📊 查看日誌: docker-compose -f build/docker-compose.yml logs -f web"
echo "🛑 停止服務: ./deployment/stop.sh"
echo "📋 服務狀態: docker-compose -f build/docker-compose.yml ps"
echo ""
