# -*- coding: utf-8 -*-
"""
本地籌碼分析腳本
用途：讀取 data/ 資料夾下的歷史 CSV，計算近 5 日、10 日三大法人買賣超排行。
"""
import pandas as pd
import os

def main():
    # 1. 檢查資料是否存在
    twse_path = os.path.join("data", "twse_flows.csv")
    tpex_path = os.path.join("data", "tpex_flows.csv")

    if not os.path.exists(twse_path):
        print(f"[Error] 找不到 {twse_path}，請先執行 python update_all.py 抓取資料。")
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

        # 確保數值型態 (避免 CSV 讀入變成字串)
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

        # 顯示賣超前 10 名
        top_sell = grouped.sort_values("total_net", ascending=True).head(10)
        print("\n[三大法人合計 '賣超' Top 10]")
        print(top_sell[["code", "name", "total_net", "foreign_net", "trust_net"]].to_string(index=False))

    # 3. 執行分析
    analyze_period(5)
    analyze_period(10)

if __name__ == "__main__":
    main()