from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

# Load environment variables
load_dotenv()

# LLM 1: ROUTER / REASONER (Qwen)

router_llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0.0,          
    max_tokens=512,
)


# LLM 2: EXECUTION / RESPONSE (LLaMA)

executor_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,         
    max_tokens=1024,
)


# TEST 1: Router Model

def test_router():
    messages = [
        SystemMessage(
            content=(
                "You are a routing agent. "
                "Your job is to decide whether the user request requires:\n"
                "1. A TOOL\n"
                "2. MULTI-STEP ACTION\n"
                "3. DIRECT ANSWER\n\n"
                "Reply with only one word: TOOL / MULTI_STEP / DIRECT"
            )
        ),
        HumanMessage(content="who is the pm of india??")
    ]

    response = router_llm.invoke(messages)
    print("\n[ROUTER OUTPUT]")
    print(response.content)



# TEST 2: Executor Model

def test_executor():
    messages = [
        SystemMessage(
            content=(
                "You are an execution agent. "
                "Given a task, explain the steps clearly."
            )
        ),
        HumanMessage(content="Explain how a ride booking will be performed.")
    ]

    response = executor_llm.invoke(messages)
    print("\n[EXECUTOR OUTPUT]")
    print(response.content)


if __name__ == "__main__":
    print("Running Groq LLM tests...")
    test_router()
    test_executor()
