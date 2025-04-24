import pandas as pd
import joblib
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from utils import mask_pii  # Custom utility for PII masking


# Load and preprocess dataset
try:
    df = pd.read_excel("data/combined_emails_with_natural_pii.xlsx")
    df.dropna(subset=["email", "type"], inplace=True)
except FileNotFoundError:
    raise FileNotFoundError(
        "Excel file not found. Ensure the dataset exists."
    )


# Apply PII masking to email content
masked_results = df["email"].apply(mask_pii)
df["Masked_Email"] = masked_results.map(lambda x: x[0])


# Prepare data for training
X_train, X_test, y_train, y_test = train_test_split(
    df["Masked_Email"],
    df["type"],
    test_size=0.2,
    random_state=42,
)


# Vectorize email text
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)


# Train Naive Bayes classifier
model = MultinomialNB()
model.fit(X_train_vec, y_train)


# Evaluate model performance
accuracy = model.score(X_test_vec, y_test)
print(f"Model accuracy: {accuracy:.2f}")


# Save model and vectorizer
os.makedirs("model", exist_ok=True)
with open("model/classifier.pkl", "wb") as file:
    joblib.dump((model, vectorizer), file)

print("Model trained and saved as 'model/classifier.pkl'")
