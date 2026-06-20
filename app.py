import streamlit as st

from src.query import query_rag

st.set_page_config(
    page_title="Document QA Bot",
    page_icon="📚"
)

st.title("📚 Document QA Bot")

question = st.text_input(
    "Ask a question from your documents"
)

if st.button("Search"):

    if question.strip():

        result = query_rag(question)

        st.subheader("Answer")

        st.write(result["answer"])