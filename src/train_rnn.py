import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, SpatialDropout1D, Bidirectional, LSTM, Dense

# Load dataset
df = pd.read_csv("data/raw/municipal_training_set_1100.csv")

# Features and labels
X = df["issue_description"].astype(str)
y = df["issue_type"]

# Encode labels
encoder = LabelEncoder()
y = encoder.fit_transform(y)

import pickle

with open("models/label_encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("Categories:")
print(df["issue_type"].unique())

print("Total Classes:", len(df["issue_type"].unique()))

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Tokenizer
tokenizer = Tokenizer(
    num_words=5000,
    oov_token="<OOV>"
)

tokenizer.fit_on_texts(X_train)

import pickle

with open("models/tokenizer.pkl", "wb") as f:
    pickle.dump(tokenizer, f)

X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

# Padding
max_len = 100

X_train_pad = pad_sequences(X_train_seq, maxlen=max_len, padding="post")
X_test_pad = pad_sequences(X_test_seq, maxlen=max_len, padding="post")

# Build model
model = Sequential()

model.add(
    Embedding(
        input_dim=5000,
        output_dim=64
    )
)

model.add(
    SpatialDropout1D(0.2)
)

model.add(
    Bidirectional(
        LSTM(64)
    )
)

model.add(
    Dense(11, activation="softmax")
)

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

model.summary()

history = model.fit(
    X_train_pad,
    y_train,
    epochs=5,
    batch_size=32,
    validation_split=0.2
)

# Save model
model.save("models/lstm_model.h5")

print("Model saved successfully!")

loss, accuracy = model.evaluate(X_test_pad, y_test)

print("Test Accuracy:", accuracy)