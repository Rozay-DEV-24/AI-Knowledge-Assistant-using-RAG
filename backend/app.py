import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from dotenv import load_dotenv
import json
import ingest
from core.logic import get_rag_answer
from core.logic import get_rag_answer_stream

load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Question not provided."}), 400

    question = data['question']
    # --- NEW: Get history from the request, default to an empty list ---
    history = data.get('history', [])
    
    print(f"Received question: {question}")
    print(f"History: {history}")
    
    # Pass the history to our logic function
    return Response(get_rag_answer_stream(question, history), mimetype='text/event-stream')

@app.route('/query', methods=['POST'])
def handle_query():
    # ... (data validation is the same)
    
    question = data['question']
    print(f"Received question: {question}")
    
    # Use the streaming function and return the generator as a response
    return Response(get_rag_answer_stream(question), mimetype='text/event-stream')

@app.route('/ingest', methods=['POST'])
def ingest_data():
    try:
        print("Ingestion process started...")
        ingest.create_vector_db()
        print("Ingestion process finished.")
        return jsonify({"status": "success", "message": "Data ingestion complete."})
    except Exception as e:
        print(f"Error during ingestion: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/query', methods=['POST'])
def handle_query():
    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Question not provided."}), 400

    question = data['question']
    print(f"Received question: {question}")
    
    try:
        # --- MODIFIED PART ---
        # The function now returns a dictionary, which we can directly jsonify
        result = get_rag_answer(question)
        return jsonify(result)
        # ---------------------
    except Exception as e:
        print(f"Error during query: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)