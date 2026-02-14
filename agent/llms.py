from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

router_llm = ChatGroq(
    model="qwen/qwen3-32b",
    temperature=0.0,
    max_tokens=256,
)

executor_llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0.2,
    max_tokens=512,
)
