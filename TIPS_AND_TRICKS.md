# Tips, Tricks & Best Practices

## ⚡ Performance Tips

### Speed Up Summarization

1. **Use smaller documents** - 5-10 pages is ideal
2. **Reduce CHUNK_SIZE** in app.py if memory-constrained
   ```python
   CHUNK_SIZE = 800  # Default: 1200
   ```
3. **Reduce RETRIEVAL_K** for faster retrieval
   ```python
   RETRIEVAL_K = 3  # Default: 5
   ```
4. **Use SSD storage** - Faster than HDD for vector operations

### Optimize Memory Usage

1. **Close other applications** - Frees up system RAM
2. **Use appropriate chunk overlap**
   ```python
   CHUNK_OVERLAP = 200  # Smaller overlap = faster
   ```
3. **Process one document at a time** - Avoid parallel uploads

## 🎨 Customization Guide

### Change Color Scheme

Edit `styles.css`:

```css
:root {
  --primary-color: #00d4ff; /* Main accent color */
  --secondary-color: #ff006e; /* Highlight color */
  --accent-color: #8338ec; /* Accent color */
  --dark-bg: #0a0e27; /* Background */
}
```

### Change Logo/Title

Edit `index.html`:

```html
<div class="logo">
  <span class="logo-icon">⚡</span>
  <!-- Change emoji -->
  <h1>DocSummarizer</h1>
  <!-- Change name -->
</div>
```

### Customize Summarization Prompt

Edit `app.py` (around line 108):

```python
rag_template = """Your custom prompt here
{context}
{question}
"""
```

### Change Model

Edit `app.py`:

```python
MODEL = "mistral"  # or llama2, neural-chat, etc.
EMBEDDING_MODEL = "all-minilm"  # Different embedding
```

## 🔧 Advanced Configurations

### Use Different Retrieval Strategy

```python
# In app.py setup_rag_chain() function:

# Option 1: Similarity search (default: MMR)
retriever = vector_db.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

# Option 2: Similarity with score threshold
retriever = vector_db.as_retriever(
    search_type="similarity_score_threshold",
    search_kwargs={"k": 5, "score_threshold": 0.5}
)
```

### Tune Chunk Parameters

```python
# Best for long documents
CHUNK_SIZE = 2000
CHUNK_OVERLAP = 400

# Best for short documents
CHUNK_SIZE = 600
CHUNK_OVERLAP = 100

# Balanced approach
CHUNK_SIZE = 1200  # Default
CHUNK_OVERLAP = 300
```

### Multi-language Support

Create language-specific prompts:

```python
PROMPTS = {
    "en": """Your English prompt...""",
    "es": """Tu indicación en español...""",
    "fr": """Votre invite en français...""",
}
```

## 🐛 Debugging Tips

### Enable Detailed Logging

Add to `app.py`:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Then in functions:
logger.debug(f"Processing file: {filename}")
logger.debug(f"Chunks created: {len(chunks)}")
```

### Check Vector Quality

```python
# In app.py, after creating vector_db:
# Query it to see what's being retrieved
results = vector_db.similarity_search("main topic", k=3)
for result in results:
    print(result.page_content)
    print("---")
```

### Monitor Memory Usage

Add to `app.py`:

```python
import psutil

def log_memory():
    memory = psutil.virtual_memory()
    print(f"Memory used: {memory.percent}%")
```

## 📱 Responsive Design Tips

The interface is already responsive, but to test:

1. **F12 in browser** - Open DevTools
2. **Ctrl+Shift+M** - Toggle device toolbar
3. **Test on different screen sizes**:
   - Mobile: 375px width
   - Tablet: 768px width
   - Desktop: 1024px+ width

## 🔒 Security Best Practices

### File Upload Security

Already implemented in `app.py`:

- ✅ File type validation
- ✅ Size limit (10MB)
- ✅ Temporary file cleanup
- ✅ CORS restriction

### Additional Security

To add authentication:

```python
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    # Implement your auth logic
    pass

@app.route('/api/summarize', methods=['POST'])
@auth.login_required
def summarize():
    # Protected endpoint
