# ============================================================================
# Simple HTTP Server for Document Summarizer
# Uses only Python built-in modules - NO external dependencies!
# ============================================================================

import http.server
import json
import os
import tempfile
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Import RAG components (these should already be installed)
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
PORT = 5000
HOST = '127.0.0.1'

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
    
    rag_template = """
        You are a document summarization and study assistant.
        You must answer ONLY using the information retrieved from the document.
        Do NOT add external knowledge.
        The size of the output should be proportional to the size of the input document. Not too short, include all the important details even if the output is long.
        If something is not in the document, do not invent it.
        and don't forget the exam questions and answers at the end. It's the most important part.

        Language: French

        Your goal is to produce a study-ready summary for exam preparation.

        ========================
        TASK 1: Structured Summary
        ========================

        Write a clear, explanatory summary of the document for a student who is learning the topic.

        Rules:
        - Use simple, clear French
        - Explain ideas as if to a beginner
        - Be detailed enough to study from
        - Use headings and subheadings
        - Keep all content strictly based on the document

        Format:

        Titre du document:
        (one clear line)

        Résumé général:
        (1 to 2 short paragraphs explaining the overall idea)

        ========================
        TASK 2: Key Topics Explained
        ========================

        Identify the main topics or sections in the document.

        For each topic, write:
        - Topic title
        - Clear explanation (4 to 8 lines)
        - Important points to remember (bullet list)

        Format:

        ### Topic 1: ...
        Explanation:
        ...
        Points clés:
        - ...
        - ...

        ### Topic 2: ...
        ...

        ========================
        TASK 3: Exam Questions
        ========================

        Create 10 to 15 exam-style questions that a teacher is likely to ask
        based ONLY on this document.

        Question types:
        - Definition questions
        - Explanation questions
        - Comparison questions
        - "Why" or "How" questions
        - Short essay questions

        Write ONLY the questions first, numbered.

        ========================
        TASK 4: Answers
        ========================

        After listing all questions, provide the answers.

        Rules:
        - Keep answers clear and structured
        - Use only information from the document
        - Do not add external examples
        - Match each answer to its question number

        ========================

        Context from document:
        {context}

        Question:
        {question}

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
# HTTP Request Handler
# ============================================================================
class DocumentSummarizerHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler for the Document Summarizer."""
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'ok'}).encode())
        else:
            # Serve static files
            super().do_GET()
    
    def do_POST(self):
        """Handle POST requests."""
        if self.path == '/api/summarize':
            self.handle_summarize()
        else:
            self.send_error(404)
    
    def do_OPTIONS(self):
        """Handle CORS preflight requests."""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def handle_summarize(self):
        """Handle document summarization request."""
        try:
            # Parse multipart form data
            content_type = self.headers['Content-Type']
            if 'multipart/form-data' not in content_type:
                self.send_json_response({'error': 'Invalid content type'}, 400)
                return
            
            # Extract boundary
            boundary = content_type.split("boundary=")[1].encode()
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            
            # Parse form data (simple parser)
            parts = body.split(b'--' + boundary)
            filename = None
            file_data = None
            
            for part in parts:
                if b'Content-Disposition' in part:
                    if b'filename=' in part:
                        # Extract filename
                        lines = part.split(b'\r\n')
                        for line in lines:
                            if b'filename=' in line:
                                filename = line.split(b'filename="')[1].split(b'"')[0].decode()
                                # Extract file data
                                file_data = part.split(b'\r\n\r\n')[1].rsplit(b'\r\n', 1)[0]
                                break
            
            if not filename or not file_data:
                self.send_json_response({'error': 'No file provided'}, 400)
                return
            
            if not allowed_file(filename):
                self.send_json_response({'error': 'Invalid file type'}, 400)
                return
            
            if len(file_data) > 10 * 1024 * 1024:
                self.send_json_response({'error': 'File too large'}, 400)
                return
            
            # Save to temp file and process
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(filename).suffix) as tmp:
                tmp.write(file_data)
                tmp_path = tmp.name
            
            try:
                print(f"Processing: {filename}")
                
                # Load document
                documents = load_document(tmp_path)
                if not documents:
                    self.send_json_response({'error': 'Could not extract text'}, 400)
                    return
                
                # Split into chunks
                chunks = split_documents(documents)
                
                # Create vector database
                vector_db = create_vector_db(chunks)
                
                # Setup and run RAG chain
                chain = setup_rag_chain(vector_db)
                summary = chain.invoke(input="Summarize the document.")
                
                # Send response
                self.send_json_response({
                    'summary': summary,
                    'filename': filename,
                    'status': 'success'
                })
            
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
        
        except Exception as e:
            print(f"Error: {str(e)}")
            self.send_json_response({'error': f'Summarization failed: {str(e)}'}, 500)
    
    def send_json_response(self, data, status=200):
        """Send a JSON response."""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())
    
    def end_headers(self):
        """Add CORS headers to all responses."""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

# ============================================================================
# Main
# ============================================================================
if __name__ == '__main__':
    server_address = (HOST, PORT)
    httpd = http.server.HTTPServer(server_address, DocumentSummarizerHandler)
    
    print("=" * 70)
    print("Document Summarizer - Simple Server")
    print("=" * 70)
    print(f"✅ Server running on http://{HOST}:{PORT}")
    print(f"📝 Open your browser and go to: http://localhost:{PORT}")
    print(f"⚠️  Make sure Ollama is running: ollama serve")
    print("=" * 70)
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n⛔ Server stopped")
        httpd.server_close()
