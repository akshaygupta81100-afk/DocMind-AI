
import math
import requests
import streamlit as st
import fitz

OLLAMA = "http://localhost:11434"
CHAT_MODEL = "gemma4:e4b"
EMBED_MODEL = "nomic-embed-text"

st.set_page_config(page_title="DocMind", page_icon="📚", layout="wide")
st.title("📚 DocMind")
st.caption("Ask questions about your PDFs • Local AI powered by Ollama")

def make_chunks(pdf_bytes):
    chunks = []
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")

    for page_num, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        size, overlap = 1000, 150

        for start in range(0, len(text), size - overlap):
            part = text[start:start + size].strip()
            if part:
                chunks.append({
                    "text": part,
                    "page": page_num
                })

    doc.close()
    return chunks

def get_embeddings(texts):
    response = requests.post(
        f"{OLLAMA}/api/embed",
        json={"model": EMBED_MODEL, "input": texts},
        timeout=180
    )
    response.raise_for_status()
    return response.json()["embeddings"]

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0

def answer_question(question, chunks, embeddings):
    q_embedding = get_embeddings([question])[0]

    ranked = sorted(
        range(len(chunks)),
        key=lambda i: cosine(q_embedding, embeddings[i]),
        reverse=True
    )[:4]

    context = "\n\n".join(
        f"[Page {chunks[i]['page']}]\n{chunks[i]['text']}"
        for i in ranked
    )

    prompt = f"""Answer the question using only the PDF context below.
If the answer is not present, say that you could not find it in the PDF.
Cite the relevant page numbers like [Page 2].
Do not invent facts.

PDF CONTEXT:
{context}

QUESTION:
{question}
"""

    response = requests.post(
        f"{OLLAMA}/api/chat",
        json={
            "model": CHAT_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        },
        timeout=300
    )
    response.raise_for_status()
    return response.json()["message"]["content"], ranked

try:
    requests.get(f"{OLLAMA}/api/tags", timeout=3).raise_for_status()
    st.success("Ollama is connected")
except requests.RequestException:
    st.error("Ollama is not running. Open Ollama and try again.")
    st.stop()

uploaded = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded:
    if st.button("Process PDF", type="primary"):
        with st.spinner("Reading PDF and creating embeddings..."):
            try:
                chunks = make_chunks(uploaded.getvalue())
                if not chunks:
                    st.error("No readable text found. This may be a scanned PDF.")
                    st.stop()

                embeddings = []
                batch_size = 16
                progress = st.progress(0)

                for start in range(0, len(chunks), batch_size):
                    batch = chunks[start:start + batch_size]
                    embeddings.extend(
                        get_embeddings([item["text"] for item in batch])
                    )
                    progress.progress(
                        min(1.0, (start + len(batch)) / len(chunks))
                    )

                st.session_state["chunks"] = chunks
                st.session_state["embeddings"] = embeddings
                st.session_state["pdf_name"] = uploaded.name
                st.success(f"Ready! {len(chunks)} text sections indexed.")

            except Exception as e:
                st.error(f"Processing failed: {e}")

if "chunks" in st.session_state:
    st.info(f"Current document: {st.session_state['pdf_name']}")
    question = st.text_input("Ask a question about your PDF")

    if st.button("Ask DocMind") and question.strip():
        with st.spinner("Gemma is finding your answer..."):
            try:
                answer, ranked = answer_question(
                    question,
                    st.session_state["chunks"],
                    st.session_state["embeddings"]
                )
                st.subheader("Answer")
                st.write(answer)

                st.subheader("Source pages")
                pages = sorted({
                    st.session_state["chunks"][i]["page"]
                    for i in ranked
                })
                st.write(", ".join(f"Page {p}" for p in pages))

            except Exception as e:
                st.error(f"Could not generate answer: {e}")

st.divider()
st.caption("DocMind • Local PDF question answering")
