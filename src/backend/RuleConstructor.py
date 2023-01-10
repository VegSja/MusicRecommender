import pandas as pd
from apyori import apriori


def get_data_as_df():
    return pd.read_csv("../../data/artist_user_mapping.csv")


def get_transactions():
    data = get_data_as_df()
    ## Drop duplicates
    data = data.drop_duplicates()

    ## Select the columns the clustering will focus on
    data = data[['user', 'artist']]

    transactions = []
    print("Converting to transactions")
    for i in data['user'].unique():
        transactions.append(list(data[data['user'] == i]['artist'].values))

    return transactions

## Used to create the output dataframe
def inspect(output):
    lhs         = [tuple(result[2][0][0])[0] for result in output]
    rhs         = [tuple(result[2][0][1])[0] for result in output]
    support    = [result[1] for result in output]
    confidence = [result[2][0][2] for result in output]
    lift       = [result[2][0][3] for result in output]
    return list(zip(lhs, rhs, support, confidence, lift))

def create_assoctiation_rules():
    transactions = get_transactions()

    print("Calculating Apriori estimates")
    rules = apriori(transactions = transactions, min_support = 0.005, min_confidence = 0.1, min_lift = 2)
    
    print("Creating list of estimates")
    results = list(rules)

    rule_dataframe = pd.DataFrame(inspect(results), columns = ['Left_Hand_Side', 'Right_Hand_Side', 'Support', 'Confidence', 'Lift'])

    return rule_dataframe

def main():
    rules = create_assoctiation_rules()
    print("Sorting rules")
    rules = rules.sort_values(by="Lift", ascending=False)

    print("Saving rules to csv")
    rules.to_csv("../../data/rules.csv", encoding='utf-8', index=False)

main()