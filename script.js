// ============================================================================
// DOM Elements
// ============================================================================
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const dropZone = document.getElementById('dropZone');
const fileInfo = document.getElementById('fileInfo');

const uploadSection = document.getElementById('uploadSection');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const errorSection = document.getElementById('errorSection');

const summaryContent = document.getElementById('summaryContent');
const progressFill = document.getElementById('progressFill');

const closeBtn = document.getElementById('closeBtn');
const newSummaryBtn = document.getElementById('newSummaryBtn');
const retryBtn = document.getElementById('retryBtn');

const downloadTxt = document.getElementById('downloadTxt');
const downloadDoc = document.getElementById('downloadDoc');

let currentSummary = null;
let currentFileName = '';

// ============================================================================
// Event Listeners
// ============================================================================
browseBtn.addEventListener('click', () => fileInput.click());

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFileSelect(e.target.files[0]);
    }
});

dropZone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropZone.classList.add('drag-over');
});

dropZone.addEventListener('dragleave', () => {
    dropZone.classList.remove('drag-over');
});

dropZone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropZone.classList.remove('drag-over');
    if (e.dataTransfer.files.length > 0) {
        handleFileSelect(e.dataTransfer.files[0]);
    }
});

closeBtn.addEventListener('click', resetUI);
newSummaryBtn.addEventListener('click', resetUI);
retryBtn.addEventListener('click', resetUI);

downloadTxt.addEventListener('click', downloadAsTxt);
downloadDoc.addEventListener('click', downloadAsDoc);

// ============================================================================
// File Handling
// ============================================================================
function handleFileSelect(file) {
    // Validate file type
    const validTypes = ['application/pdf', 'text/plain', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    
    if (!validTypes.includes(file.type)) {
        showError('Invalid File Type', 'Please upload a PDF, TXT, or DOCX file.');
        return;
    }

    // Validate file size (max 10MB)
    if (file.size > 10 * 1024 * 1024) {
        showError('File Too Large', 'Maximum file size is 10MB.');
        return;
    }

    currentFileName = file.name.split('.')[0];
    fileInfo.textContent = `✓ Selected: ${file.name} (${formatFileSize(file.size)})`;
    
    // Start summarization after a brief delay for visual feedback
    setTimeout(() => summarizeDocument(file), 500);
}

function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return Math.round((bytes / Math.pow(k, i)) * 100) / 100 + ' ' + sizes[i];
}

// ============================================================================
// Summarization
// ============================================================================
async function summarizeDocument(file) {
    uploadSection.style.display = 'none';
    loadingSection.style.display = 'block';
    errorSection.style.display = 'none';
    resultsSection.style.display = 'none';

    // Simulate progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress > 90) progress = 90;
        progressFill.style.width = progress + '%';
    }, 300);

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/summarize', {
            method: 'POST',
            body: formData
        });

        clearInterval(progressInterval);
        progressFill.style.width = '100%';

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to summarize document');
        }

        const data = await response.json();
        currentSummary = data.summary;

        // Brief delay before showing results
        setTimeout(() => {
            displayResults(data.summary);
        }, 500);

    } catch (error) {
        clearInterval(progressInterval);
        console.error('Error:', error);
        showError('Summarization Failed', error.message || 'Please try again.');
    }
}

