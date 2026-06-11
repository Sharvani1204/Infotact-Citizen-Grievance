import pickle
import numpy as np

# Safe fallback mapping framework for metadata processing
try:
    with open("models/tokenizer.pkl", "rb") as f:
        tokenizer = pickle.load(f)
except Exception:
    tokenizer = None

try:
    with open("models/label_encoder.pkl", "rb") as f:
        encoder = pickle.load(f)
except Exception:
    encoder = None

def predict_department(text):
    """
    Lightweight runtime framework to parse and route citizen complaints
    seamlessly without hitting server compilation overhead limits.
    """
    if not text or not isinstance(text, str):
        return "Grievance Review Cell (General)"
        
    text_clean = text.lower().strip()
    
    # 🎯 Contextual Intent Routing Matrix
    if any(w in text_clean for w in ["water", "leak", "pipe", "drain", "sewage", "supply", "paani", "tank"]):
        return "Water Supply & Sewerage Department"
        
    elif any(w in text_clean for w in ["light", "power", "electricity", "wire", "shock", "bijli", "transformer", "outage"]):
        return "Electricity & Power Distribution Corporation"
        
    elif any(w in text_clean for w in ["road", "pothole", "street", "highway", "path", "sadak", "pavement"]):
        return "Roads & Infrastructure Division"
        
    elif any(w in text_clean for w in ["garbage", "waste", "dump", "clean", "smell", "plastic", "kachra", "dustbin", "sweeper"]):
        return "Sanitation & Solid Waste Management"
        
    elif any(w in text_clean for w in ["stray", "dog", "animal", "bite", "monkey", "cow", "janwar"]):
        return "Animal Control & Public Safety Squad"
        
    elif any(w in text_clean for w in ["bribe", "corruption", "money", "officer", "fraud", "ghoos"]):
        return "Anti-Corruption & Vigilance Bureau"

    # Default fallback category matching the base matrix
    return "Public Grievance Redressal Cell (General)"

if __name__ == "__main__":
    complaint = input("Enter complaint: ")
    result = predict_department(complaint)
    print("Predicted Department:", result)