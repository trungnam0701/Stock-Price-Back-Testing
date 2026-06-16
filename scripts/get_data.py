import pandas as pd
import os
import yfinance as yf
from functools import reduce

SAVE_FOLDER = 'D:\StockPrice\data'

dfs = []
tickers = [
    "FPT.VN",
    "HPG.VN",
    "VCB.VN",
    "TCB.VN",
    "MWG.VN", 
    "^VNINDEX"
]

for ticker in tickers:
    
    if ".VN" in ticker:
        code = ticker.replace(".VN", "")
    else:
        code = ticker.replace("^", "")
    
    df = yf.download(
        ticker,
        start="2019-01-01",
        end="2026-06-01"
    )

    file_name = f"{ticker}.xlsx"
    # Xoá cột đầu tiên của bảng
    df.columns = df.columns.droplevel(1)
    
    df = df[['Close', 'Volume']]
    df = df.rename(columns={
        'Close': f'{code}_Close',
        'Volume': f'{code}_Volume'
    })
    
    df.reset_index(inplace=True)

    dfs.append(df)
    
merged_df = reduce(
    lambda left, right: pd.merge(left, right, on='Date', how='outer'),
    dfs
)

merged_df.to_excel(
    os.path.join(SAVE_FOLDER, "VN5_Close_Volume.xlsx"),
    index=False
)

print(f'Đã lưu data vào {SAVE_FOLDER}')
