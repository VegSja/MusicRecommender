import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.preprocessing import TransactionEncoder

import sqlite3

conn = sqlite3.connect("../database/sqlite.db")
c = conn.cursor()

def get_data_as_df():
    data = pd.read_csv("../../data/artist_user_mapping.csv")
    artist = data["artistname"].drop_duplicates()
    artist.to_sql("Artist", con=conn, if_exists='replace', index=True)
    return data

def save_transactions(transactions):
    total = []
    for transaction in transactions:
        trans_str = ",".join(transaction)
        total.append(trans_str)
    df = pd.DataFrame(total, columns=["Content"])
    df.to_sql("Playlist", con=conn, if_exists='replace', index=True)
    
def read_transactions_from_file():
    transactions = []
    with open("../../data/transactions.txt", "r") as file:
        text = file.read()
        text_list = text.split('\n')
        for element in text_list:
            transactions.append(element.split(','))
    return transactions

def read_transactions_from_db():
    c.execute("SELECT Content FROM Playlist;")
    data = c.fetchall()
    transactions = []
    for transaction in data:
        transactions.append(transaction[0].split(","))
    return transactions

def get_transactions():
    nb_of_playlists = 100

    data = get_data_as_df()
    ## Drop duplicates
    data = data.drop_duplicates()

    ## Select the columns the clustering will focus on
    data = data[['userplaylist', 'artistname']]

    print("Converting to transactions")
    amount = data['userplaylist'].unique().size
    current = 0
    transactions = []
    for i in data['userplaylist'].unique():
        current += 1
        transactions.append(list(data[data['userplaylist'] == i]['artistname'].values))
        print(f"Progress: {current}/{amount}")
        #if(current == nb_of_playlists): break
    
    save_transactions(transactions=transactions)

    return transactions

def retrieve_second_item(iterator):
    x = iter(iterator)
    next(x)
    return next(x)

def create_assoctiation_rules():
    get_data_as_df()
    transactions = read_transactions_from_db()

    print("Calculating Apriori estimates")
    te = TransactionEncoder()
    oht_ary = te.fit(transactions).transform(transactions, sparse=True)

    sparse_df = pd.DataFrame.sparse.from_spmatrix(oht_ary, columns=te.columns_)
    rules = apriori(sparse_df, min_support=0.001, max_len=2, use_colnames=True, verbose=1, low_memory=True)
    
    print("Creating dataframe")
    rules['length'] = rules['itemsets'].apply(lambda x: len(x))
    rules = rules[rules.length != 1]
    rules["leftside"] = rules['itemsets'].apply(lambda x: next(iter(x)))
    rules["rightside"] = rules['itemsets'].apply(lambda x: retrieve_second_item(x))
    rules = rules[["leftside", "rightside", "support"]]

    # Make dataframe symmetric
    print("Making dataframe symmetric")
    rules_inverse = rules.copy()
    rules_inverse.columns = ["rightside", "leftside", "support"]

    symmetric_df = pd.concat([rules, rules_inverse]).sort_index().reset_index(drop=True)


    return symmetric_df

def main():
    rules = create_assoctiation_rules()
    print("Sorting rules")
    rules = rules.sort_values(by="support", ascending=False)

    print("Saving rules to database")
    rules.to_sql("Rules", con=conn, if_exists='replace', index=True)

main()