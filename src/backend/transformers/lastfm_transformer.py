import pandas as pd

## With small
print("Reading small file")
data = pd.read_csv("../../../data/lastfm.csv")

data = data[["user", "artist"]]
## Drop duplicates
data = data.drop_duplicates()

data.to_csv("../../../data/artist_user_mapping.csv",encoding="utf-8", index=False)

## With large
print("Reading large file")
data = pd.read_csv("../../../data/lastfm_big.csv", delimiter="\t")

print("Filtering large file")
data = data.loc[data["plays"] > 5000]

print(f"Size after filtering: {data.size}")

data = data[["user", "artist"]]
## Drop duplicates
data = data.drop_duplicates()

print("Saving to artist_user_mapping")
data.to_csv("../../../data/artist_user_mapping.csv",encoding="utf-8", mode="a", header=False, index=False)