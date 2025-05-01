from langchain_openai import OpenAIEmbeddings 
import os


def get_embedding_function():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Please set the OPENAI_API_KEY environment variable")
    return OpenAIEmbeddings(openai_api_key=api_key)