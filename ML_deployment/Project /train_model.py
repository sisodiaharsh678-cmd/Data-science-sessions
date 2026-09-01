import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

reviews = [
    "Great product, exactly as described", "Excellent quality, very happy with purchase",
    "Works perfectly, highly recommend", "Good value for money, satisfied",
    "Fast delivery and great packaging", "Amazing product, will buy again",
    "Superb quality, worth every rupee", "Loved it, works flawlessly",
    "Best purchase I've made this year", "Very happy with this product",
    "Poor quality, stopped working in a week", "Very disappointed, product was damaged",
    "Waste of money, do not buy", "Not as described, low quality",
    "Terrible experience, requesting refund", "Product broke on first use",
    "Extremely disappointed with the quality", "Worst purchase ever, avoid this",
    "Cheap material, not worth the price", "Item arrived damaged and defective"
]

labels = ['Positive']*10 + ['Negative']*10


vectorizer = CountVectorizer()
X = vectorizer.fit_transform(reviews)

model = MultinomialNB()
model.fit(X, labels)


with open("review_sentiment_model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

