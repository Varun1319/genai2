# 1. Install (if you haven't already)
pip install langchain cohere langchain-community google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client

# 2. Mount Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 3. Load document
# Update the file_path to reflect the location in your mounted Google Drive
# Assuming your file is located in the root of your Google Drive in a folder named "AI & ML/Car_Gearbox"
file_path = '/content/drive/MyDrive/car.txt'
with open(file_path, 'r') as file:
    document_text = file.read()

# 4. Set up Cohere LLM
import os
from langchain.llms import Cohere

os.environ["COHERE_API_KEY"] = "o6DdGd0awe4vhcOEBS4r3RJOt0PdNB4iC60lIE40"
llm = Cohere(cohere_api_key=os.getenv("COHERE_API_KEY"))

# 5. Create PromptTemplate
from langchain.prompts import PromptTemplate

prompt = PromptTemplate(
    input_variables=["document"],
    template="""
You are a helpful assistant.
Given the following document, summarize it in **bullet points**:
---
{document}
---
Summary:
"""
)

# 6. Create LLMChain
from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt)

# 7. Run the chain
response = chain.run(document=document_text)

# 8. Output
print(response)
