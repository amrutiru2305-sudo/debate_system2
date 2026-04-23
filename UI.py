import sys
import os

# Fix module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st

from agents.proponent import proponent_agent
from agents.skeptic import skeptic_agent
from agents.decomposer import decompose_claims
from agents.moderator import moderator_agent
from agents.baseline import baseline_agent

from memory.cache import search_cache, add_to_cache
from evaluation.metrics import evaluate_claims

st.set_page_config(page_title="Debate AI System", layout="wide")

st.title("🧠 Hybrid Multi-Agent Debate System")
st.write("Fact-checking using Debate + RAG + Atomic Claims + Metrics")

# Input
query = st.text_input("Enter your question:")

if st.button("Run") and query:

    # 🔥 1. Cache Check
    cached = search_cache(query)
    if cached:
        st.success("⚡ Cache Hit (Fast Response)")
        st.write(cached)
        st.stop()

    # 🔥 2. Baseline (Normal LLM)
    with st.spinner("Running baseline..."):
        baseline = baseline_agent(query)

    st.subheader("⚪ Baseline (Normal LLM)")
    st.write(baseline)

    # 🔥 3. Proponent
    with st.spinner("Proponent thinking..."):
        proponent = proponent_agent(query)

    st.subheader("🟢 Proponent")
    st.write(proponent)

    # 🔥 4. Early Termination (Simple heuristic)
    if "well-known" in proponent.lower() or "clearly" in proponent.lower():
        st.warning("⚡ Early Termination Triggered (High Confidence)")
        st.write(proponent)

        add_to_cache(query, proponent)
        st.stop()

    # 🔥 5. Decompose into claims
    with st.spinner("Breaking into claims..."):
        claims = decompose_claims(proponent)

    st.subheader("🔍 Atomic Claims")
    st.write(claims)

    # 🔥 6. Skeptic
    with st.spinner("Skeptic analyzing..."):
        skeptic = skeptic_agent(query, proponent)

    st.subheader("🔴 Skeptic")
    st.write(skeptic)

    # 🔥 7. Moderator (Final Decision + Evidence)
    with st.spinner("Final evaluation..."):
        final = moderator_agent(query, proponent, skeptic, claims)

    st.subheader("🧑‍⚖️ Final Verdict")
    st.write(final)

    # 🔥 8. Metrics
    metrics = evaluate_claims(final)
    st.subheader("📊 Metrics")

    st.write(f"Accuracy: {metrics.get('accuracy', 0)}")
    st.write(f"Hallucination Rate: {metrics.get('hallucination_rate', 0)}")
    st.write(f"Risk Level: {metrics.get('risk', 'Safe')}")

    # 🔥 9. Save to Cache
    add_to_cache(query, final)