import json
import nltk
from nltk.stem import PorterStemmer
from typing import Dict, Any

class NLPProcessor:
    def __init__(self):
        self.stemmer = PorterStemmer()
        self.intents = self._load_intents()
    
    def _load_intents(self) -> Dict[str, Any]:
        with open('intents.json') as file:
            return json.load(file)
    
    def process_input(self, text: str) -> Dict[str, Any]:
        tokens = nltk.word_tokenize(text.lower())
        stemmed = [self.stemmer.stem(word) for word in tokens]
        
        for intent in self.intents['intents']:
            for pattern in intent['patterns']:
                if any(self.stemmer.stem(word) in stemmed for word in pattern.split()):
                    return {
                        "intent": intent['tag'],
                        "response": intent['responses'][0],
                        "code_example": intent.get('code_example', '')
                    }
        
        return {
            "intent": "unknown",
            "response": "Não entendi. Pode reformular?",
            "code_example": ""
        }
