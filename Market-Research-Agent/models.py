from typing import TypedDict, List, Dict, Any

class AgentState(TypedDict, total=False):
    company: str
    competitors: List[str]
    research: Dict[str, Any]
    analyses: Dict[str, Any]
    final_report: str
    errors: List[str]
    approved: bool
