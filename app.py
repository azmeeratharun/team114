import streamlit as st
from pdf_processor import extract_and_chunk
from semantic_search import build_faiss_index, retrieve_chunks
from answer_generator import generate_answer
from pathlib import Path

st.set_page_config(page_title="StudyMate", page_icon="📚", layout="wide")
st.title("📚 StudyMate – Conversational Q&A from PDFs")

# ---- File Upload ----
uploaded_files = st.file_uploader(
    "Upload one or more PDF study materials", type="pdf", accept_multiple_files=True
)

# ---- Question Input ----
question = st.text_input("Ask a question based on the uploaded PDFs:")

# ---- Action Button ----
if st.button("Get Answer"):
    if not uploaded_files:
        st.error("Please upload at least one PDF.")
    elif not question.strip():
        st.error("Please enter a question.")
    else:
        with st.spinner("Processing PDFs…"):
            # Extract and chunk all uploaded PDFs
            docs_chunks = [extract_and_chunk(f) for f in uploaded_files]
            all_chunks = [chunk for doc in docs_chunks for chunk in doc]

            # Build FAISS index & retrieve relevant chunks
            index, embeddings, text_chunks = build_faiss_index(all_chunks)
            relevant_chunks = retrieve_chunks(
                query=question,
                index=index,
                embeddings=embeddings,
                chunks=text_chunks,
                top_k=5
            )

        with st.spinner("Generating answer with IBM Granite…"):
            answer = generate_answer(relevant_chunks, question)

        st.subheader("Answer")
        st.write(answer)

# ---- Optional local PDF processing ----
if __name__ == "__main__":
    pdf_files = ["sample1.pdf", "sample2.pdf"]
    pdf_paths = [Path(f) for f in pdf_files if Path(f).exists()]

    if pdf_paths:
        docs_chunks = [extract_and_chunk(f) for f in pdf_paths]
        all_chunks = [chunk for doc in docs_chunks for chunk in doc]

        print("\n--- Extracted Chunks from Local PDFs ---")
        for i, chunk in enumerate(all_chunks, 1):
            print(f"\n--- Chunk {i} ---\n{chunk}")
    else:
        print("No local PDF files found. Upload PDFs via Streamlit UI.")