# 使用 Python 3.10 slim 版本作為基底，兼顧映像檔大小與相容性
FROM python:3.10-slim

# 安裝 tzdata 以支援 ZoneInfo("Asia/Taipei")
RUN apt-get update && apt-get install -y tzdata && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 先複製 requirements.txt 以利用 Docker cache 加速後續建置
COPY requirements.txt .

# 安裝 Python 套件
# 提示：pandas.read_html 通常需要 lxml，請確保 requirements.txt 內有包含 lxml
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案所有程式碼到容器內
COPY . .

# 設定容器啟動時執行的指令
CMD ["python", "update_all.py"]