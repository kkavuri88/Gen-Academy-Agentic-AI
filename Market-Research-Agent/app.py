import streamlit as st
from dotenv import load_dotenv
from graph import build_graph

load_dotenv()
st.set_page_config(page_title="Market Research Agent", page_icon="🔎", layout="wide")

st.title("Competitor Research Agent")
st.caption("Multi-agent competitive intelligence with LangGraph orchestration, web-search tools, state, error handling, and human review.")

with st.sidebar:
    st.header("Agent Architecture")
    st.markdown("**1. Discovery Agent** → identifies 3 competitors\n\n**2. Research Agent** → gathers fresh web evidence\n\n**3. Analysis Agent** → compares positioning, strengths and gaps\n\n**4. Orchestrator** → compiles the final briefing")
    st.info("Human-in-the-loop: the report is not accepted until you explicitly approve it.")

company = st.text_input("Company to research", placeholder="e.g., Snowflake")
run = st.button("Run Competitor Analysis", type="primary", disabled=not company.strip())

if run:
    st.session_state.approved = False
    st.session_state.company = company.strip()
    with st.status("Running multi-agent workflow...", expanded=True) as status:
        st.write("Discovering competitors...")
        graph = build_graph()
        result = graph.invoke({"company": company.strip(), "errors": [], "approved": False})
        st.session_state.result = result
        status.update(label="Agent workflow complete", state="complete")

result = st.session_state.get("result")
if result:
    st.subheader("Discovered Competitors")
    cols = st.columns(max(1, len(result.get("competitors", []))))
    for i, c in enumerate(result.get("competitors", [])):
        cols[i].metric(f"Competitor {i+1}", c)

    if result.get("errors"):
        with st.expander("Errors / recovery notes"):
            for e in result["errors"]:
                st.warning(e)

    st.subheader("Competitive Intelligence Briefing")
    st.markdown(result.get("final_report", "No report generated."))

    st.divider()
    st.subheader("Human Review")
    c1, c2 = st.columns(2)
    if c1.button("Approve Report", type="primary"):
        st.session_state.approved = True
    if c2.button("Regenerate Analysis"):
        st.session_state.pop("result", None)
        st.session_state.approved = False
        st.rerun()

    if st.session_state.get("approved"):
        st.success("Report approved by human reviewer.")
        st.download_button("Download Approved Report", result.get("final_report", ""), file_name=f"{st.session_state.get('company','company')}_competitor_report.md", mime="text/markdown")
