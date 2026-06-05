import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from config import CUSTOM_STOPWORDS

nltk.download("stopwords")
nltk.download("wordnet")

lemmatizer = WordNetLemmatizer()

stop_words = set(stopwords.words("english"))
stop_words.update(CUSTOM_STOPWORDS)


def remove_urls(text):
    return re.sub(r"http\S+|www\S+", "", text)


def remove_emails(text):
    return re.sub(r"\S+@\S+", "", text)


def remove_phone_numbers(text):
    return re.sub(r"\d{10}", "", text)


def remove_html(text):
    return re.sub(r"<.*?>", "", text)


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def remove_stopwords(words):
    return [word for word in words if word not in stop_words]


def lemmatize_words(words):
    return [lemmatizer.lemmatize(word) for word in words]


def clean_text(text):
    """
    Main text preprocessing function
    """

    if not isinstance(text, str):
        return ""

    text = text.lower()

    text = remove_urls(text)
    text = remove_emails(text)
    text = remove_phone_numbers(text)
    text = remove_html(text)
    text = remove_punctuation(text)

    words = text.split()

    words = remove_stopwords(words)
    words = lemmatize_words(words)

    return " ".join(words)