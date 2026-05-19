import pandas as pd

def load_data(filepath):
    try:
        df = pd.read_csv(filepath, encoding='utf-8')

    except UnicodeDecodeError:
        print("UTF-8 failed, trying latin1...")
        df = pd.read_csv(filepath, encoding='latin1')

    print("Dataset Shape:", df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nData Types:")
    print(df.dtypes)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    print("\nComplaint Category Distribution:")
    print(df["issue_type"].value_counts())

    print("\nComplaint Description Length:")
    print(df["issue_description"].str.len().describe())

    return df


if __name__ == "__main__":
    filepath = "data/raw/municipal_training_set_1100.csv"
    df = load_data(filepath)