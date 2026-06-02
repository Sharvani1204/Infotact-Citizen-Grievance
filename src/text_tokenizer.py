import pandas as pd
import pickle

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load dataset
df = pd.read_csv("data/raw/municipal_training_set_1100.csv")

# Remove missing values
df = df.dropna(subset=["issue_description"])

# Text column
texts = df["issue_description"].astype(str)

# Tokenizer settings
VOCAB_SIZE = 5000
MAX_LEN = 100
OOV_TOKEN = "<OOV>"

# Create tokenizer
tokenizer = Tokenizer(
    num_words=VOCAB_SIZE,
    oov_token=OOV_TOKEN
)

# Fit tokenizer
tokenizer.fit_on_texts(texts)

# Convert text to sequences
sequences = tokenizer.texts_to_sequences(texts)

# Apply padding
padded_sequences = pad_sequences(
    sequences,
    maxlen=MAX_LEN,
    padding="post",
    truncating="post"
)

# Save tokenizer
with open("models/tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

print("Tokenizer saved successfully")

print("Vocabulary size:", VOCAB_SIZE)
print("Max sequence length:", MAX_LEN)
print("Padded sequence shape:", padded_sequences.shape)