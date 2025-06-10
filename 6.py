from transformers import pipeline

sentiment_pipeline = pipeline("sentiment-analysis")

reviews = [
    "The product quality is amazing! I'm really happy with my purchase.",
    "Terrible customer service. I will not buy from here again.",
    "It was okay, not great but not terrible either.",
    "Absolutely love it! Fast shipping and great packaging.",
    "The item arrived broken and the support team was unhelpful."
]

result = sentiment_pipeline(reviews)

for review, res in zip(reviews, result):
    print(f"Review: {review}")
    print(f"Sentiment: {res['label']}")
    print(f"Confidence: {res['score']:.2f}\n")
