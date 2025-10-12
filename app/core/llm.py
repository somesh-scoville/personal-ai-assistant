import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq
from pydantic import SecretStr

load_dotenv()


def get_llm_model():
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if groq_api_key is None:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    return ChatGroq(
        model="llama-3.3-70b-versatile", api_key=SecretStr(groq_api_key), temperature=0.0
    )


model = get_llm_model()
