import json
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

stemmer = PorterStemmer()

def main():
    with open('intents.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    texts = []
    labels = []

    for intent in data['intents']:
        tag = intent['tag']
        for pattern in intent['patterns']:
            tokens = nltk.word_tokenize(pattern.lower())
            tokens_stemmed = [stemmer.stem(t) for t in tokens]
            joined = " ".join(tokens_stemmed)
            texts.append(joined)
            labels.append(tag)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)
    y = labels

    clf = LogisticRegression()
    clf.fit(X, y)

    joblib.dump(vectorizer, 'vectorizer.joblib')
    joblib.dump(clf, 'intent_model.joblib')
    print("Modelo de intenções treinado e salvo: intent_model.joblib, vectorizer.joblib")

if __name__ == "__main__":
    nltk.download('punkt') 
    main()
