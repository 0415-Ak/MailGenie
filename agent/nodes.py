from langchain_core.messages import SystemMessage, HumanMessage
from datetime import datetime
from langchain_core.messages import SystemMessage, HumanMessage
from tools.email_sender import send_email
from HITL.email_approval import email_human_approval
from llms import executor_llm
from langchain_core.messages import SystemMessage, HumanMessage
import json
from utils.json_parser import extract_json


# DIRECT LLM ANSWER----------------------->> 

def direct_answer_node(state):
    messages = [
        SystemMessage(
    content=(
        "You are an intelligent and professional AI assistant.\n\n"
        "Understand the user's query carefully.\n"
        "Infer the depth, tone, and structure the user expects.\n\n"
        "Adapt your response style dynamically:\n"
        "- If the user asks briefly, respond concisely.\n"
        "- If the user asks for detail, provide structured explanation.\n"
        "- If comparison is implied, organize clearly.\n"
        "- If steps are required, present logically ordered steps.\n"
        "- If code is required, provide clean and correct code.\n\n"
        "Also consider relevant context from the ongoing conversation when appropriate."
        "Do not ask unnecessary clarification questions unless required.\n"
        "Be clear, structured, and precise.\n"
        "Avoid unnecessary verbosity.\n"
        "Focus on correctness and usefulness."
    )
),
        HumanMessage(content=state["user_query"]),
    ]
    # Add conversation memory
    messages.extend(state["conversation_history"])

    response = executor_llm.invoke(messages)
    return {"final_answer": response.content}



# WEB SEARCHING--------------------------------->>

def web_answer_node(state):
    today = datetime.now().strftime("%Y-%m-%d")

    messages = [
        SystemMessage(
            content=(
                f"Today is {today}.\n"
                "You must use the web search results as the PRIMARY source."
                "You may summarize, rephrase, and explain them clearly."
                "If results are weak or partial, say so and provide high-level context."
                  "Adapt your response style dynamically:\n"
                "- If the user asks briefly, respond concisely.\n"
                "- If the user asks for detail, provide structured explanation.\n"
                "- If comparison is implied, organize clearly.\n"
                "- If steps are required, present logically ordered steps.\n"
                "- If code is required, provide clean and correct code.\n\n"
                "Also consider relevant context from the ongoing conversation when appropriate."
                "Do not invent facts."
            )
        ),
    ]

     # Add conversation history
    messages.extend(state["conversation_history"])

    messages.append(
        HumanMessage(
            content=(
                f"Question:\n{state['user_query']}\n\n"
                f"Evidence:\n{state['search_results']}"
            )
        )
    )

    response = executor_llm.invoke(messages)
    return {"final_answer": response.content}


# SEND EMAIL----------------------------------------------->>

def email_node(state):

    messages = [
        SystemMessage(
            content=(
               "You are an intelligent email drafting assistant.\n\n"

        "Your task:\n"
        "1. Infer the relationship and intent from the user's request.\n"
        "   Examples:\n"
        "   - Formal: manager, HR, professor, client\n"
        "   - Semi-formal: colleague, senior, mentor\n"
        "   - Informal: friend, family, close contact\n\n"

        "2. Based on this inference, choose:\n"
        "- Appropriate tone (formal / friendly / casual)\n"
        "- Proper greeting\n"
        "- Clear paragraph structure (do NOT write in a single block)\n"
        "- Appropriate closing and sign-off\n\n"

        "Formatting rules:\n"
        "- Use short, readable paragraphs\n"
        "- Leave blank lines between paragraphs\n"
        "- Avoid generic filler phrases\n"
        "- Sound natural and human\n\n"

        "Output STRICTLY in the following JSON format:\n"
        "{\n"
        '  "subject": "Concise and context-aware subject line",\n'
        '  "body": "Properly formatted email body with line breaks"\n'
        "}\n\n"

        "Do NOT include explanations, markdown, or extra text.\n"
        "Only return valid JSON."
            )
        ),
        HumanMessage(content=state["user_query"]),
    ]

    messages.extend(state["conversation_history"])

    response = executor_llm.invoke(messages)
    draft = extract_json(response.content)

    return {
        "email_draft": draft,
        "final_answer": "Email draft generated."
    }


#      USE THIS CODE WHEN U HAVE TO RUN MAIN.PY IN TERMINAL--------------------->

# def email_node(state):
#     to_email = input("Enter recipient email: ")

#     messages = [
#         SystemMessage(
#             content=(
#                "You are an intelligent email drafting assistant.\n\n"

#         "Your task:\n"
#         "1. Infer the relationship and intent from the user's request.\n"
#         "   Examples:\n"
#         "   - Formal: manager, HR, professor, client\n"
#         "   - Semi-formal: colleague, senior, mentor\n"
#         "   - Informal: friend, family, close contact\n\n"

#         "2. Based on this inference, choose:\n"
#         "- Appropriate tone (formal / friendly / casual)\n"
#         "- Proper greeting\n"
#         "- Clear paragraph structure (do NOT write in a single block)\n"
#         "- Appropriate closing and sign-off\n\n"

#         "Formatting rules:\n"
#         "- Use short, readable paragraphs\n"
#         "- Leave blank lines between paragraphs\n"
#         "- Avoid generic filler phrases\n"
#         "- Sound natural and human\n\n"

#         "Output STRICTLY in the following JSON format:\n"
#         "{\n"
#         '  "subject": "Concise and context-aware subject line",\n'
#         '  "body": "Properly formatted email body with line breaks"\n'
#         "}\n\n"

#         "Do NOT include explanations, markdown, or extra text.\n"
#         "Only return valid JSON."
#             )
#         ),
#         HumanMessage(content=state["user_query"]),
#     ]

#     # Add conversation history
#     messages.extend(state["conversation_history"])

#     response = executor_llm.invoke(messages)

#     draft = extract_json(response.content)


#     # 2️ HITL LOOP
#     while True:

#         action, payload = email_human_approval(draft)

#         if action == "SEND":
#             send_email(to_email, draft["subject"], draft["body"])
#             return {"final_answer": "Email sent successfully."}

#         elif action == "CANCEL":
#             return {"final_answer": "Email cancelled by user."}

#         elif action == "EDIT":
#             edit_instruction = payload

#             # Append edit instruction to conversation memory
#             state["conversation_history"].append(
#                 HumanMessage(content=f"Edit this email: {edit_instruction}")
#             )

#             # Ask LLM to modify existing draft
#             edit_messages = [
#                 SystemMessage(
#                     content=(
#                         "You are an email editing assistant.\n"
#                         "Modify the existing email based on user instruction.\n"
#                         "Formatting rules:\n"
#                         "- Use short, readable paragraphs\n"
#                         "- Leave blank lines between paragraphs\n"
#                         "- Avoid generic filler phrases\n"
#                         "- Sound natural and human\n\n"
#                         "Return STRICTLY JSON with subject and body."
#                     )
#                 ),
#                 HumanMessage(
#                     content=(
#                         f"Current Email:\n"
#                         f"Subject: {draft['subject']}\n\n"
#                         f"{draft['body']}\n\n"
#                         f"User Instruction: {edit_instruction}"
#                     )
#                 ),
#             ]

#             response = executor_llm.invoke(edit_messages)
#             draft = extract_json(response.content)




