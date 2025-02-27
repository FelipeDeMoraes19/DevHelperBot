import json
import nltk
from nltk.stem import PorterStemmer
from typing import Dict, Any
import os
import joblib

class NLPProcessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.intents = self._load_intents()
        self._load_ml_model()

    def _load_intents(self) -> Dict[str, Any]:
        with open('intents.json') as file:
            return json.load(file)

    def _load_ml_model(self):
        if os.path.exists('intent_model.joblib') and os.path.exists('vectorizer.joblib'):
            self.model = joblib.load('intent_model.joblib')
            self.vectorizer = joblib.load('vectorizer.joblib')
        else:
            self.model = None
            self.vectorizer = None

    def process_input(self, text: str) -> Dict[str, Any]:
        tokens = nltk.word_tokenize(text.lower())
        stemmed = [self.stemmer.stem(word) for word in tokens]

        if self.model and self.vectorizer:
            input_joined = " ".join(stemmed)
            X_test = self.vectorizer.transform([input_joined])
            predicted_tag = self.model.predict(X_test)[0]
            for intent in self.intents["intents"]:
                if intent["tag"] == predicted_tag:
                    return {
                        "intent": intent["tag"],
                        "response": intent["responses"][0],
                        "code_example": intent.get("code_example", "")
                    }

        for intent in self.intents["intents"]:
            for pattern in intent["patterns"]:
                if any(self.stemmer.stem(word) in stemmed for word in pattern.split()):
                    return {
                        "intent": intent["tag"],
                        "response": intent["responses"][0],
                        "code_example": intent.get("code_example", "")
                    }

        return {
            "intent": "unknown",
            "response": "Não entendi. Pode reformular?",
            "code_example": ""
        }
