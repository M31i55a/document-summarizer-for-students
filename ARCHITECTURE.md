# Architecture & Flow Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        USER BROWSER                             │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │             Beautiful Futuristic UI                      │   │
│  │  ┌──────────────┐      ┌──────────────┐                 │   │
│  │  │ Upload Area  │      │ Results Area │                 │   │
│  │  │              │  OR  │              │                 │   │
│  │  │ Drag & Drop  │      │ Summary View │                 │   │
│  │  └──────────────┘      └──────────────┘                 │   │
│  │                                                          │   │
│  │  Files: .pdf, .txt, .docx                               │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────────┘
                       │ HTTP POST /api/summarize
                       │ (FormData with file)
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FLASK BACKEND (app.py)                       │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  API Endpoints:                                          │   │
│  │  • GET  /           → Serve index.html                   │   │
│  │  • GET  /api/health → Health check                       │   │
│  │  • POST /api/summarize → Process document                │   │
│  └──────────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │  File Validation:                                        │   │
│  │  • Check file type (PDF, TXT, DOCX)                      │   │
│  │  • Check file size (max 10MB)                            │   │
│  │  • Save to temporary location                            │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RAG PIPELINE (LangChain)                      │
│                                                                 │
│  ┌─ Document Loading ──────────────────────────────────────┐   │
│  │  • UnstructuredPDFLoader (for .pdf)                     │   │
│  │  • TextLoader (for .txt)                               │   │
│  │  • UnstructuredWordDocumentLoader (for .docx)          │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│  ┌─ Text Splitting ──────▼────────────────────────────────┐   │
│  │  • RecursiveCharacterTextSplitter                      │   │
│  │  • Chunk Size: 1200 characters                         │   │
│  │  • Overlap: 300 characters                             │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│  ┌─ Vector Embedding ────▼────────────────────────────────┐   │
│  │  • Model: nomic-embed-text                             │   │
│  │  • Via: Ollama                                         │   │
│  │  • Converts text to vectors                            │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│  ┌─ Vector Storage ──────▼────────────────────────────────┐   │
│  │  • ChromaDB (local vector database)                    │   │
│  │  • Collection: "simple-rag"                            │   │
│  │  • Stores embeddings & chunks                          │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│  ┌─ Retrieval ───────────▼────────────────────────────────┐   │
│  │  • Search Type: MMR (Maximal Marginal Relevance)       │   │
│  │  • K: 5 (retrieve 5 most relevant chunks)              │   │
│  │  • Context: Retrieved document excerpts                │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│  ┌─ Prompt Template ─────▼────────────────────────────────┐   │
│  │  You are a document summarization assistant.           │   │
│  │  Use ONLY retrieved information.                       │   │
│  │  Summarize in simple language.                         │   │
│  │  Output format:                                        │   │
│  │    Title: [one line]                                   │   │
│  │    Summary: [3-5 bullets]                              │   │
│  │    Key takeaway: [one sentence]                        │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
│  ┌─ LLM Processing ──────▼────────────────────────────────┐   │
│  │  • Model: Ollama (llama3.2)                            │   │
│  │  • Input: Context + Prompt Template                    │   │
│  │  • Output: Structured Summary                          │   │
│  └────────────────────────┬────────────────────────────────┘   │
│                           │                                     │
└───────────────────────────┼──────────────────────────────────────┘
                            │
                            ▼ JSON Response
┌─────────────────────────────────────────────────────────────────┐
│                    BROWSER (JavaScript)                         │
│  • Receive summary JSON                                         │
│  • Parse and format                                             │
│  • Display in beautiful UI                                      │
│  • Provide download options                                     │
└─────────────────────────────────────────────────────────────────┘
```

## Request/Response Flow

```
┌──────────────────────────────────────────────────────────┐
│                     USER INTERACTION                     │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
         ┌───────────────────────┐
         │  File Selected/Dropped│
         └───────────┬───────────┘
                     │
                     ▼
    ┌────────────────────────────────┐
    │  Show Loading Spinner          │
    │  Start Progress Bar Animation  │
    └────────────────┬───────────────┘
                     │
                     ▼
    ┌────────────────────────────────┐
    │  POST /api/summarize           │
    │  Body: FormData(file)          │
    │  Headers: CORS enabled         │
    └────────────────┬───────────────┘
                     │
        ╔════════════╩═════════════╗
        │                          │
        ▼                          ▼
   ┌─────────────┐          ┌──────────────┐
   │ 200 OK      │          │ Error (40x/50x)
   │ {summary}   │          │ {error msg}
   └──────┬──────┘          └───────┬──────┘
          │                         │
          ▼                         ▼
    ┌──────────────┐         ┌──────────────┐
    │ Display      │         │ Show Error   │
    │ Summary      │         │ UI           │
    └──────┬───────┘         └──────┬───────┘
           │                        │
           │                        │
    ┌──────▼────────────────────────▼──────┐
    │  User Can:                           │
    │  • Download .TXT                     │
    │  • Download .DOCX                    │
    │  • Summarize Another Document        │
    └──────────────────────────────────────┘
