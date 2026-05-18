import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "municipal_training_set_1100.csv")
CLEANED_DATA_PATH = os.path.join(BASE_DIR, "data", "cleaned_grievances.csv")

TEXT_COLUMN = "issue_description"  # The raw citizen complaint text
LABEL_COLUMN = "issue_type"        # The target department category

TARGET_DEPARTMENTS = [
    "noise",
    "streetlight",
    "illegal_parking",
    "pothole",
    "water_leakage"
]


CUSTOM_STOPWORDS = [
    "sir", "madam", "please", "request", "complaint",
    "grievance", "dear", "urgent", "emergency", "area", "problem"
]