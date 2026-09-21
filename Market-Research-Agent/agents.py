import json
import os
from typing import Dict, List, Any
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from tools import you_search, compact_search_results


def llm():
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise RuntimeError("OPENAI_API_KEY is missing. Add it to your .env file.")
    return ChatOpenAI(model=os.getenv("OPENAI_MODEL", "gpt-4.1-mini"), temperature=0.1)


def _json_call(system: str, user: str) -> Any:
    model = llm().bind(response_format={"type": "json_object"})
    msg = model.invoke([SystemMessage(content=system), HumanMessage(content=user)])
    return json.loads(msg.content)


def discover_competitors(company: str) -> List[str]:
    evidence = compact_search_results(you_search(f"{company} top competitors alternatives market", count=7))
    data = _json_call(
        "You are Competitor Discovery Agent. Use only the supplied search evidence. Return JSON with key competitors containing exactly 3 company names. Do not include the target company.",
        f"Target company: {company}\n\nSearch evidence:\n{evidence}",
    )
    competitors = [str(x).strip() for x in data.get("competitors", []) if str(x).strip()]
    if len(competitors) < 3:
        raise RuntimeError("Discovery agent did not identify three competitors.")
    return competitors[:3]


def research_competitor(target: str, competitor: str) -> Dict[str, Any]:
    queries = [
        f"{competitor} official products features pricing",
        f"{competitor} market positioning compared with {target}",
        f"{competitor} recent news announcements 2026",
    ]
    all_results = []
    for q in queries:
        all_results.extend(you_search(q, count=4))
    evidence = compact_search_results(all_results)
    data = _json_call(
        "You are a Web Research Agent. Extract facts only from supplied evidence. Return JSON keys: company, core_products_features (array), pricing (string), market_positioning (string), recent_news (array), sources (array of objects with title and url). If evidence is insufficient, say so instead of inventing facts.",
        f"Target company: {target}\nCompetitor: {competitor}\n\nEvidence:\n{evidence}",
    )
    return data


def analyze_competitor(target: str, competitor: str, research: Dict[str, Any]) -> Dict[str, Any]:
    return _json_call(
        "You are a Competitive Analysis Agent. Based only on the supplied research, return JSON keys: competitor, summary, strengths (array), potential_gaps (array), comparison_to_target (string), confidence (High/Medium/Low). Avoid unsupported claims.",
        f"Target: {target}\nCompetitor: {competitor}\nResearch:\n{json.dumps(research, indent=2)}",
    )


def compile_report(company: str, competitors: List[str], research: Dict[str, Any], analyses: Dict[str, Any]) -> str:
    prompt = f"""Create a concise professional competitor-analysis briefing in Markdown.
Target company: {company}
Competitors: {competitors}
Research: {json.dumps(research, indent=2)}
Analyses: {json.dumps(analyses, indent=2)}

Include: Executive Summary, a comparison table, a section for each competitor (products/features, pricing, positioning, recent news, strengths/gaps), Key Takeaways, and Sources. Do not add facts not present in the supplied data."""
    return llm().invoke([SystemMessage(content="You are the Orchestrator/Report Agent."), HumanMessage(content=prompt)]).content
