import os

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv()) # read local .env file

import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.1)
embedder = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

# res = embedder.embed_query("What is the capital of France?")
# print(res)
# llm.bind
