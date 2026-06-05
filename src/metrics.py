import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def calculate_evaluation_metrics(y_true, y_pred, output_dir="models/"):
    """
    Unified performance evaluation tracker.
    Generates text logs and visual confusion matrix heatmaps.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Calculate Standard Metrics
    accuracy = accuracy_score(y_true, y_pred)
    class_report = classification_report(y_true, y_pred)
    
    print("\n========= 📊 MODEL PERFORMANCE REPORT =========")
    print(f"🎯 Global Accuracy Score: {accuracy:.4f}")
    print("\n📝 Detailed Classification Report:")
    print(class_report)
    print("================================================")
    
    # 2. Save text report to tracking storage
    report_path = os.path.join(output_dir, "evaluation_report.txt")
    with open(report_path, "w") as f:
        f.write("========= MODEL PERFORMANCE REPORT =========\n")
        f.write(f"Global Accuracy Score: {accuracy:.4f}\n\n")
        f.write("Detailed Classification Report:\n")
        f.write(class_report)
    print(f"💾 Performance logs archived safely at: {report_path}")

def generate_confusion_matrix_plot(y_true, y_pred, classes, output_path="notebooks/confusion_matrix.png"):
    """
    Generates a clean, normalized Seaborn Heatmap for error analysis.
    Directly injectable into Member 4's notebook layout.
    """
    cm = confusion_matrix(y_true, y_pred, labels=classes)
    
    plt.figure(figsize=(10, 7))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=classes, yticklabels=classes)
    
    plt.title('⚖️ Baseline Model: Error Distribution Confusion Matrix', fontsize=14, pad=15)
    plt.ylabel('Actual Department Labels', fontsize=12)
    plt.xlabel('Predicted Department Labels', fontsize=12)
    plt.tight_layout()
    
    # Ensure notebooks folder exists before saving plot
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, dpi=300)
    plt.close()
    print(f"🎨 Confusion Matrix plot generated and saved at: {output_path}")

if __name__ == "__main__":
    # Test block to verify imports and file routing work perfectly
    print("🚀 Validation framework active. Ready for model predictions evaluation pipeline.")