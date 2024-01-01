import os
import requests
import streamlit as st

API_BASE = os.getenv("API_BASE", "http://localhost:8000")

st.set_page_config(page_title="RAG Q&A", layout="wide")
st.title("RAG Q&A (Eval-Driven)")

with st.sidebar:
    st.header("Actions")
    if st.button("Ingest data/raw/*"):
        r = requests.post(f"{API_BASE}/ingest", json={})
        st.toast(r.json())
    if st.button("Build index"):
        r = requests.post(f"{API_BASE}/index")
        st.toast(r.json())

query = st.text_input("Ask a question", value="What is in these documents?")
top_k = st.slider("Top K", 1, 10, 5)

if st.button("Search"):
    r = requests.post(f"{API_BASE}/search", json={"query": query, "top_k": top_k})
    st.json(r.json())

if st.button("Answer"):
    r = requests.post(f"{API_BASE}/qa", json={"query": query, "top_k": top_k})
    res = r.json()
    st.subheader("Answer")
    st.write(res.get("answer", ""))
    st.subheader("Contexts")
    st.json(res.get("contexts", []))
    helpful = st.checkbox("Helpful")
    comment = st.text_input("Feedback comment", "")
    if st.button("Submit Feedback"):
        fr = {
            "query": query,
            "answer": res.get("answer", ""),
            "helpful": helpful,
            "comment": comment,
        }
        rr = requests.post(f"{API_BASE}/feedback", json=fr)
        st.toast(rr.json())

