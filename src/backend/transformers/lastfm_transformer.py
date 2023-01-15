import os
import pandas as pd

DATA_SOURCE_PATH  = "../../../data/data_sources/"

dir = os.scandir(DATA_SOURCE_PATH)

large_df = pd.DataFrame()

for entry in dir:
    if entry.is_dir():
        break
    if entry.is_file():
        print(f"Reading: {entry.name}")
        data = pd.read_csv(entry)
        data["userplaylist"] = data["user_id"] + data["playlistname"]
        data = data[['userplaylist', 'artistname']]
        data["playlist_size"] = data.groupby("userplaylist")["userplaylist"].transform('count')
        data = data.loc[data["playlist_size"] < 25]
        data = data.loc[data["playlist_size"] > 5]
        data = data[['userplaylist', 'artistname']]
        large_df = pd.concat([large_df, data], ignore_index=True)

large_df = large_df.drop_duplicates()


print("Saving to artist_user_mapping. Size: ", large_df.size)
data.to_csv("../../../data/artist_user_mapping.csv",encoding="utf-8", mode="w", index=False)