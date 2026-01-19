# ============================================================================
# Imports
# ============================================================================
from langchain_community.document_loaders import UnstructuredPDFLoader
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from pathlib import Path

# ============================================================================
# Configuration
# ============================================================================
DOC_PATH = "./data/intro.pdf"
MODEL = "llama3.2"
EMBEDDING_MODEL = "nomic-embed-text"
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 300
COLLECTION_NAME = "simple-rag"
RETRIEVAL_K = 5

# ============================================================================
# Step 1: Load PDF Document
# ============================================================================
def load_pdf(file_path: str):
    """Load PDF document from file path."""
    if not file_path:
        raise ValueError("PDF file path is required")
    
    loader = UnstructuredPDFLoader(file_path=file_path)
    documents = loader.load()
    print(f"✓ Loaded PDF: {file_path}")
    return documents


# ============================================================================
# Step 2: Split Documents into Chunks
# ============================================================================
def split_documents(documents):
    """Split documents into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    print(f"✓ Split into {len(chunks)} chunks")
    return chunks


# ============================================================================
# Step 3: Create Vector Database
# ============================================================================
def create_vector_db(chunks):
    """Create and store document chunks in vector database."""
    embeddings = OllamaEmbeddings(model=EMBEDDING_MODEL)
    vector_db = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
    )
    print("✓ Vector database created")
    return vector_db


# ============================================================================
# Step 4: Setup Retrieval Chain
# ============================================================================
def setup_retrieval_chain(vector_db):
    """Setup the RAG retrieval chain."""
    llm = ChatOllama(model=MODEL)
    
    # Retriever with MMR search
    retriever = vector_db.as_retriever(
        search_type="mmr",
        search_kwargs={"k": RETRIEVAL_K}
    )
    
    # RAG prompt template - Document Summarization
    rag_template = """
        You are a document summarization and study assistant.
        You must answer ONLY using the information retrieved from the document.
        Do NOT add external knowledge.
        If something is not in the document, do not invent it.

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
        (1–2 short paragraphs explaining the overall idea)

        ========================
        TASK 2: Key Topics Explained
        ========================

        Identify the main topics or sections in the document.

        For each topic, write:
        - Topic title
        - Clear explanation (4–8 lines)
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

        Create 10–15 exam-style questions that a teacher is likely to ask
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
    
    # Build the chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("✓ Retrieval chain setup complete")
    return chain


# ============================================================================
# Main Execution
# ============================================================================



if __name__ == "__main__":
    try:
        # Load PDF
        documents = load_pdf(DOC_PATH)
        
        # Split into chunks
        chunks = split_documents(documents)
        
        # Create vector database
        vector_db = create_vector_db(chunks)
        
        # Setup retrieval chain
        chain = setup_retrieval_chain(vector_db)
        
        # Query the RAG system
        print("\n" + "="*70)
        print("Running query...")
        print("="*70)
        # response = chain.invoke(input="how to report BOI?")
        response = chain.invoke(input="Summarize the document.")
        
        # Save response to file in data directory
        output_dir = Path("./data")
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / "summary.txt"
        
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(response)
        
        print(f"✓ Summary saved to {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise
