from graph import build_graph
from langchain_core.messages import HumanMessage, AIMessage

app = build_graph()

if __name__ == "__main__":
    state={
        "conversation_history":[]
    }
    while True:
        query = input("\nEnter your query: ")
        if query in ["exit", "quit"]:
            break
        state["user_query"] = query

        #  add human message to history

        state["conversation_history"].append(
            HumanMessage(content=query)
        )
        result = app.invoke(state)

        if result.get("final_answer"):
            print("\n[FINAL ANSWER]")
            print(result["final_answer"])

            # Append assistant response to memory

            state["conversation_history"].append(
                AIMessage(content=result["final_answer"])
            )

        MAX_MEMORY = 10

        if len(state["conversation_history"]) > MAX_MEMORY:
            state["conversation_history"] = state["conversation_history"][-MAX_MEMORY:]