```

## 🌐 Deployment Considerations

### For Production

1. **Use production WSGI server**:

   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set Flask to production mode**:

   ```python
   app.run(debug=False)  # Not debug=True
   ```

3. **Use environment variables**:

   ```python
   import os
   DEBUG = os.getenv('DEBUG', 'False') == 'True'
   ```

4. **Add rate limiting**:

   ```python
   from flask_limiter import Limiter
   limiter = Limiter(app, key_func=lambda: request.remote_addr)

   @limiter.limit("10 per minute")
   @app.route('/api/summarize', methods=['POST'])
   def summarize():
       ...
   ```

### Docker Deployment

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
```

## 📊 Monitoring & Analytics

### Track API Usage

```python
from datetime import datetime
api_calls = []

@app.before_request
def log_request():
    api_calls.append({
        'timestamp': datetime.now(),
        'endpoint': request.endpoint,
        'method': request.method
    })
```

### Performance Metrics

```python
import time

@app.route('/api/summarize', methods=['POST'])
def summarize():
    start_time = time.time()

    # ... processing code ...

    duration = time.time() - start_time
    print(f"Summarization took {duration:.2f} seconds")
```

## 💾 Data Persistence

### Save Summaries History

```python
import json
from pathlib import Path

HISTORY_FILE = "summaries_history.json"

def save_to_history(filename, summary):
    history = json.load(open(HISTORY_FILE)) if Path(HISTORY_FILE).exists() else []
    history.append({
        'timestamp': datetime.now().isoformat(),
        'filename': filename,
        'summary': summary
    })
    json.dump(history, open(HISTORY_FILE, 'w'))
```

## 🎓 Learning Resources

### LangChain

- https://python.langchain.com
- RAG patterns and examples
- Vector store integration

### Ollama

- https://ollama.ai
- Model management
- Local LLM deployment

### ChromaDB

- https://docs.trychroma.com
- Vector database operations
- Query optimization

### Flask

- https://flask.palletsprojects.com
- Web framework basics
- API development

## 🚀 Enhancement Ideas

### Easy Additions

- [ ] Save summaries to database
- [ ] Add summary history page
- [ ] Support more file formats (HTML, Markdown)
- [ ] Add manual prompt customization in UI
- [ ] Export to PDF format

### Medium Complexity

- [ ] User authentication
- [ ] Batch processing
- [ ] Different summarization styles (bullet, paragraph, etc.)
- [ ] Keyword extraction
- [ ] Document comparison

### Advanced Features

- [ ] Real-time collaborative summarization
- [ ] Model fine-tuning on custom data
- [ ] Multi-document summarization
- [ ] Question-answering from documents
- [ ] Document clustering and topic modeling

## 🎯 Optimization Checklist

Before going to production:

- [ ] Test with various document sizes
- [ ] Verify error handling
- [ ] Check memory leaks
- [ ] Test on different browsers
- [ ] Verify CORS configuration
- [ ] Clean up temporary files
- [ ] Add request validation
- [ ] Set up logging
- [ ] Test rate limiting
- [ ] Verify security settings

## 💡 Troubleshooting Common Issues

### "Summary is too long"

**Solution**: Reduce RETRIEVAL_K or CHUNK_SIZE

```python
RETRIEVAL_K = 3  # Was 5
CHUNK_SIZE = 800  # Was 1200
```

### "Summary seems generic"

**Solution**: Improve the prompt in app.py or increase RETRIEVAL_K

```python
RETRIEVAL_K = 7  # Get more context
```

### "Takes too long to summarize"

**Solution**:

- Use smaller documents
- Reduce CHUNK_SIZE
- Check system resources
- Consider using a faster model

### "Downloads not working"

**Solution**: Check browser console for CORS errors

- Enable CORS in app.py: ✅ Already configured
- Clear browser cache
- Try different browser

## 🎓 Code Quality

### Format Code

```bash
pip install black
black *.py
```

### Lint Code

```bash
pip install pylint
pylint app.py
```

### Type Checking

```bash
pip install mypy
mypy app.py --ignore-missing-imports
```

## 📖 Useful Terminal Commands

```bash
# List running processes
netstat -ano | findstr 5000

# Kill process on port 5000
taskkill /PID <PID> /F

# Check disk space
wmic logicaldisk get name,size,freespace

# Monitor Ollama models
ollama list

# Pull new model
ollama pull <model-name>

# Remove unused models
ollama rm <model-name>
```

Happy Summarizing! 🎉
