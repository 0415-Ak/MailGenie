from langgraph.graph import StateGraph, END
from state import AgentState

from router import router_node
from tools.web_search import web_search_node
from nodes import direct_answer_node, web_answer_node
from nodes import email_node

from langgraph.checkpoint.memory import InMemorySaver




def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("router", router_node)
    graph.add_node("web_search", web_search_node)
    graph.add_node("web_answer", web_answer_node)
    graph.add_node("direct_answer", direct_answer_node)
    graph.add_node("email", email_node)


    graph.set_entry_point("router")

    graph.add_conditional_edges(
        "router",
        lambda state: state["route"],
        {
            "WEB_SEARCH": "web_search",
            "DIRECT": "direct_answer",
            "EMAIL": "email",
        },
    )


    graph.add_edge("web_search", "web_answer")
    graph.add_edge("web_answer", END)
    graph.add_edge("direct_answer", END)
    graph.add_edge("email", END)

    memory=InMemorySaver()

    return graph.compile(checkpointer=memory)
