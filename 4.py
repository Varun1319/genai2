import gensim.downloader as api
import openai

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
    expanded_prompt = expanded_prompt.replace(
        word, f"{word} ({', '.join(similar_words)})"
    )

print("Original Prompt:", original_prompt)
print("Enriched Prompt:", expanded_prompt)

openai.api_key = ""
#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

import openai

client = openai.OpenAI(api_key=" ")

response_enriched = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": expanded_prompt}]
)

response_original = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": original_prompt}]
)

print("\nResponse to original prompt:\n", response_original.choices[0].message.content)
print("\nResponse to enriched prompt:\n", response_enriched.choices[0].message.content)
