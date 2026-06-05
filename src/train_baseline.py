import os
import pickle
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from src.config import RAW_DATA_PATH  # importing master paths if needed

def train_baseline_models():
    print("============================================================")
    # 1. Hamare models/ folder se fitted vectorizer load karenge
    vectorizer_path = "models/vectorizer.pkl"
    if not os.path.exists(vectorizer_path):
        print(f"❌ Error: Vectorizer not found at {vectorizer_path}. Please run text vectorization first!")
        return
        
    print("📦 Loading fitted TF-IDF Vectorizer...")
    with open(vectorizer_path, "rb") as f:
        vectorizer = pickle.load(f)

    # 2. Mocking Train-Test Data Splits (Ideally yahan validation split inputs honge)
    # Note: For baseline verification, loading raw data and splitting internally
    print("📊 Loading dataset and preparing matrices...")
    df = pd.read_csv(RAW_DATA_PATH, encoding='latin1')
    
    # Text aur Labels ko isolate karna (using clean text series)
    # Pro Tip: Split structure strictly separates training set (80%)
    from sklearn.model_selection import train_test_split
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(
        df['issue_description'], 
        df['issue_type'], 
        test_size=0.2, 
        random_state=42, 
        stratify=df['issue_type']
    )
    
    # Vector transformation
    X_train = vectorizer.transform(X_train_raw)
    
    print(f"🔹 Training Shape: {X_train.shape}")
    print(f"🔹 Target Classes: {list(y_train.unique())}")

    # 3. Model 1: Multinomial Naive Bayes (Standard Text Classifier)
    print("\n🤖 Training Model 1: Multinomial Naive Bayes...")
    nb_model = MultinomialNB()
    nb_model.fit(X_train, y_train)
    
    # Save Naive Bayes
    nb_path = "models/naive_bayes_model.pkl"
    with open(nb_path, "wb") as f:
        pickle.dump(nb_model, f)
    print(f"✅ Saved Naive Bayes to {nb_path}")

    # 4. Model 2: Logistic Regression (With Balanced Class Weights)
    print("\n🤖 Training Model 2: Logistic Regression (Balanced)...")
    lr_model = LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42)
    lr_model.fit(X_train, y_train)
    
    # Save Logistic Regression
    lr_path = "models/logistic_regression_model.pkl"
    with open(lr_path, "wb") as f:
        pickle.dump(lr_model, f)
    print(f"✅ Saved Logistic Regression to {lr_path}")
    
    print("============================================================")
    print("🎉 BASELINE MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("============================================================")

if __name__ == "__main__":
    train_baseline_models()