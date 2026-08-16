import os
import re
import string
import joblib
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from django.conf import settings
nltk.download("stopwords", quiet=True)
nltk.download("wordnet", quiet=True)
nltk.download("omw-1.4", quiet=True)

MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    "ml_models",
    "xgboost_model.pkl"
)
VECTORIZER_PATH = os.path.join(
    settings.BASE_DIR,
    "ml_models",
    "tfidf_vectorizer.pkl"
)
model = joblib.load(MODEL_PATH)
tfidf = joblib.load(VECTORIZER_PATH)
stop_words = set(
    stopwords.words("english")
)
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text)
    text = text.lower()
    text = BeautifulSoup(
        text,
        "html.parser"
    ).get_text()
    text = re.sub(
        r"http\S+|www\S+",
        " ",
        text
    )
    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )
    text = re.sub(
        r"\d+",
        " ",
        text
    )
    text = text.translate(
        str.maketrans(
            "",
            "",
            string.punctuation
        )
    )
    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()
    words = text.split()
    words = [
        lemmatizer.lemmatize(word)
        for word in words
        if word not in stop_words
    ]
    return " ".join(words)

def predict_fake_news(title, content):
    combined_text = f"{title} {content}"
    cleaned_text = clean_text(
        combined_text
    )
    vectorized_text = tfidf.transform(
        [cleaned_text]
    )
    prediction = model.predict(
        vectorized_text
    )[0]
    probability = model.predict_proba(
        vectorized_text
    )[0][1]
    if int(prediction) == 1:
        label = "fake"
    else:
        label = "real"
    return label, float(probability)