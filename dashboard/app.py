import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath('..'))))

from dotenv import load_dotenv
load_dotenv()

from core.state import ResearchState
from core.graph import build_graph

# Page config
st.set_page_config(
    page_title="Research Agents",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Research Agents")
st.caption("Autonomous AI research powered by Claude & Tavily")

# Query input
query = st.text_input("Enter a company or topic to research:", 
                       placeholder="e.g. What is OpenAI")

if st.button("🚀 Run Research", disabled=not query):

    # Agent status panel
    st.subheader("Agent Pipeline")
    col1, col2, col3 = st.columns(3)

    with col1:
        scout_status = st.status("🔍 Scout Agent", state="running")
    with col2:
        analyst_status = st.status("🧠 Analyst Agent", state="running")
    with col3:
        synth_status = st.status("📝 Synthesizer Agent", state="running")

    # Run pipeline
    pipeline = build_graph()
    state = ResearchState(
        query=query,
        search_results=[],
        analyst_findings={},
        final_report={},
        current_agent=""
    )

    with st.spinner("Running research pipeline..."):
        result = pipeline.invoke(state)

    # Update statuses
    scout_status.update(state="complete", label="🔍 Scout Agent ✅")
    analyst_status.update(state="complete", label="🧠 Analyst Agent ✅")
    synth_status.update(state="complete", label="📝 Synthesizer Agent ✅")

    # Sources found
    st.subheader("📄 Sources Found")
    for source in result["search_results"]:
        with st.expander(f"{source['title']} — {source['confidence']} confidence"):
            st.write(source["url"])
            st.write(source["snippet"])

    # Final report
    report = result["final_report"]
    st.subheader("📋 Final Report")

    st.markdown(f"### Executive Summary")
    st.info(report["executive_summary"])

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 📌 Key Facts")
        for fact in report["key_facts"]:
            st.write(f"• {fact}")

        st.markdown("### 🚀 Opportunities")
        for opp in report["opportunities"]:
            st.write(f"• {opp}")

    with col2:
        st.markdown("### ⚠️ Risks")
        for risk in report["risks"]:
            st.write(f"• {risk}")

        st.markdown("### 🎯 Confidence")
        confidence = report["overall_confidence"].upper()
        if confidence == "HIGH":
            st.success(f"Overall Confidence: {confidence}")
        elif confidence == "MEDIUM":
            st.warning(f"Overall Confidence: {confidence}")
        else:
            st.error(f"Overall Confidence: {confidence}")

        st.metric("Sources Analyzed", report["sources_used"])