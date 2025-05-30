
pip install langchain cohere langchain-community google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client


from google.colab import drive
drive.mount('/content/drive')


file_path = '/content/drive/MyDrive/car.txt'
with open(file_path, 'r') as file:
    document_text = file.read()


import os
from langchain.llms import Cohere

os.environ["COHERE_API_KEY"] = "o6DdGd0awe4vhcOEBS4r3RJOt0PdNB4iC60lIE40"
llm = Cohere(cohere_api_key=os.getenv("COHERE_API_KEY"))


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


from langchain.chains import LLMChain

chain = LLMChain(llm=llm, prompt=prompt)


response = chain.run(document=document_text)


print(response)
