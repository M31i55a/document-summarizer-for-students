# 📄 Document Summarizer - AI Powered

A beautiful, futuristic web interface for summarizing documents using RAG (Retrieval Augmented Generation) and LLMs. Upload a document and get an instant, structured summary with download options.

## ✨ Features

🎨 **Beautiful UI** - Modern, responsive design with smooth animations and glassmorphic effects

📄 **Multiple Formats** - Upload PDF, TXT, or DOCX files

📋 **Structured Summaries** - Get professionally formatted summaries with:

- Title
- 3-5 key bullet points
- One-sentence key takeaway

💾 **Download Options** - Export summaries as .TXT or .DOCX

🚀 **Fast Processing** - Real-time document analysis with visual progress

🔒 **Privacy First** - All processing done locally using Ollama — your documents never leave your machine

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Backend**: Flask, Python
- **RAG/LLM**: LangChain, Ollama, ChromaDB
- **Document Processing**: Unstructured, pdfplumber
- **Export**: python-docx (for .DOCX generation)

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.9+
- Ollama installed and running

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Make sure Ollama is running

Pull the required models:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Start Ollama server:

```bash
ollama serve
```

### 4. Run the Application

```bash
python app.py
```

The server will start at **http://localhost:5000**

### 5. Open in Browser

Navigate to `http://localhost:5000` and start summarizing documents!

## 📂 Project Structure

```
.
├── index.html          # Main web interface
├── styles.css          # Beautiful futuristic styling
├── script.js           # Frontend JavaScript logic
├── app.py              # Flask backend API server
├── start1.py           # Original RAG pipeline (optional)
├── requirements.txt    # Python dependencies
├── README.md           # This file
└── data/               # Data directory
    └── BOI.pdf         # Sample PDF (if available)
```

## 📋 How it Works

1. **Document Upload** - User uploads PDF, TXT, or DOCX file
2. **Document Processing** - Backend loads and chunks the document
3. **Vector Embedding** - Chunks are converted to embeddings using nomic-embed-text
4. **Vector Storage** - Embeddings stored in ChromaDB
5. **Retrieval** - MMR (Maximal Marginal Relevance) retrieves relevant chunks
6. **Summarization** - Llama 3.2 generates structured summary using RAG
7. **Display** - Beautiful formatted results shown in browser
8. **Export** - User can download as .TXT or .DOCX

## 🎨 Output Format

The AI generates structured summaries with:

```
Title: [One short line]

Summary:
- [Bullet point 1]
- [Bullet point 2]
- [Bullet point 3]
- [Bullet point 4]
- [Bullet point 5]

Key takeaway: [One simple sentence]
```

## 🔌 API Endpoints

### GET `/`

Serves the HTML interface

### GET `/api/health`

Health check

```json
{ "status": "ok" }
```

### POST `/api/summarize`

Summarize a document

- **Request**: Multipart form-data with `file` field
- **Response**:

```json
{
  "summary": "...",
  "filename": "document.pdf",
  "status": "success"
}
```

## ⚙️ Configuration

Edit `app.py` to customize:

- `MODEL` - Change LLM model (default: llama3.2)
- `EMBEDDING_MODEL` - Change embedding model
- `CHUNK_SIZE` - Document chunk size (default: 1200)
- `CHUNK_OVERLAP` - Chunk overlap percentage
- `RETRIEVAL_K` - Number of chunks to retrieve

## 🐛 Troubleshooting

**"Connection refused" error**

- Make sure Ollama is running: `ollama serve`
- Check Flask server is running on port 5000

**"Model not found" error**

- Pull models: `ollama pull llama3.2` and `ollama pull nomic-embed-text`

**"Out of memory" error**

- Reduce `CHUNK_SIZE` in app.py
- Process smaller documents
- Close other applications

**Browser shows blank page**

- Check console (F12) for errors
- Verify Flask server is running
- Clear browser cache (Ctrl+Shift+Delete)

## 🌐 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (responsive design)

## 💡 Tips

- First run takes longer (model initialization)
- Large documents (>50 pages) may take 2-5 minutes
- All processing is local - no internet required
- Documents are processed in memory and not saved

## 📄 License

This project is licensed under the MIT License.

Built with ❤️ for students and researchers.
