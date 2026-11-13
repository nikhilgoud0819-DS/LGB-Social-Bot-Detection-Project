import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


# Load Dataset
df = pd.read_csv("../dataset/bot_detection_data.csv")

# Remove empty tweets
df = df.dropna(subset=["Tweet"])


# Input and Output
X = df["Tweet"]
y = df["Bot Label"]


# Text Vectorization
vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=10000,
    ngram_range=(1,2)
)


X_vectorized = vectorizer.fit_transform(X)


# Split Dataset
X_train, X_test, y_train, y_test = train_test_split(
    X_vectorized,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# Improved Model
model = LogisticRegression(
    class_weight="balanced",
    max_iter=1000
)


# Training
model.fit(X_train, y_train)


# Testing
predictions = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    predictions
)


print("Accuracy:", round(accuracy * 100,2), "%")


print("\nClassification Report:")
print(
    classification_report(
        y_test,
        predictions
    )
)


# Save Model
joblib.dump(
    model,
    "bot_model.pkl"
)


joblib.dump(
    vectorizer,
    "vectorizer.pkl"
)


print("\nModel Updated Successfully!")