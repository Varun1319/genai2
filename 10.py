import spacy

nlp = spacy.load("en_core_web_sm")


IPC_SECTIONS = {
    "302": "Section 302 IPC: Punishment for murder. Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine.",
    "375": "Section 375 IPC: Rape. This section defines what constitutes rape under Indian law.",
    "420": "Section 420 IPC: Cheating and dishonestly inducing delivery of property.",
    "376": "Section 376 IPC: Punishment for rape. Rigorous imprisonment of not less than 10 years, which may extend to life imprisonment, and a fine.",
    "124A": "Section 124A IPC: Sedition – whoever, by words or signs, brings or attempts to bring hatred or contempt against the Government shall be punished."
}


def extract_ipc_section(user_input):
    doc = nlp(user_input)
    for i, token in enumerate(doc):
        if token.like_num and token.text in IPC_SECTIONS:
            return token.text
        if "section" in token.text.lower():
            if i + 1 < len(doc):
                next_token = doc[i + 1]
                if next_token.text in IPC_SECTIONS:
                    return next_token.text
    return None


def detect_intent(user_input):
    if "section" in user_input.lower() or any(sec in user_input for sec in IPC_SECTIONS.keys()):
        return "ipc_query"
    elif "hello" in user_input.lower() or "hi" in user_input.lower():
        return "greeting"
    else:
        return "general"


def chat():
    print("IPC Chatbot: Hello! Ask me about any section of the Indian Penal Code (e.g., 'What is Section 302?').")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("IPC Chatbot: Goodbye!")
            break

        intent = detect_intent(user_input)

        if intent == "ipc_query":
            section = extract_ipc_section(user_input)
            if section:
                print(f"IPC Chatbot: {IPC_SECTIONS[section]}")
            else:
                print("IPC Chatbot: Sorry, I couldn't identify the IPC section. Please specify like 'Section 302'.")
        
        elif intent == "greeting":
            print("IPC Chatbot: Hello! Ask me about any IPC section.")
        
        else:
            print("IPC Chatbot: I can help you with information about the Indian Penal Code. Try asking about a section like 'What is Section 420?'")

if __name__ == "__main__":
    chat()
