#!/bin/bash

# 台股三大法人持股追蹤系統 - Docker 停止腳本

# 切換到專案根目錄
cd "$(dirname "$0")/.."

echo "=========================================="
echo "正在停止所有 Docker 容器..."
echo "=========================================="
echo ""

docker-compose -f build/docker-compose.yml down

echo ""
echo "✅ 所有服務已停止"
echo ""
