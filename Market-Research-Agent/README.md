# Week 3 Project — AI Competitor Research Agent

## Project overview
A multi-agent competitor research application built for The Gen Academy Week 3 Agentic AI Systems project. A LangGraph orchestrator coordinates specialized agents that discover three competitors, gather fresh web evidence, analyze the findings, and compile a structured competitive-intelligence briefing in Streamlit.

## One-liner
My agent helps business analysts research a company and its competitors in a Streamlit web app, replacing manual searching and tab-juggling. It autonomously discovers competitors, researches current web evidence, and produces a structured briefing using search and LLM tools, then hands the final report to a human for approval.

## Architecture
User → Streamlit → LangGraph Orchestrator → Discovery Agent → Research Agent → Analysis Agent → Report Agent → Human Approval

## Agent framework
- **Goal:** Produce a grounded competitor-analysis briefing for a target company.
- **Surface:** Streamlit web application.
- **Steps:** Discover competitors → research each competitor → analyze evidence → compile report → human review.
- **Tools/actions:** You.com web search (read), OpenAI model calls (reason/structure), report download after approval (write to user's local machine).
- **State:** Target company, competitors, research evidence, analyses, final report, errors, approval state.
- **Never do:** Invent unsupported competitor facts, expose API keys, or automatically publish/send the report.
- **Human-in-the-loop:** User approves the final report before download/acceptance.
- **Failure handling:** Search calls retry; per-competitor failures are captured so the workflow can continue; errors are displayed to the user.
- **Success measure:** Produce a usable briefing for three competitors with traceable sources and human approval.

## Setup
1. Create and activate a Python virtual environment.
2. Install dependencies: `pip install -r requirements.txt`
3. Copy `.env.example` to `.env`.
4. Add `OPENAI_API_KEY` and `YOU_API_KEY`.
5. Run: `streamlit run app.py`

## Demo suggestion
Try `Snowflake`, `Databricks`, or another company with substantial public web coverage.

## Security
`.env` is excluded by `.gitignore`. Never commit API keys.
