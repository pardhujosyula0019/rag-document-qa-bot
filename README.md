# Document Q&A Bot using Retrieval-Augmented Generation (RAG)

## Overview

This project is a Retrieval-Augmented Generation (RAG) based Document Question Answering system built using Python.

The application allows users to ask natural language questions about a collection of documents and receive accurate, context-grounded answers with source citations.

Instead of relying solely on the knowledge of a Large Language Model (LLM), the system retrieves relevant information from a custom document collection and provides answers based only on the retrieved content.

---

## Features

* Supports PDF and DOCX documents
* Extracts and processes document text
* Splits documents into overlapping chunks
* Stores embeddings in a persistent ChromaDB vector database
* Performs semantic similarity search
* Retrieves the most relevant document chunks
* Generates grounded answers using Google Gemini
* Includes source citations (filename and page number)
* Interactive command-line interface
* Persistent vector storage (documents are indexed only once)

---

## Project Architecture

```text
User Question
      │
      ▼
Query Embedding
      │
      ▼
ChromaDB Similarity Search
      │
      ▼
Top-K Relevant Chunks
      │
      ▼
Prompt Construction
      │
      ▼
Google Gemini
      │
      ▼
Grounded Answer + Citation
```

---

## Project Structure

```text
document-qa-bot/
│
├── data/
│   ├── Artificial_Intelligence.pdf
│   ├── Business_Trends.pdf
│   ├── Cyber_Security.pdf
│   ├── renewable_energy.pdf
│   └── space_exploratory.docx
│
├── db/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── ingest.py
│   ├── query.py
│   └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Technologies Used

### Programming Language

* Python 3.11+

### Document Processing

* pypdf
* python-docx

### Embeddings

* Sentence Transformers
* all-MiniLM-L6-v2

### Vector Database

* ChromaDB

### Large Language Model

* Google Gemini

### Utilities

* python-dotenv
* tqdm

---

## Chunking Strategy

The system uses a fixed-size chunking strategy.

### Configuration

* Chunk Size: 1000 characters
* Chunk Overlap: 200 characters

### Why Overlap?

Chunk overlap helps preserve context at chunk boundaries and reduces the possibility of losing important information during retrieval.

Each chunk stores metadata including:

* Source filename
* Page number
* Chunk range

---

## Retrieval Process

1. User enters a question.
2. The question is converted into an embedding using the same embedding model used during indexing.
3. ChromaDB performs similarity search.
4. Top-K relevant chunks are retrieved.
5. Retrieved chunks are used as context for Gemini.
6. Gemini generates a grounded answer with citations.

---

## Hallucination Prevention

The system uses a grounding prompt that instructs Gemini to:

* Use only the retrieved document context.
* Avoid external knowledge.
* Return a fallback response if the answer is not present in the provided documents.

Fallback Response:

```text
I am sorry, but the provided documents do not contain the answer to your question.
```

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd document-qa-bot
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

Windows:

```bash
venv\Scripts\activate
```

Linux / macOS:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Setup

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_api_key_here
```

---

## Index Documents

Run:

```bash
py -m src.ingest
```

This will:

* Read documents
* Extract text
* Create chunks
* Generate embeddings
* Store vectors in ChromaDB

---

## Run the Application

```bash
py -m src.main
```

Example:

```text
Question: What is Artificial Intelligence?

Answer:
Artificial Intelligence is a computing concept that helps machines solve problems and learn from experience.

(Source: Artificial_Intelligence.pdf, Page: 1)
```

---

## Future Improvements

* Streamlit web interface
* Support for TXT files
* Better PDF text cleaning
* Hybrid search (keyword + semantic)
* Re-ranking retrieved chunks
* Multi-document citations

---

## Author

Submitted as part of the AI Engineering Internship Assignment.

Built using Python, ChromaDB, Sentence Transformers, and Google Gemini.
