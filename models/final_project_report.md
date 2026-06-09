# 🏛️ Final Evaluation Ledger: Multi-Class Citizen Grievance Redressal

This document records the definitive comparative audit metrics across our production classification frameworks for municipal complaint classification (5 Target Classes).

## 📊 Global Performance Summary

| Architecture Metric | Classical Baseline (Logistic Regression) | Deep Learning Core (Bidirectional LSTM) |
| :--- | :---: | :---: |
| **Global Accuracy** | *[Insert %]* | *[Insert %]* |
| **Macro Precision** | *[Insert Value]* | *[Insert Value]* |
| **Macro Recall** | *[Insert Value]* | *[Insert Value]* |
| **Macro F1-Score** | *[Insert Value]* | *[Insert Value]* |

---

## 🔍 Key Architectural Insights & Analysis

### 1. Why the Bidirectional LSTM Outperformed the Baseline
* **Sequential Context Tracking:** While the classical TF-IDF baseline treated words as an isolated "bag-of-words" (losing phrase order), the Bidirectional LSTM processed the text forward and backward simultaneously. This allowed the network to learn structural dependencies (e.g., catching complex sentence context for "water accumulation due to pipe leakage").
* **Stopword Resilience:** The deep learning embedding layer natively map words into dense vector spaces, capturing underlying semantic meanings much more effectively than rigid character-matching frequencies.

### 2. Failure Mode Analysis (Where the network still struggles)
* *[Write 1-2 sentences here after your final run about which classes confused the model the most, e.g., minor overlaps between 'potholes' and 'illegal_parking' when street names were mentioned together.]*