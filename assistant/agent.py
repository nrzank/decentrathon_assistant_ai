from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

class Agent:
    def __init__(self):
        self.model = make_pipeline(TfidfVectorizer(), MultinomialNB())

    def train(self, questions, labels):
        self.model.fit(questions, labels)

    def predict(self, question):
        return self.model.predict([question])[0]
