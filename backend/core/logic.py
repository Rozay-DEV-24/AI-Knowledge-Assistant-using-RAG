# import os
# import google.generativeai as genai
# from langchain.vectorstores import Chroma
# from langchain.embeddings import HuggingFaceEmbeddings
# from langchain.prompts import PromptTemplate

# # --- Configuration ---
# DB_PATH = "../db/"
# EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# # Configure the Gemini API
# genai.configure(api_key=GOOGLE_API_KEY)

# # --- Initialize models and vector store ---
# embeddings = HuggingFaceEmbeddings(
#     model_name=EMBEDDING_MODEL,
#     model_kwargs={'device': 'cpu'}
# )

# db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

# prompt_template = """
# Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer.

# Context:
# {context}

# Question: {question}

# Helpful Answer:
# """
# PROMPT = PromptTemplate(
#     template=prompt_template, input_variables=["context", "question"]
# )

# llm = genai.GenerativeModel('gemini-2.5-pro')

# def get_rag_answer_stream(question):
#     """
#     A generator function that yields the answer token by token with sources.
#     """
#     print("Searching for relevant documents...")
#     retrieved_docs = db.similarity_search(question, k=3)
    
#     # --- This part is new: We will yield the sources first ---
#     sources = []
#     if retrieved_docs:
#         sources = list(set([doc.metadata.get('source', 'Unknown') for doc in retrieved_docs]))
#         # Yield sources as a special JSON object
#         yield f"SOURCES:{json.dumps(sources)}\n"

#     # --- Now, stream the LLM response ---
#     context = "\n\n".join([doc.page_content for doc in retrieved_docs])
#     prompt_with_context = PROMPT.format(context=context, question=question)

#     print("Generating answer with Gemini...")
#     # Use the stream=True parameter
#     responses = llm.generate_content(prompt_with_context, stream=True)
    
#     for response in responses:
#         # Yield each chunk of the response text
#         yield response.text

# def get_rag_answer(question):
#     """
#     Retrieves documents, generates an answer, and returns the answer with sources.
#     """
#     print("Searching for relevant documents...")
#     retrieved_docs = db.similarity_search(question, k=3)

#     if not retrieved_docs:
#         print("No relevant documents found. Asking Gemini directly.")
#         response = llm.generate_content(question)
#         # --- MODIFIED PART ---
#         return {"answer": response.text, "sources": []}
#         # ---------------------

#     # --- NEW PART: EXTRACT SOURCES ---
#     # Get the source file path from metadata and remove duplicates
#     sources = set([doc.metadata.get('source', 'Unknown') for doc in retrieved_docs])
#     # ---------------------------------
    
#     context = "\n\n".join([doc.page_content for doc in retrieved_docs])
#     prompt_with_context = PROMPT.format(context=context, question=question)

#     print("Generating answer with Gemini...")
#     response = llm.generate_content(prompt_with_context)
    
#     # --- MODIFIED PART: RETURN DICTIONARY ---
#     return {"answer": response.text, "sources": list(sources)}
#     # ----------------------------------------

import os
import json
import google.generativeai as genai
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.prompts import PromptTemplate

# --- Configuration (is the same) ---
DB_PATH = "../db/"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

# --- Models and DB (is the same) ---
embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
    model_kwargs={'device': 'cpu'}
)
db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
llm = genai.GenerativeModel('gemini-1.0-pro')

# --- NEW: Updated Prompt Template ---
# The template now includes a placeholder for chat history
prompt_template = """
You are a helpful AI assistant. Use the following pieces of context from a knowledge base and the chat history to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Chat History:
{chat_history}

Context:
{context}

Question: {question}

Helpful Answer:
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["chat_history", "context", "question"]
)

# --- MODIFIED: The main logic function now accepts history ---
def get_rag_answer_stream(question, history):
    """
    A generator function that yields the answer token by token with sources,
    considering the chat history.
    """
    print("Searching for relevant documents...")
    # The search is still based on the latest question
    retrieved_docs = db.similarity_search(question, k=3)
    
    sources = []
    if retrieved_docs:
        sources = list(set([doc.metadata.get('source', 'Unknown') for doc in retrieved_docs]))
        yield f"SOURCES:{json.dumps(sources)}\n"

    # --- NEW: Format the chat history for the prompt ---
    formatted_history = "\n".join(history)
    
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])
    
    # The prompt now includes the formatted history
    prompt_with_context = PROMPT.format(
        chat_history=formatted_history, 
        context=context, 
        question=question
    )

    print("Generating answer with Gemini...")
    responses = llm.generate_content(prompt_with_context, stream=True)
    
    for response in responses:
        yield response.text