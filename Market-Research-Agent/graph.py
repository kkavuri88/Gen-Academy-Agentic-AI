from langgraph.graph import StateGraph, START, END
from models import AgentState
from agents import discover_competitors, research_competitor, analyze_competitor, compile_report


def discovery_node(state: AgentState):
    try:
        return {"competitors": discover_competitors(state["company"]), "errors": state.get("errors", [])}
    except Exception as exc:
        return {"competitors": [], "errors": state.get("errors", []) + [f"Discovery failed: {exc}"]}


def research_node(state: AgentState):
    research = {}
    errors = list(state.get("errors", []))
    for competitor in state.get("competitors", []):
        try:
            research[competitor] = research_competitor(state["company"], competitor)
        except Exception as exc:
            errors.append(f"Research failed for {competitor}: {exc}")
    return {"research": research, "errors": errors}


def analysis_node(state: AgentState):
    analyses = {}
    errors = list(state.get("errors", []))
    for competitor, data in state.get("research", {}).items():
        try:
            analyses[competitor] = analyze_competitor(state["company"], competitor, data)
        except Exception as exc:
            errors.append(f"Analysis failed for {competitor}: {exc}")
    return {"analyses": analyses, "errors": errors}


def report_node(state: AgentState):
    if not state.get("analyses"):
        return {"final_report": "No report could be generated. Review the errors and retry."}
    try:
        report = compile_report(state["company"], state.get("competitors", []), state.get("research", {}), state.get("analyses", {}))
        return {"final_report": report}
    except Exception as exc:
        return {"final_report": "Report generation failed.", "errors": state.get("errors", []) + [str(exc)]}


def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("discover_competitors", discovery_node)
    graph.add_node("research_competitors", research_node)
    graph.add_node("analyze_competitors", analysis_node)
    graph.add_node("compile_report", report_node)
    graph.add_edge(START, "discover_competitors")
    graph.add_edge("discover_competitors", "research_competitors")
    graph.add_edge("research_competitors", "analyze_competitors")
    graph.add_edge("analyze_competitors", "compile_report")
    graph.add_edge("compile_report", END)
    return graph.compile()
