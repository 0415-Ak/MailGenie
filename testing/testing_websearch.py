from tavily import TavilyClient
from dotenv import load_dotenv

import os

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY not found in environment variables")

tavily_client = TavilyClient(api_key=TAVILY_API_KEY)



def web_search(query: str, max_results: int = 5):
    """
    Simple web search tool
    """
    results = tavily_client.search(
        query=query,
        max_results=max_results,
        include_answer=True,
        include_raw_content=False,
    )

    snippets = []
    for r in results.get("results", []):
        snippets.append(f"- {r.get('title')}: {r.get('content')}")

    return "\n".join(snippets)


print(web_search("what is the current indian union budget announced in india?"))

while(True):
    query=input("\n\nenter the query :")

    if query in ["exit","quit"]:
        print("exiting....")
        break
    print(web_search(query))