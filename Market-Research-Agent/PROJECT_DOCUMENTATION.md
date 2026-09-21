# Project 3 Documentation — AI Competitor Research Agent

## 1. Project Overview
I built a multi-agent competitor research system that accepts a target company and produces a structured competitive-intelligence briefing. The application uses specialized agents for competitor discovery, web research, competitive analysis, and report generation, coordinated through a LangGraph workflow and presented through Streamlit.

## 2. Problem Statement
Manual competitor research requires repeated web searches, switching between sources, organizing findings, and synthesizing them into a usable report. The agent automates this multi-step workflow while keeping a human reviewer responsible for final approval.

## 3. Architecture
Streamlit UI → LangGraph Orchestrator → Competitor Discovery Agent → Web Research Agent → Competitive Analysis Agent → Report Agent → Human Review.

## 4. Data / Search Sources
The project does not use a static training dataset. It uses fresh web-search results returned by the You.com Search API. The research agent passes retrieved evidence to the LLM and instructs it not to invent information when evidence is insufficient.

## 5. Tools and Technologies
Python, Streamlit, LangChain, LangGraph, OpenAI-compatible chat model, You.com Search API, python-dotenv, Requests, Git/GitHub.

## 6. Vibe-Coding Prompts Used
Examples of prompts used during development:
- Build a LangGraph multi-agent workflow with discovery, research, analysis, and report-generation nodes.
- Add typed shared state for company, competitors, research results, analysis, errors, and final report.
- Ground competitor research in web-search evidence and require structured JSON output.
- Add retry/error handling for search-tool failures without crashing the entire workflow.
- Add a Streamlit human-approval step before the report is accepted or downloaded.

## 7. Iterations
1. Started with a sequential multi-agent architecture.
2. Added structured state so each agent receives outputs from previous steps.
3. Added evidence-grounded research and source collection.
4. Added retry logic and per-competitor error capture.
5. Added human approval and report download in the Streamlit UI.

## 8. Human-in-the-Loop
The application generates a draft competitive briefing but does not automatically publish or send it. The user reviews the output and explicitly approves it before downloading the approved report.

## 9. Error Handling
The search tool retries transient failures. If one competitor cannot be researched, the error is recorded and shown in the UI while other available results can continue through the workflow. The system also reports missing API keys and insufficient search results.

## 10. Key Learnings / Observations
The main challenge in an agentic system is not a single prompt. The workflow must coordinate specialized responsibilities, preserve state across steps, ground model outputs in tool results, recover from failures, and define where a human should remain in control.

## 11. Sample Test
Target company: Snowflake. Expected flow: discover three competitors, gather fresh evidence for each, produce structured analyses, compile a final briefing, and request human approval.
