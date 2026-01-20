# ============================================================================
# Flask Backend for Document Summarizer
# ============================================================================
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import tempfile
from pathlib import Path

# Import RAG components
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ============================================================================
# Configuration
# ============================================================================
app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

MODEL = "llama3.2"
EMBEDDING_MODEL = "nomic-embed-text"
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 300
COLLECTION_NAME = "simple-rag"
RETRIEVAL_K = 5

ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx'}

# ============================================================================
# Utility Functions
# ============================================================================
def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_document(file_path: str):
    """Load document (PDF or text)."""
    file_ext = Path(file_path).suffix.lower()
    
    if file_ext == '.pdf':
        from langchain_community.document_loaders import UnstructuredPDFLoader
        loader = UnstructuredPDFLoader(file_path=file_path)
        return loader.load()
    elif file_ext == '.txt':
        from langchain_community.document_loaders import TextLoader
        loader = TextLoader(file_path=file_path, encoding='utf-8')
        return loader.load()
    elif file_ext in ['.doc', '.docx']:
        from langchain_community.document_loaders import UnstructuredWordDocumentLoader
        loader = UnstructuredWordDocumentLoader(file_path=file_path)
        return loader.load()
    else:
        raise ValueError(f"Unsupported file type: {file_ext}")

def split_documents(documents):
    """Split documents into chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    return text_splitter.split_documents(documents)

def create_vector_db(chunks):
    """Create vector database from chunks."""
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
    )
    return vector_db

def setup_rag_chain(vector_db):
    """Setup RAG chain for summarization."""
    llm = ChatOllama(model=MODEL)
    
    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": RETRIEVAL_K}
    )
    
    rag_template = """You are a document summarization assistant.
Use only the information retrieved from the document to answer. Do not add external knowledge.

Your task is to:
- Summarize the document in very simple language
- Explain the main idea as if to a beginner
- Keep the response short, clear, and direct
- Avoid unnecessary details, examples, or repetition

Output format (strict):
Title: one short line
Summary: 3–5 bullet points, one sentence each
Key takeaway: one simple sentence

Style rules:
- Use plain language
- Short sentences
- No technical jargon unless it appears in the document
- No extra commentary

Context from document:
{context}

Question: {question}
"""
    
    prompt = ChatPromptTemplate.from_template(rag_template)
    
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return chain

# ============================================================================
# Routes
# ============================================================================

@app.route('/')
def index():
    """Serve the main HTML file."""
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files (CSS, JS)."""
    return send_from_directory('.', path)

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """Summarize uploaded document."""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Please upload PDF, TXT, or DOCX'}), 400
        
        # Save file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_file:
            file.save(tmp_file.name)
            tmp_path = tmp_file.name
        
        try:
            # Load document
            print(f"Loading document: {file.filename}")
            documents = load_document(tmp_path)
            
            if not documents:
                return jsonify({'error': 'Could not extract text from document'}), 400
            
            # Split into chunks
            print("Splitting document into chunks...")
            chunks = split_documents(documents)
            
            # Create vector database
            print("Creating vector database...")
            vector_db = create_vector_db(chunks)
            
            # Setup RAG chain
            print("Setting up RAG chain...")
            chain = setup_rag_chain(vector_db)
            
            # Generate summary
            print("Generating summary...")
            summary = chain.invoke(input="Summarize the document.")
            
            return jsonify({
                'summary': summary,
                'filename': file.filename,
                'status': 'success'
            })
        
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': f'Summarization failed: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500

# ============================================================================
# Main
# ============================================================================
if __name__ == '__main__':
    print("Starting Document Summarizer Backend...")
    print("Server running on http://localhost:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
