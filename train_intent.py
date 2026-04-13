import json
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

#loaad data
with open('data/intent.json') as f:
    data = json.load(f)

X=[]
y=[]

for intent in data['intents']:
    for example in intent['examples']:
        X.append(example.lower())
        y.append(intent['tag'])

print(f"Total training examples: {len(X)}")

#model create
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

#train model
model.fit(X,y)
print("Model training completed.")

#save model
with open("data/intent_model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to data/intent_model.pkl")