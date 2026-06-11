from tensorflow.keras.models import load_model
import pickle
import numpy as np

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load tokenizer
with open("models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Load label encoder
with open("models/label_encoder.pkl", "rb") as f:
    encoder = pickle.load(f)

# Load model
model = load_model("models/lstm_model.h5")

MAX_LEN = 100


def predict_department(text):
    sequence = tokenizer.texts_to_sequences([text])

    padded = pad_sequences(
        sequence,
        maxlen=MAX_LEN,
        padding="post"
    )

    prediction = model.predict(padded, verbose=0)

    index = np.argmax(prediction)

    return encoder.inverse_transform([index])[0]


if __name__ == "__main__":
    complaint = input("Enter complaint: ")

    result = predict_department(complaint)

    print("Predicted Department:", result)