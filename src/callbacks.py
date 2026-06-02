import os
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from src.config import BASE_DIR  # Using BASE_DIR because MODELS_DIR doesn't exist there

def get_training_callbacks(model_name="lstm_model.h5"):
    """
    Generates and returns the standardized Keras callbacks for Deep Learning governance.
    Ensures optimal training termination and dynamically checkpoints peak performance.
    """
    # Create the 'models' directory path safely using your existing BASE_DIR
    models_directory = os.path.join(BASE_DIR, "models")
    os.makedirs(models_directory, exist_ok=True)
    
    checkpoint_path = os.path.join(models_directory, model_name)
    
    # 1. Guardrail: Early Stopping
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=3,
        restore_best_weights=True,
        verbose=1
    )
    
    # 2. Guardrail: Model Checkpointing
    model_checkpoint = ModelCheckpoint(
        filepath=checkpoint_path,
        monitor='val_loss',
        save_best_only=True,
        mode='min',
        verbose=1
    )
    
    return [early_stopping, model_checkpoint]

if __name__ == "__main__":
    print("🔄 Testing Callbacks Configuration with BASE_DIR...")
    try:
        callbacks = get_training_callbacks()
        print(f"✅ Governance Framework Active: {len(callbacks)} callbacks successfully initialized.")
    except Exception as e:
        print(f"❌ Error initializing callbacks: {e}")