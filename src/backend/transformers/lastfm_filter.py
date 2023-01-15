import pandas as pd

print("Reading large file")
data = pd.read_csv("../../../data/lastfm_big.csv", delimiter="\t")

print(f"Number of elements removed from file: {(data.loc[data['plays'] <= 1000]).size}")

print("Filtering large file")
data = data.loc[data["plays"] > 1000]

print(f"Size after filtering: {data.size}")

data.to_csv("../../../data/lastfm_filtered.csv",encoding="utf-8", mode="w", index=False)