```

## File Processing Pipeline

```
┌─────────────┐
│  User File  │
│ (PDF/TXT/..)│
└──────┬──────┘
       │
       ▼
┌──────────────────────┐
│ Browser Validation   │
│ • File type check    │
│ • Size limit (10MB)  │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────┐
│ Send via FormData    │
│ HTTP POST to /api/   │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────┐
│ Backend Validation       │
│ • MIME type check        │
│ • Size verification      │
└──────┬───────────────────┘
       │
       ▼
┌──────────────────────────┐
│ Save to Temp File        │
│ (auto-cleanup after)     │
└──────┬───────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Load Based on Extension:       │
│ .pdf → UnstructuredPDFLoader   │
│ .txt → TextLoader              │
│ .docx → WordDocumentLoader     │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Extract Text Content           │
│ Return: List[Document]         │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Split into Chunks              │
│ Size: 1200 chars               │
│ Overlap: 300 chars             │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Create Embeddings              │
│ Model: nomic-embed-text        │
│ via Ollama                      │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Store in ChromaDB              │
│ Indexed & Searchable           │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Retrieve Relevant Chunks       │
│ MMR Search, K=5                │
│ Return: Top matching context   │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Generate Summary               │
│ Input: Context + Prompt        │
│ LLM: Ollama (llama3.2)         │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Return JSON Response           │
│ {summary, filename, status}    │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ Browser Display Summary        │
│ Format & Styled HTML           │
└──────┬─────────────────────────┘
       │
       ▼
┌────────────────────────────────┐
│ User Download Options          │
│ .TXT via browser API           │
│ .DOCX via docx.js library      │
└────────────────────────────────┘
```

## Component Communication

```
        ┌─────────────────────────┐
        │   index.html            │
        │ (HTML Structure)        │
        └────────────┬────────────┘
                     │
                     │ CSS classes
                     │
        ┌────────────▼────────────┐
        │   styles.css            │
        │ (UI & Animations)       │
        └────────────┬────────────┘
                     │
                     │ DOM elements
                     │ & manipulation
                     │
        ┌────────────▼────────────┐
        │   script.js             │
        │ (Logic & API calls)     │
        └────────────┬────────────┘
                     │
                     │ HTTP requests
                     │ FormData
                     │
        ┌────────────▼────────────┐
        │   app.py (Flask)        │
        │ (REST API Server)       │
        └────────────┬────────────┘
                     │
                     │ LangChain
                     │ orchestration
                     │
        ┌────────────▼────────────┐
        │   RAG Pipeline          │
        │ (Document → Summary)    │
        └────────────┬────────────┘
                     │
                     │ JSON response
                     │
        ┌────────────▼────────────┐
        │ Display & Download      │
        │ in Browser              │
        └─────────────────────────┘
```

## Data Structures

### File Upload (FormData)

```
{
  "file": <File object>
  [binary content]
}
```

### API Response (JSON)

```json
{
  "summary": "Title: ...\nSummary: ...\nKey takeaway: ...",
  "filename": "document.pdf",
  "status": "success"
}
```

### Error Response

```json
{
  "error": "Error message describing what went wrong"
}
```

### Summary Format (Plain Text)

```
Title: Document Title Here

Summary:
- First key point
- Second key point
- Third key point
- Fourth key point
- Fifth key point

Key takeaway: One sentence summarizing the entire document
```

## Environment & Dependencies

```
System:
├── Python 3.9+
├── Ollama (running)
│   ├── llama3.2 model
│   └── nomic-embed-text model
└── Browser (modern)

Python Packages:
├── Flask (web framework)
├── Flask-CORS (cross-origin)
├── LangChain (RAG orchestration)
│   ├── langchain-core
│   ├── langchain-ollama
│   └── langchain-community
├── ChromaDB (vector store)
├── Unstructured (doc parsing)
├── python-docx (Word export)
└── ... (see requirements.txt)
```

This comprehensive architecture ensures smooth, efficient document summarization with a beautiful user experience!
