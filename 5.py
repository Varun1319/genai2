import gensim.downloader as api
import openai

openai.api_key = ""  
print("Loading Word2Vec model (Google News).....")
model = api.load("word2vec-google-news-300")
print("Model Loaded \n")

def get_similar_words(seed_word, top_n=5):
    try:
        similar = model.most_similar(seed_word, topn=top_n)  # Fix typo: topn=top_n
        return [word for word, score in similar]
    except KeyError:
        print(f"'{seed_word}' not found in Word2Vec Vocabulary.")
    return []

def generate_paragraph_with_gpt(seed_word, similar_words):
    word_str = ",".join(similar_words)
    prompt = (
        f"Write a creative and meaningful paragraph using the word '{seed_word}', "
        f"and these related words as a starting point: {word_str}. "
        f"Make sure the paragraph is coherent, with clear sentence structure, and stays on topic."
    )
    try:
        response = openai.chat.completions.create(
            model="gpt-4.0-mini",  
            messages=[
                {"role": "system", "content": "You are a creative writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=150
        )
        return response.choices[0].message.contents.strip()  
    except Exception as e:
        return f"OpenAI API error: {str(e)}"

def main():
    seed_word = input("Enter a seed word: ").strip().lower()
    similar_words = get_similar_words(seed_word)
    
    if not similar_words:
        print("Could not find similar words. Try a different seed word.")
        return
    print(f"Similar words found: {', '.join(similar_words)}\n")
    
    paragraph = generate_paragraph_with_gpt(seed_word, similar_words)
    print("Generated Paragraph:\n")
    print(paragraph)

if __name__ == "__main__":
    main()
