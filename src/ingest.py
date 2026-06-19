import os

from pypdf import PdfReader
from docx import Document

import chromadb
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

from src.config import (
    GEMINI_API_KEY,
    DB_PATH,
    COLLECTION_NAME,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
    SUPPORTED_FILES
)



def extract_pdf_pages(file_path):
    pages = []

    file_name = os.path.basename(file_path)

    try:
        reader = PdfReader(file_path)

        for page_number, page in enumerate(reader.pages, start=1):

            text = page.extract_text()

            if text and text.strip():

                clean_text = " ".join(text.split())

                pages.append(
                    {
                        "text": clean_text,
                        "metadata": {
                            "source": file_name,
                            "page": page_number
                        }
                    }
                )

    except Exception as error:
        print(f"Error reading {file_name}: {error}")

    return pages


def extract_docx_pages(file_path):
    pages = []

    file_name = os.path.basename(file_path)

    try:

        document = Document(file_path)

        full_text = []

        for paragraph in document.paragraphs:

            text = paragraph.text.strip()

            if text:
                full_text.append(text)

        combined_text = "\n".join(full_text)

        pages.append(
            {
                "text": combined_text,
                "metadata": {
                    "source": file_name,
                    "page": 1
                }
            }
        )

    except Exception as error:
        print(f"Error reading {file_name}: {error}")

    return pages


def load_documents(data_folder):
    all_pages = []

    for file_name in os.listdir(data_folder):

        file_path = os.path.join(data_folder, file_name)

        extension = os.path.splitext(file_name)[1].lower()

        if extension not in SUPPORTED_FILES:
            continue

        print(f"Reading {file_name}")

        if extension == ".pdf":
            pages = extract_pdf_pages(file_path)

        elif extension == ".docx":
            pages = extract_docx_pages(file_path)

        else:
            continue

        all_pages.extend(pages)

    return all_pages


def chunk_extracted_pages(
    pages,
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP
):
    chunks = []

    for page in pages:

        text = page["text"]

        metadata = page["metadata"]

        start = 0

        text_length = len(text)

        while start < text_length:

            end = min(start + chunk_size, text_length)

            chunk_text = text[start:end]

            chunks.append(
                {
                    "text": chunk_text,
                    "metadata": {
                        "source": metadata["source"],
                        "page": metadata["page"],
                        "chunk_range": f"{start}-{end}"
                    }
                }
            )

            start += (chunk_size - chunk_overlap)

    return chunks


def save_to_vector_db(chunks):

    client = chromadb.PersistentClient(path=DB_PATH)

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    ids = []
    documents = []
    metadatas = []

    for index, chunk in enumerate(chunks):

        ids.append(f"chunk_{index}")

        documents.append(chunk["text"])

        metadatas.append(chunk["metadata"])

    print("Loading embedding model...")

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print("Generating embeddings...")

    embeddings = embedding_model.encode(
        documents,
        show_progress_bar=True
    ).tolist()

    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings
    )

    print(f"Stored {len(chunks)} chunks")

    
def run_ingestion():

    data_folder = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "data"
    )

    print("Loading documents...")

    pages = load_documents(data_folder)

    print(f"Pages loaded: {len(pages)}")

    if len(pages) == 0:
        print("No document content found.")
        return

    print("Chunking documents...")

    chunks = chunk_extracted_pages(pages)

    print(f"Chunks created: {len(chunks)}")

    print("Creating embeddings and storing...")

    save_to_vector_db(chunks)

    print("Indexing complete")


if __name__ == "__main__":
    run_ingestion()