📄 AI Document Intelligence (RAG)
A futuristic, full-stack RAG (Retrieval-Augmented Generation) application that transforms dense PDF documents into structured study guides. Upload a document, and let local AI generate a summary, key topics, and exam-style questions with a sleek, glassmorphic interface.

✨ Features
Smart Summarization: Automatically generates a beginner-friendly summary in French.

Knowledge Extraction: Breaks down complex topics into clear explanations and bullet points.

Exam Preparation: Generates 10-15 teacher-style questions and answers based only on the provided text.

Futuristic UI: A high-end, responsive "Cyberpunk-Glassmorphism" interface.

Multi-Format Export: Download your generated study guide as .txt or .doc.

Privacy First: Runs locally using Ollama—your documents never leave your machine.

🛠️ Tech Stack
Backend
LangChain: For RAG orchestration and document processing.

FastAPI: High-performance Python web framework for the API.

ChromaDB: Vector database for local document storage.

Ollama: Powering Llama 3.2 (LLM) and nomic-embed-text (Embeddings).

Frontend
HTML5/CSS3: Modern Glassmorphism design with CSS variables and animations.

JavaScript (Vanilla): For asynchronous API handling and dynamic DOM updates.

Marked.js: To render AI-generated Markdown into beautiful HTML.

🚀 Getting Started

1. Prerequisites
   Install Python 3.9+

Install Ollama

Pull the required models:

Bash

ollama pull llama3.2
ollama pull nomic-embed-text 2. Installation
Clone the repository and install the dependencies:

Bash

git clone https://github.com/M31i55a/document-summarizer-for-students.git
cd ai-doc-intelligence
pip install -r requirements.txt
Note: Ensure you have fastapi, uvicorn, langchain, langchain-ollama, chromadb, and unstructured installed.

3. Running the Application
   Start the Backend:

Bash

python app.py
The server will start at http://localhost:8000.

Open the Frontend: Simply open index.html in your favorite web browser.

📂 Project Structure
Plaintext

├── app.py # FastAPI Backend & RAG Logic
├── index.html # Futuristic Frontend
├── style.css # Glassmorphism Styling
├── script.js # Frontend Logic & API Integration
├── data/ # Directory for uploaded PDFs and vector store
└── README.md # Project Documentation
📝 How it Works
Ingestion: The PDF is loaded via UnstructuredPDFLoader and split into chunks of 1200 characters with a 300-character overlap.

Vectorization: Chunks are converted into embeddings using nomic-embed-text and stored in a local Chroma database.

Retrieval: When a summary is requested, the system uses MMR (Maximal Marginal Relevance) to find the most relevant and diverse parts of the document.

Generation: The Llama 3.2 model processes the context and follows a strict prompt template to generate a structured study guide in French.

🤝 Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request for new features (like multi-language support or dark/light mode toggle).

📄 License
This project is licensed under the MIT License.

Built with ❤️ for students and researchers.
