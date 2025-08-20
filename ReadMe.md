## Secure AI Knowledge Assistant
A private, secure, and conversational AI assistant that allows you to chat with your own documents. Built with Python, Flask, Gemini, and Docker.

This project is a complete implementation of a Retrieval-Augmented Generation (RAG) pipeline, creating a "ChatGPT for your own data." It allows users to ask questions in natural language and receive answers that are grounded in a private library of documents, ensuring that no sensitive data is ever exposed.

## Key Features
🔒 Secure & Private: All document processing and embedding happens locally. Only relevant text snippets are sent to the LLM, never the full documents.

💬 Conversational Memory: Remembers the last few turns of the conversation to answer follow-up questions.

⚡ Real-Time Streaming: AI responses are streamed token-by-token for a smooth, interactive user experience.

📚 Source Citation: Every answer is accompanied by the source documents it was based on, allowing for easy verification.

📄 PDF Support: Ingests and processes PDF documents recursively from a data folder.

🐳 Dockerized for Production: Comes with a Dockerfile for easy, secure, and scalable deployment.

## Architecture Overview

The application follows a Retrieval-Augmented Generation (RAG) architecture:

Ingestion: Documents in the /data folder are loaded, split into chunks, and converted into numerical vectors (embeddings) using a local sentence-transformers model. These vectors are stored in a local ChromaDB vector database.

Retrieval: When a user asks a question, it is also converted into a vector. The system performs a similarity search in the vector database to find the most relevant document chunks.

Generation: The user's question, the chat history, and the retrieved document chunks are combined into a prompt that is sent to the Gemini API. The AI generates an answer based on the provided context, which is then streamed back to the user.

## Tech Stack
Category

Technology

Backend

Python, Flask, Gunicorn

AI/ML

Google Gemini API, LangChain, SentenceTransformers

Database

ChromaDB (Vector Store)

Frontend

HTML, CSS, JavaScript (vanilla)

Deployment

Docker

## Setup and Installation
## Prerequisites:

Python 3.8+

Docker Desktop

1. Clone the Repository

git clone https://github.com/your-username/ai-knowledge-assistant.git
cd ai-knowledge-assistant

2. Backend Setup

# Install required packages
pip install -r requirements.txt

# Create a .env file in the /backend directory
# Add your Google API key to it
echo 'GOOGLE_API_KEY="YOUR_API_KEY_HERE"' > backend/.env

3. Add Your Documents
Place your PDF files inside the /data directory. You can create subfolders as needed.

4. Run the Ingestion Script
This will process your documents and create the local vector database.

cd backend
python ingest.py
cd ..

Usage
Development Mode
Start the Backend Server:

cd backend
python app.py

Open the Frontend:
Navigate to the /frontend directory and open index.html in your web browser.

Production Mode (Docker)
Build the Docker Image:
From the project root directory, run:

docker build -t knowledge-assistant .

Run the Docker Container:
Replace "YOUR_API_KEY_HERE" with your actual key.

docker run -p 5000:5000 -e GOOGLE_API_KEY="YOUR_API_KEY_HERE" --name my-assistant knowledge-assistant

The application will be accessible through the same index.html file, which will now communicate with the containerized backend.