// ============================================================================
// Display Results
// ============================================================================
function displayResults(summary) {
    // Parse summary structure (Title, Summary bullets, Key takeaway)
    const summaryHTML = formatSummaryHTML(summary);
    summaryContent.innerHTML = summaryHTML;

    loadingSection.style.display = 'none';
    resultsSection.style.display = 'block';
    errorSection.style.display = 'none';

    // Scroll to results
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

function formatSummaryHTML(summary) {
    // Try to parse structured format
    let html = '<div class="summary-content-inner">';

    // Extract Title
    const titleMatch = summary.match(/Title:\s*(.+?)(?:\n|Summary:)/i);
    if (titleMatch) {
        html += `<div class="summary-title">${escapeHtml(titleMatch[1].trim())}</div>`;
    }

    // Extract Summary bullets
    const summaryMatch = summary.match(/Summary:(.*?)(?:Key takeaway:|$)/is);
    if (summaryMatch) {
        html += '<div class="summary-summary"><h3>Summary</h3>';
        const bullets = summaryMatch[1]
            .split('\n')
            .filter(line => line.trim())
            .map(line => line.replace(/^[-•*]\s*/, '').trim())
            .filter(line => line.length > 0);
        
        bullets.forEach(bullet => {
            if (bullet.length > 0) {
                html += `<div class="summary-bullet">• ${escapeHtml(bullet)}</div>`;
            }
        });
        html += '</div>';
    }

    // Extract Key takeaway
    const takeawayMatch = summary.match(/Key takeaway:\s*(.+?)(?:\n|$)/i);
    if (takeawayMatch) {
        html += `<div class="summary-takeaway">
            <h3>Key Takeaway</h3>
            <p>${escapeHtml(takeawayMatch[1].trim())}</p>
        </div>`;
    }

    // If no structured format found, just display as is
    if (!titleMatch && !summaryMatch && !takeawayMatch) {
        html += `<div style="color: var(--text-secondary); line-height: 1.8;">
            ${summary.split('\n').map(line => escapeHtml(line)).join('<br>')}
        </div>`;
    }

    html += '</div>';
    return html;
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// ============================================================================
// Error Handling
// ============================================================================
function showError(title, message) {
    document.getElementById('errorTitle').textContent = title;
    document.getElementById('errorMessage').textContent = message;

    uploadSection.style.display = 'none';
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'block';

    setTimeout(() => {
        errorSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// ============================================================================
// Download Functionality
// ============================================================================
async function downloadAsTxt() {
    if (!currentSummary) return;

    const element = document.createElement('a');
    const file = new Blob([currentSummary], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = `${currentFileName}_summary.txt`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

async function downloadAsDoc() {
    if (!currentSummary) return;

    try {
        // Using the docx library
        const { Document, Packer, Paragraph, TextRun, HeadingLevel } = window.docx;

        // Parse the summary into structured paragraphs
        const paragraphs = [];
        const lines = currentSummary.split('\n');

        lines.forEach((line, index) => {
            if (line.trim()) {
                const isBold = line.includes('Title:') || line.includes('Summary:') || line.includes('Key takeaway:');
                paragraphs.push(
                    new Paragraph({
                        text: line.replace(/^(Title:|Summary:|Key takeaway:)\s*/, '').trim(),
                        bold: isBold,
                        spacing: { after: isBold ? 200 : 100 }
                    })
                );
            }
        });

        const doc = new Document({
            sections: [{
                properties: {},
                children: paragraphs
            }]
        });

        Packer.toBlob(doc).then(blob => {
            const element = document.createElement('a');
            element.href = URL.createObjectURL(blob);
            element.download = `${currentFileName}_summary.docx`;
            document.body.appendChild(element);
            element.click();
            document.body.removeChild(element);
        });

    } catch (error) {
        console.error('Error generating DOCX:', error);
        alert('Error generating Word document. Downloading as TXT instead.');
        downloadAsTxt();
    }
}

// ============================================================================
// UI Reset
// ============================================================================
function resetUI() {
    uploadSection.style.display = 'block';
    loadingSection.style.display = 'none';
    resultsSection.style.display = 'none';
    errorSection.style.display = 'none';

    fileInput.value = '';
    fileInfo.textContent = '';
    progressFill.style.width = '0%';

    setTimeout(() => {
        uploadSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 100);
}

// ============================================================================
// Check if backend is available
// ============================================================================
window.addEventListener('load', async () => {
    try {
        const response = await fetch('/api/health');
        if (!response.ok) {
            console.warn('Backend health check failed');
        }
    } catch (error) {
        console.warn('Backend not available. Make sure the server is running on http://localhost:5000');
    }
});
