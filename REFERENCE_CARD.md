# 📋 Quick Reference Card

## 🚀 Commands Cheat Sheet

### Initial Setup

```bash
# Install all dependencies
pip install -r requirements.txt

# Verify installation
pip list | findstr langchain flask chromadb
```

### Running the Application

**Terminal 1 - Ollama Server**

```bash
ollama serve
# Keep this running in the background
```

**Terminal 2 - Flask Backend**

```bash
cd c:\Users\DELL\Desktop\llm
python app.py
# Output: Server running on http://localhost:5000
```

**Browser**

```
http://localhost:5000
```

### Optional: Pull Additional Models

```bash
# List available models
ollama list

# Pull new model
ollama pull mistral
ollama pull neural-chat
ollama pull codellama

# Remove unused model
ollama rm llama3.2
```

---

## 📁 File Guide

| File               | Purpose        | Edit?                     |
| ------------------ | -------------- | ------------------------- |
| `index.html`       | Web interface  | Design changes            |
| `styles.css`       | Styling        | Colors, fonts, animations |
| `script.js`        | Frontend logic | Upload, download behavior |
| `app.py`           | Backend API    | Prompt, models, config    |
| `requirements.txt` | Dependencies   | Add/remove packages       |
| `QUICKSTART.md`    | Setup guide    | ❌ Read only              |
| `README.md`        | Documentation  | ❌ Read only              |

---

## 🎨 Common Customizations

### Change Primary Color (Cyan → Purple)

Edit `styles.css`:

```css
--primary-color: #8338ec; /* Was #00d4ff */
```

### Change Model

Edit `app.py`:

```python
MODEL = "mistral"  # Was "llama3.2"
```

### Change Summary Style

Edit `app.py` `rag_template` (around line 108):

```python
rag_template = """Your custom prompt"""
```

### Change Port

Edit `app.py` (last line):

```python
app.run(debug=True, host='127.0.0.1', port=8000)  # Was 5000
```

---

## 🔍 Troubleshooting Quick Fixes

### "Address already in use"

```bash
# Find process on port 5000
netstat -ano | findstr :5000

# Kill it (replace PID with actual number)
taskkill /PID <PID> /F
```

### "Models not found"

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

### "Import error"

```bash
pip install --upgrade langchain langchain-ollama
```

### "CORS error"

✅ Already fixed in `app.py` with `CORS(app)`

---

## 📊 API Reference

### GET `/`

Returns `index.html` interface

### GET `/api/health`

Check if backend is running

```json
{ "status": "ok" }
```

### POST `/api/summarize`

Upload document and get summary

**Request:**

```
Content-Type: multipart/form-data
Body: file=[binary]
```

**Response (Success):**

```json
{
  "summary": "Title: ...\nSummary: ...\nKey takeaway: ...",
  "filename": "document.pdf",
  "status": "success"
}
```

**Response (Error):**

```json
{
  "error": "Error message"
}
```

---

## 🎯 Configuration Options

```python
# In app.py:

MODEL = "llama3.2"
# Available: llama3.2, mistral, neural-chat, codellama

EMBEDDING_MODEL = "nomic-embed-text"
# Smaller options: all-minilm (faster but less accurate)

CHUNK_SIZE = 1200
# Smaller = faster, larger = more context

CHUNK_OVERLAP = 300
# Overlap between chunks

RETRIEVAL_K = 5
# Number of chunks to retrieve

COLLECTION_NAME = "simple-rag"
# Vector database collection name
```

---

## 📱 Browser Testing

### Test on Mobile

Press `F12` → `Ctrl+Shift+M` (or Cmd+Shift+M on Mac)

### Test Different Sizes

```
Mobile: 375px
Tablet: 768px
Desktop: 1024px+
```

---

## 🐍 Python Version

```bash
# Check Python version
python --version
# Required: 3.9+

# Create virtual environment (if not using .venv)
python -m venv venv
venv\Scripts\activate
```

---

## 📦 Key Dependencies

```
Flask==2.3.0          # Web framework
langchain==0.0.300    # RAG orchestration
chromadb==0.3.0       # Vector database
ollama==0.1.0         # Local LLM
unstructured==0.7.0   # Document parsing
python-docx==0.8.11   # Word export
```

---

## 🎓 Learning Path

1. **Understand the flow** → Read ARCHITECTURE.md
2. **Run the app** → Follow QUICKSTART.md
3. **Customize styling** → Edit styles.css
4. **Modify prompt** → Edit app.py rag_template
5. **Advanced features** → Read TIPS_AND_TRICKS.md

---

## 📝 File Upload Limits

```
Max Size: 10 MB
Allowed Types: PDF, TXT, DOCX

Timeout: ~5 minutes per document
```

---

## 🎨 Color Palette

```
Primary (Cyan):      #00d4ff
Secondary (Magenta): #ff006e
Accent (Purple):     #8338ec
Dark Background:     #0a0e27
Light Text:          #ffffff
Dim Text:            #b0b5c0
Success (Green):     #00ff88
Error (Red):         #ff4757
```

---

## 📊 Performance Targets

```
Setup Time:          ~2 minutes
App Load Time:       <1 second
Upload Processing:   ~30 seconds (first run)
Summarization:       15 seconds - 5 minutes
                     (depends on document size)
```

---

## 🔐 Security Checklist

✅ File type validated
✅ File size limited
✅ CORS configured
✅ Input sanitized
✅ Temp files cleaned
✅ No external APIs
✅ Local processing only

---

## 🚨 Common Errors

| Error              | Cause                     | Fix                         |
| ------------------ | ------------------------- | --------------------------- |
| Connection refused | Ollama not running        | `ollama serve`              |
| Model not found    | Missing model             | `ollama pull llama3.2`      |
| Port 5000 in use   | Another app using it      | Kill process or change port |
| Out of memory      | Document too large        | Reduce CHUNK_SIZE           |
| CORS error         | Frontend/backend mismatch | Check base URL              |
| Blank page         | JS error                  | Check console (F12)         |

---

## 💾 Save Your Work

### Backup Config

```bash
# Copy all settings before major changes
copy app.py app.py.backup
copy styles.css styles.css.backup
```

### Reset to Defaults

```bash
# Restore from git
git checkout app.py
git checkout styles.css
```

---

## 🌐 Local Network Access

To access from another computer on your network:

1. Find your IP: `ipconfig | findstr IPv4`
2. In `app.py`, change:
   ```python
   app.run(host='0.0.0.0')  # Instead of '127.0.0.1'
   ```
3. Access from other computer: `http://YOUR_IP:5000`

---

## 📚 Documentation Index

- **GETTING_STARTED.md** ← You are here
- **QUICKSTART.md** - Setup instructions
- **README.md** - Full documentation
- **ARCHITECTURE.md** - System design
- **TIPS_AND_TRICKS.md** - Advanced features
- **IMPLEMENTATION_SUMMARY.md** - What was built

---

## 🎉 You're All Set!

Everything is ready. Just run:

```bash
ollama serve              # Terminal 1
python app.py             # Terminal 2
# Then open http://localhost:5000
```

---

**Version:** 1.0
**Created:** January 2026
**Status:** Production Ready ✅
