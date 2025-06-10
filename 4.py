import gensim.downloader as api
from openai import OpenAI

word2vec_model = api.load("word2vec-google-news-300")

def get_similar_words(word, top_n=3):
    try:
        return [w for w, _ in word2vec_model.most_similar(word, topn=top_n)]
    except KeyError:
        return [word]

original_prompt = "Generate a detailed story about an astronaut exploding a distant exoplanet"
keywords = ["astronaut", "exploding", "distant", "exoplanet"]

expanded_prompt = original_prompt
for word in keywords:
    similar_words = get_similar_words(word)
    enriched = f"{word} ({', '.join(similar_words)})"
    expanded_prompt = expanded_prompt.replace(word, enriched)

print("Original Prompt:\n", original_prompt)
print("\nEnriched Prompt:\n", expanded_prompt)

client = OpenAI(api_key="")  # Replace with your valid key

response_original = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": original_prompt}]
)

response_enriched = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": expanded_prompt}]
)

print("\nResponse to Original Prompt:\n", response_original.choices[0].message.content)
print("\nResponse to Enriched Prompt:\n", response_enriched.choices[0].message.content)
