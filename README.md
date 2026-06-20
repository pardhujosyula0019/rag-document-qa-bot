# Document Q&A Bot using Retrieval-Augmented Generation (RAG)

## Project Overview

Document Q&A Bot is an AI-powered question-answering system that allows users to ask questions about a collection of PDF and DOCX documents. The system uses Retrieval-Augmented Generation (RAG) to retrieve relevant document content from a vector database and generate grounded answers using Google's Gemini API.

Instead of relying only on the language model's knowledge, the bot first searches the uploaded documents, retrieves the most relevant information, and then generates answers based on the retrieved content. This improves answer accuracy and provides source citations.

---

## Tech Stack

### Programming Language

* Python 3.13

### Frontend

* Streamlit

### Vector Database

* ChromaDB 1.5.9

### Embedding Model

* Sentence Transformers
* all-MiniLM-L6-v2

### Large Language Model

* Google gemini-2.5-flash

### Document Processing

* PyPDF
* python-docx

### Environment Management

* python-dotenv

### Additional Libraries

* tqdm

---

## Architecture Overview

The application follows a Retrieval-Augmented Generation (RAG) architecture.

User Question
↓
SentenceTransformer Embedding
↓
ChromaDB Similarity Search
↓
Top-K Relevant Chunks Retrieved
↓
Context Construction
↓
Gemini Prompt Generation
↓
Answer Generation
↓
Source-Cited Response

## Project Structure

```text
rag-document-qa-bot/
│
├── data/
│   ├── Artificial_Intelligence.pdf
│   ├── Business_Trends.pdf
│   ├── Cyber_Security.pdf
│   ├── renewable_energy.pdf
│   └── space_exploratory.docx
│
├── db/
│   └── ChromaDB vector database
│
├── src/
│   ├── config.py
│   ├── ingest.py
│   ├── query.py
│   └── main.py
│
├── app.py
├── requirements.txt
├── README.md
└── .env

### Ingestion Pipeline

Documents
↓
Text Extraction
↓
Chunking
↓
Embedding Generation
↓
Store in ChromaDB

---

## Chunking Strategy

The project uses fixed-size overlapping chunking.

Configuration:

* Chunk Size: 1000 characters
* Chunk Overlap: 200 characters

Reason:

Large documents cannot be embedded as a single vector. Splitting documents into overlapping chunks preserves context across chunk boundaries and improves retrieval quality.

---

## Embedding Model and Vector Database

### Embedding Model

Model:
all-MiniLM-L6-v2

Reason:

* Lightweight
* Fast inference
* Strong semantic similarity performance
* Suitable for small-to-medium RAG applications

### Vector Database

Database:
ChromaDB

Reason:

* Easy local deployment
* Persistent storage
* Fast similarity search
* Open-source and beginner-friendly

---

## Setup Instructions

### 1. Clone Repository

git clone https://github.com/pardhujosyula0019/rag-document-qa-bot.git

cd rag-document-qa-bot

### 2. Create Virtual Environment

python -m venv venv

### 3. Activate Virtual Environment

Windows:

venv\Scripts\activate

### 4. Install Dependencies

pip install -r requirements.txt

### 5. Configure Environment Variables

Create a .env file:

GEMINI_API_KEY=YOUR_API_KEY

### 6. Run Ingestion

python -m src.ingest

### 7. Launch Application

streamlit run app.py

---

## Environment Variables

Required:

GEMINI_API_KEY

How to obtain:

1. Visit Google AI Studio.
2. Generate an API key.
3. Store it in the .env file.

Never commit API keys to GitHub.

---

## Example Queries

### Question 1

What is Artificial Intelligence?

Expected Theme:

Definition and characteristics of AI.

### Question 2

What are renewable energy sources?

Expected Theme:

Solar, wind, hydroelectric and sustainable energy.

### Question 3

What is cybersecurity?

Expected Theme:

Protection of systems, networks and digital information.

### Question 4

What is space law?

Expected Theme:

Legal framework governing activities in outer space.

### Question 5

How is AI expected to impact future industries?

Expected Theme:

Automation, productivity and technological advancement.

---

## Known Limitations

1. Retrieval quality depends on chunk size configuration.

2. The system only searches indexed documents.

3. Answers may be incomplete if relevant information is split across multiple chunks.

4. Small embedding models may miss subtle semantic relationships.

5. The application currently supports only PDF and DOCX files.

6. Documents must be re-indexed after adding new files.

---

## Future Improvements

* Dynamic document upload
* Conversational memory
* Hybrid search
* Metadata filtering
* Larger embedding models
* Multi-user support

---

## Deployment

Frontend: Streamlit Cloud

Repository:
https://github.com/pardhujosyula0019/rag-document-qa-bot

Deployment:
https://rag-document-app-bot-guxcx5rguiut4hbsyes34b.streamlit.app