import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split

# Load dataset
df = pd.read_csv("data/raw/municipal_training_set_1100.csv")

# Text column
X = df["issue_description"]

# Target column
y = df["issue_type"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# TF-IDF vectorizer
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=3000
)

# Transform text
X_train_vectors = vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)

# Print shapes
print("Training Shape:", X_train_vectors.shape)
print("Testing Shape:", X_test_vectors.shape)

# Save vectorizer
with open("models/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("\nVectorizer saved successfully!")