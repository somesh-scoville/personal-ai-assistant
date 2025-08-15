import os
from dotenv import load_dotenv

_ = load_dotenv()

# from langchain_openai import ChatOpenAI
# openai_model = ChatOpenAI(model= 'gpt-4o', temperature=0.0)

from langchain_groq import ChatGroq

model = ChatGroq(model='llama-3.3-70b-versatile', 
                 api_key=os.environ.get("GROQ_API_KEY"),
                 temperature=0.0)