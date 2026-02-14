import json
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_groq import ChatGroq

executor_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    max_tokens=512,
)

import json
from langchain_core.messages import SystemMessage, HumanMessage

def ride_extraction_node(state):
    """
    Extract pickup, destination, and ride_type from user query.
    Returns ONLY structured ride_details.
    """

    old = state.get("ride_details") or {
        "pickup": None,
        "destination": None,
        "ride_type": None,
    }

    system_prompt = (
        "You are an information extraction assistant.\n\n"
        "Extract ride booking details from the user query.\n\n"
        "Return ONLY valid JSON with EXACTLY these keys:\n"
        "- pickup (string or null)\n"
        "- destination (string or null)\n"
        "- ride_type (string or null)\n\n"
        "Rules:\n"
        "- Do NOT explain anything\n"
        "- Do NOT add extra keys\n"
        "- Do NOT assume missing information\n"
        "- Use null if a value is not mentioned\n"
        "- Output must be valid JSON only\n\n"
        "Examples:\n"
        "Query: 'book a bike to airport'\n"
        "Output: {\"pickup\": null, \"destination\": \"airport\", \"ride_type\": \"bike\"}\n\n"
        "Query: 'go from hostel to office by cab'\n"
        "Output: {\"pickup\": \"hostel\", \"destination\": \"office\", \"ride_type\": \"cab\"}"
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=state["user_query"]),
    ]

    response = executor_llm.invoke(messages)
    raw_output = response.content.strip()

   
    try:
        extracted = json.loads(raw_output)
    except Exception:
        
        extracted = {
            "pickup": None,
            "destination": None,
            "ride_type": None
        }


     # MERGE instead of overwrite
    merged = {
        "pickup": extracted.get("pickup") or old.get("pickup"),
        "destination": extracted.get("destination") or old.get("destination"),
        "ride_type": extracted.get("ride_type") or old.get("ride_type"),
    }

    return {"ride_details": merged}


while(True):
    query=input("\nenter your query: ")
    if query in ['exit','quit']:
        print("exiting.....")
        break
    test_state = {
        "user_query": query
    }

    output =ride_extraction_node(test_state)
    print(output)