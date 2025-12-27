# -*- coding: utf-8 -*-
"""
籌碼排行分析
執行方式：在專案根目錄執行 `python analysis/01_ranking_chips.py`
"""
import pandas as pd
import os
import sys

def main():
    # 1. 設定資料路徑 (自動抓取上一層的 data 資料夾)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    
    twse_path = os.path.join(data_dir, "twse_flows.csv")
    tpex_path = os.path.join(data_dir, "tpex_flows.csv")

    if not os.path.exists(twse_path):
        print(f"[Error] 找不到 {twse_path}，請確認資料是否已下載。")
        return

    # 2. 讀取並合併上市上櫃資料
    print("[Info] 讀取資料中...")
    df_twse = pd.read_csv(twse_path)
    df_tpex = pd.read_csv(tpex_path)
    df = pd.concat([df_twse, df_tpex], ignore_index=True)

    # 轉換日期格式並排序
    df["date"] = pd.to_datetime(df["date"])
    all_dates = sorted(df["date"].unique())
    
    if not all_dates:
        print("[Error] 資料檔是空的。")
        return

    print(f"[Info] 資料區間: {all_dates[0].date()} ~ {all_dates[-1].date()}")

    # --- 分析函式 ---
    def analyze_period(days):
        if len(all_dates) < days:
            print(f"\n[Warn] 資料不足 {days} 天，跳過分析。")
            return

        # 取出最後 N 天的日期
        target_dates = all_dates[-days:]
        start_date = target_dates[0].date()
        end_date = target_dates[-1].date()

        print(f"\n{'='*10} 近 {days} 日籌碼分析 ({start_date} ~ {end_date}) {'='*10}")

        # 篩選資料
        mask = df["date"].isin(target_dates)
        subset = df[mask].copy()

        # 確保數值型態
        cols = ["foreign_net", "trust_net", "dealer_net"]
        for c in cols:
            subset[c] = pd.to_numeric(subset[c], errors="coerce").fillna(0)

        # 分組加總
        grouped = subset.groupby(["code", "name", "market"])[cols].sum().reset_index()
        grouped["total_net"] = grouped["foreign_net"] + grouped["trust_net"] + grouped["dealer_net"]

        # 顯示買超前 10 名
        top_buy = grouped.sort_values("total_net", ascending=False).head(10)
        print("\n[三大法人合計 '買超' Top 10]")
        print(top_buy[["code", "name", "total_net", "foreign_net", "trust_net"]].to_string(index=False))

    # 3. 執行分析
    analyze_period(5)
    analyze_period(10)

if __name__ == "__main__":
    main()