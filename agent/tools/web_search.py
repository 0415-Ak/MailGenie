from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def web_search_node(state):
    query = state["user_query"]

    results = tavily.search(
        query=query,
        max_results=5,
        include_answer=False,
    )

    evidence = []
    for r in results.get("results", []):
        evidence.append(
            f"Title: {r.get('title')}\n"
            f"Content: {r.get('content')}"
        )

    return {"search_results": "\n---\n".join(evidence)}
