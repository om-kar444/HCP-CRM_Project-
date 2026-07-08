from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional
from sqlalchemy.orm import Session
from agent.tools import (
    log_interaction_tool,
    edit_interaction_tool,
    fetch_hcp_history_tool,
    suggest_followup_tool,
    compliance_check_tool
)
from agent.llm import classify_message_intent


class AgentState(TypedDict):
    message: str
    hcp_name: Optional[str]
    interaction_id: Optional[int]
    intent: Optional[str]
    result: Optional[dict]
    db: Session


def classify_intent(state: AgentState) -> AgentState:
    intent = classify_message_intent(state["message"])
    state["intent"] = intent
    return state


def run_log_tool(state: AgentState) -> AgentState:
    state["result"] = log_interaction_tool(state["message"], state["db"])
    return state


def run_edit_tool(state: AgentState) -> AgentState:
    state["result"] = edit_interaction_tool(
        state["message"], state["db"],
        interaction_id=state.get("interaction_id"),
        hcp_name=state.get("hcp_name")
    )
    return state


def run_history_tool(state: AgentState) -> AgentState:
    state["result"] = fetch_hcp_history_tool(state["db"], state.get("hcp_name"))
    return state


def run_followup_tool(state: AgentState) -> AgentState:
    state["result"] = suggest_followup_tool(
        state["db"],
        interaction_id=state.get("interaction_id"),
        hcp_name=state.get("hcp_name")
    )
    return state


def run_compliance_tool(state: AgentState) -> AgentState:
    state["result"] = compliance_check_tool(state["message"])
    return state


def route_after_classify(state: AgentState) -> str:
    return state["intent"]


workflow = StateGraph(AgentState)

workflow.add_node("classify", classify_intent)
workflow.add_node("log", run_log_tool)
workflow.add_node("edit", run_edit_tool)
workflow.add_node("history", run_history_tool)
workflow.add_node("followup", run_followup_tool)
workflow.add_node("compliance", run_compliance_tool)

workflow.set_entry_point("classify")
workflow.add_conditional_edges(
    "classify",
    route_after_classify,
    {
        "log": "log",
        "edit": "edit",
        "history": "history",
        "followup": "followup",
        "compliance": "compliance"
    }
)
workflow.add_edge("log", END)
workflow.add_edge("edit", END)
workflow.add_edge("history", END)
workflow.add_edge("followup", END)
workflow.add_edge("compliance", END)

agent_graph = workflow.compile()


def run_agent(message: str, db: Session, hcp_name: str = None, interaction_id: int = None) -> dict:
    initial_state = {
        "message": message,
        "hcp_name": hcp_name,
        "interaction_id": interaction_id,
        "intent": None,
        "result": None,
        "db": db
    }
    final_state = agent_graph.invoke(initial_state)
    return final_state["result"]