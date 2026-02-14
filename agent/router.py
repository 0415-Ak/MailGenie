from langchain_core.messages import SystemMessage, HumanMessage
from llms import router_llm

import json
from pydantic import BaseModel
from typing import Literal

def router_node(state):
    
    messages = [
    SystemMessage(
        content=(
            "You are a query classifier. Your ONLY job is to return one word.\n\n"
            "Read the user query and respond with EXACTLY one word based on these rules:\n\n"

            "Return 'WEB_SEARCH' if:\n"
            "- Query needs current or real-time information (weather, news, stock prices)\n"
            "- Query asks about recent events or latest updates\n"
            "- Query contains words like: today, now, current, latest, recent\n\n"

            "Return 'EMAIL' if:\n"
            "- Query is about composing, sending, writing, or drafting an email\n"
            "- Query mentions email explicitly\n\n"

            "Return 'DIRECT' for:\n"
            "- Everything else (explanations, coding help, general knowledge, historical info)\n\n"

            "EXAMPLES (learn the pattern):\n"
            "Query: 'Send an email to my manager' → EMAIL\n"
            "Query: 'What is the weather right now?' → WEB_SEARCH\n"
            "Query: 'Latest news on AI' → WEB_SEARCH\n"
            "Query: 'Explain Python decorators' → DIRECT\n"
            "Query: 'Tell me about Article 370' → DIRECT\n\n"

            "CRITICAL RULES:\n"
            "- Return ONLY ONE WORD\n"
            "- Allowed outputs: WEB_SEARCH, EMAIL, DIRECT\n"
            "- NO explanations\n"
            "- NO punctuation\n"
            "- NO extra text\n\n"

            "Now classify this query:"
        )
    ),
    HumanMessage(content=state['user_query']),
]


    response = router_llm.invoke(messages)
    route = response.content.strip().upper()
    # print(route)
    
    route = route.splitlines()[-1].strip()

    if route not in {"EMAIL", "WEB_SEARCH", "DIRECT"}:
        # print(route)
        return {"route": "DIRECT"}
    

    return {"route": route}


# while(True):
#     query=input("\nenter your query : ")
#     if query in ["exit","quit"]:
#         break
#     test_state = {
#         "user_query": query
#     }

#     output = router_node(test_state)
#     print(output)
