import pickle

with open("data/intent_model.pkl", "rb") as f:
    model = pickle.load(f)

def detect_intent(command):
    prediction = model.predict([command.lower()])
    return prediction[0]