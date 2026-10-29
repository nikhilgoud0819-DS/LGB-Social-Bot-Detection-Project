import joblib

model = joblib.load("bot_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


tweets = [
    "hello how are you today",
    "click here to win money instantly",
    "follow me and get free followers",
    "buy now limited offer"
]


for tweet in tweets:

    vector = vectorizer.transform([tweet])

    result = model.predict(vector)

    probability = model.predict_proba(vector)

    print(tweet)
    print("Prediction:", result[0])
    print("Confidence:", max(probability[0])*100)
    print("--------------------")