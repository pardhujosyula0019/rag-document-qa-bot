import chromadb
import google.generativeai as genai

from sentence_transformers import SentenceTransformer

from src.config import (
    GEMINI_API_KEY,
    DB_PATH,
    COLLECTION_NAME,
    TOP_K,
    GEMINI_MODEL
)


genai.configure(api_key=GEMINI_API_KEY)


def retrieve_chunks(user_question):
    """
    Convert user question into embedding
    and retrieve most relevant chunks.
    """

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    query_embedding = embedding_model.encode(
        user_question
    ).tolist()

    client = chromadb.PersistentClient(
        path=DB_PATH
    )

    collection = client.get_collection(
        name=COLLECTION_NAME
    )

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )

    return results


def build_context(results):
    """
    Build context string
    using retrieved chunks.
    """

    context_parts = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    for document, metadata in zip(
        documents,
        metadatas
    ):

        source = metadata["source"]
        page = metadata["page"]

        context_parts.append(
            f"[Source: {source}, Page: {page}]\n"
            f"{document}"
        )

    context = "\n\n---\n\n".join(
        context_parts
    )

    return context


def generate_answer(
    user_question,
    context
):
    """
    Generate grounded answer
    using Gemini.
    """

    prompt = f"""
You are a professional document question-answering assistant.

Use ONLY the context provided below.

If the answer is not present in the context,
reply exactly:

I am sorry, but the provided documents do not contain the answer to your question.

Always mention source citations.

CONTEXT:

{context}

QUESTION:

{user_question}

ANSWER:
"""

    model = genai.GenerativeModel(
        GEMINI_MODEL
    )

    response = model.generate_content(
        prompt
    )

    return response.text


def query_rag(user_question):
    """
    Complete RAG pipeline.
    """

    results = retrieve_chunks(
        user_question
    )

    context = build_context(
        results
    )

    answer = generate_answer(
        user_question,
        context
    )

    return {
        "answer": answer,
        "context": context
    }