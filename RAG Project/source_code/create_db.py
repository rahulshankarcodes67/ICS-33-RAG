from langchain.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import shutil
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores.chroma import Chroma
import argparse
from dataclasses import dataclass
from langchain.prompts import ChatPromptTemplate



DATA_PATH = "/Users/rahul/Desktop/RAG Project/data_files"
CHROMA_PATH = "/Users/rahul/Desktop/RAG Project/chroma/chroma"


PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---
Answer the question based on the above context:{question}
"""
def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    loader = DirectoryLoader(DATA_PATH,glob = "*.md")
    documents = loader.load()
    return documents 

def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 1000,
        chunk_overlap = 500,
        length_function = len,
        add_start_index = True,
    )

    chunks  = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")
    return chunks 

def save_to_chroma(chunks):
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)
    db = Chroma.from_documents(chunks,OpenAIEmbeddings(openai_api_key= ""
),persist_directory=CHROMA_PATH)
    db.persist()


if __name__ == "__main__":
    main()