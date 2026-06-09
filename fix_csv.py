import pandas as pd

columns = [
    "timestamp",
    "open",
    "high",
    "low",
    "close",
    "volume_btc",
    "volume_usd"
]

df = pd.read_csv(
    "data.csv",
    header=None,
    names=["raw"]
)

split_df = df["raw"].str.split(",", expand=True)

split_df.columns = columns

split_df.to_csv(
    "clean_data.csv",
    index=False
)

print("CSV fixed successfully!")
print(split_df.head())