# Quick Start Guide

## Step 1: Install Dependencies

Open PowerShell in the `llm` directory and run:

```powershell
pip install -r requirements.txt
```

Wait for all packages to install. This may take 5-10 minutes.

## Step 2: Start Ollama

Open a new PowerShell window and run:

```powershell
ollama serve
```

This starts the Ollama server. You should see output like:

```
[GIN] 2026/01/20 14:30:45 Listening and serving HTTP on 127.0.0.1:11434
```

Leave this window open.

## Step 3: Pull Required Models (First Time Only)

Open another PowerShell window and run:

```powershell
ollama pull llama3.2
ollama pull nomic-embed-text
```

Wait for both models to download. The total size is ~6GB.

## Step 4: Run the Backend Server

In the original PowerShell window (from Step 1), run:

```powershell
python app.py
```

You should see output like:

```
Starting Document Summarizer Backend...
Server running on http://localhost:5000
```

## Step 5: Open in Browser

Open your web browser and go to:

```
http://localhost:5000
```

You should see the beautiful Document Summarizer interface!

## Step 6: Upload and Summarize

1. **Click "Choose File"** or **drag and drop** a PDF, TXT, or DOCX file
2. **Wait for processing** - The progress bar shows real-time progress
3. **View results** - The summary appears with Title, Bullet Points, and Key Takeaway
4. **Download** - Click "Download .TXT" or "Download .DOCX"

## Troubleshooting

### Server won't start

- Make sure Ollama is running (Step 2)
- Check that no other application is using port 5000
- Run: `netstat -ano | findstr 5000` to check

### Models not found

- Verify they downloaded completely (Step 3)
- Run `ollama list` to see installed models
- Re-download if needed: `ollama pull llama3.2`

### File upload fails

- Check file size (max 10MB)
- Allowed formats: PDF, TXT, DOCX
- Check browser console (F12) for error messages

### Summarization is slow

- First run is slower (model loading)
- Large documents take longer
- Check console output for progress

## File Locations

- **Main interface**: `http://localhost:5000/index.html`
- **Static files**: `index.html`, `styles.css`, `script.js`
- **Backend code**: `app.py`
- **Dependencies**: `requirements.txt`
- **Data**: `./data/` directory

## Keep Running

To use the application, you must keep these two windows open:

1. **Ollama server** (from Step 2)
2. **Flask backend** (from Step 4)

To stop: Press `Ctrl+C` in either window

## Next Steps

- Try summarizing different types of documents
- Download results in different formats
- Customize the prompt in `app.py` (lines 95-110)
- Adjust settings in `app.py` configuration section (lines 16-21)

## Need Help?

Check the console output in the Flask window (Step 4) for error messages. They will help diagnose issues.

Good luck! 🚀
