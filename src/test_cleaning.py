import pandas as pd
from cleaning_utils import clean_text
from config import RAW_DATA_PATH, TEXT_COLUMN

df = pd.read_csv(RAW_DATA_PATH)

sample = df[TEXT_COLUMN].iloc[0]

print("Original:")
print(sample)

print("\nCleaned:")
print(clean_text(sample))