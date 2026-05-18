print("🚀 Python Engine: Script successfully triggered!")

import pandas as pd
import os
from src.config import RAW_DATA_PATH, TEXT_COLUMN, LABEL_COLUMN

def run_data_audit():
    print("=" * 60)
    print("🔍 STARTING AUTOMATED DATA INTEGRITY AUDIT")
    print("=" * 60)
    
    # Check if the file exists before reading
    if not os.path.exists(RAW_DATA_PATH):
        print(f"❌ Error: Raw data file not found at {RAW_DATA_PATH}")
        return
    
    # Ingest Data
    df = pd.read_csv(RAW_DATA_PATH, encoding='latin1')
    
    # 1. Structural Integrity Check
    print("\n📊 [1/4] STRUCTURAL METRICS:")
    print(f"   • Total Rows (Complaints): {df.shape[0]}")
    print(f"   • Total Columns: {df.shape[1]}")
    print(f"   • Columns Present: {df.columns.tolist()}")

    if TEXT_COLUMN not in df.columns or LABEL_COLUMN not in df.columns:
        print(f"   ⚠️ WARNING: Target columns ('{TEXT_COLUMN}' or '{LABEL_COLUMN}') are missing!")
        return
    
    # 2. Null/Missing Value Scan
    print("\n❌ [2/4] MISSING VALUE SCAN:")
    text_nulls = df[TEXT_COLUMN].isnull().sum()
    label_nulls = df[LABEL_COLUMN].isnull().sum()
    total_nulls = df.isnull().sum().sum()

    print(f"   • Missing Text Values (`{TEXT_COLUMN}`): {text_nulls}")
    print(f"   • Missing Department Labels (`{LABEL_COLUMN}`): {label_nulls}")
    print(f"   • Total Missing Data Points across file: {total_nulls}")

    # 3. Duplicate Complaint Tracking
    print("\n🔄 [3/4] DUPLICATE ENTRIES SCAN:")
    text_duplicates = df.duplicated(subset=[TEXT_COLUMN]).sum()
    print(f"   • Duplicate complaints found (based on text): {text_duplicates}")

    # 4. Text Length Distributions
    print("\n📝 [4/4] TEXT LENGTH & DISTRIBUTION (Character Counts):")
    clean_text_series = df[TEXT_COLUMN].dropna().astype(str)
    lengths = clean_text_series.str.len()

    print(f"   • Minimum length: {lengths.min()} characters")
    print(f"   • Maximum length: {lengths.max()} characters")
    print(f"   • Average length: {round(lengths.mean(), 2)} characters")

    short_complaints = (lengths < 10).sum()
    print(f"   • Anomalously short complaints (< 10 chars): {short_complaints}")

    print("\n" + "=" * 60)
    print("✅ DATA INTEGRITY AUDIT COMPLETE")
    print("=" * 60)

run_data_audit()