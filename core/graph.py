from langgraph.graph import StateGraph, END
from core.state import ResearchState
from agents.scout import scout_agent
from agents.analyst import analyst_agent
from agents.synthesizer import synthesizer_agent

def build_graph():
    graph = StateGraph(ResearchState)

    # Add each agent as a node
    graph.add_node("scout", scout_agent)
    graph.add_node("analyst", analyst_agent)
    graph.add_node("synthesizer", synthesizer_agent)

    # Define the flow
    graph.set_entry_point("scout")
    graph.add_edge("scout", "analyst")
    graph.add_edge("analyst", "synthesizer")
    graph.add_edge("synthesizer", END)

    return graph.compile()