import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader, PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# --- Configuration ---
DATA_PATH = "../data/"
DB_PATH = "../db/"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

def create_vector_db():
    """
    Creates a Chroma vector database from documents in the DATA_PATH,
    searching recursively through subdirectories.
    """
    print("Loading documents from all subfolders...")
    
    # --- THIS IS THE UPDATED LINE ---
    # The glob pattern '**/*.pdf' tells the loader to look in all subdirectories for PDF files.
    loader = DirectoryLoader(DATA_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader, recursive=True)
    # ---------------------------------
    
    documents = loader.load()
    
    if not documents:
        print("No documents found. Please ensure there are PDF files in the 'data' folder and its subdirectories.")
        return

    print(f"Loaded {len(documents)} document(s) from across all folders.")

    # Split the documents into smaller chunks for better processing
    print("Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)
    print(f"Created {len(texts)} text chunks.")

    # Initialize the embedding model
    print(f"Initializing embedding model: {EMBEDDING_MODEL}")
    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={'device': 'cpu'} # Use CPU for embedding
    )

    # Create the Chroma vector store and persist it to disk
    print("Creating and persisting vector database...")
    db = Chroma.from_documents(
        texts, 
        embeddings, 
        persist_directory=DB_PATH
    )
    db.persist()
    print(f"Vector database created successfully at {DB_PATH}")

if __name__ == "__main__":
    create_vector_db()