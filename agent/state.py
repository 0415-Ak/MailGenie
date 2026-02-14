from typing import TypedDict, Optional, List
from langchain_core.messages import BaseMessage


class AgentState(TypedDict):
    user_query: str
    route: Optional[str]

    search_results: Optional[str]

    # Email Sending
    email_to: Optional[str]
    email_draft: Optional[dict]
    email_edit_instruction: Optional[str]
    email_status: Optional[str]

    conversation_history: List[BaseMessage]


    final_answer: Optional[str]

