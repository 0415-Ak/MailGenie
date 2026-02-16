import streamlit as st
import uuid
from graph import build_graph
from langchain_core.messages import HumanMessage, AIMessage
from tools.email_sender import send_email
from llms import executor_llm
from utils.json_parser import extract_json
from langchain_core.messages import SystemMessage
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(BASE_DIR, "logo.png")

st.set_page_config(
    page_title="MailGenie AI",
    layout="wide"
)

col1, col2 = st.columns([1, 6])

with col1:
    st.image(logo_path, width=120)

with col2:
    st.title("MailGenie AI")
    st.caption("Intelligent Email & Multi-Tool AI Assistant")



app = build_graph()

# MultiSession setup

if "sessions" not in st.session_state:
    st.session_state.sessions = {}

if "chat_counter" not in st.session_state:
    st.session_state.chat_counter = 0

if "current_session" not in st.session_state:
    session_id = str(uuid.uuid4())
    st.session_state.chat_counter += 1
    chat_name = f"Chat {st.session_state.chat_counter}"

    st.session_state.sessions[session_id] = {
        "chat_name": chat_name,   
        "chat_messages": [],
        "agent_state": {"conversation_history": []},
    }

    st.session_state.current_session = session_id


st.sidebar.title("Conversations")

if st.sidebar.button("➕ New Chat"):
    session_id = str(uuid.uuid4())
    st.session_state.chat_counter += 1
    chat_name = f"Chat {st.session_state.chat_counter}"

    st.session_state.sessions[session_id] = {
        "chat_name": chat_name, 
        "chat_messages": [],
        "agent_state": {"conversation_history": []},
    }

    st.session_state.current_session = session_id
    st.rerun()


for session_id, session_data in st.session_state.sessions.items():
    if st.sidebar.button(session_data["chat_name"]):
        st.session_state.current_session = session_id
        st.rerun()


current_session = st.session_state.current_session
session_data = st.session_state.sessions[current_session]

chat_messages = session_data["chat_messages"]
agent_state = session_data["agent_state"]


# Email State

if "email_mode" not in st.session_state:
    st.session_state.email_mode = False

if "email_draft" not in st.session_state:
    st.session_state.email_draft = None

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = False

if "show_recipient" not in st.session_state:
    st.session_state.show_recipient = False


for msg in chat_messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input

user_input = st.chat_input("Type your message...")

if user_input:

    with st.chat_message("user"):
        st.markdown(user_input)

    chat_messages.append({"role": "user", "content": user_input})

    agent_state["user_query"] = user_input
    agent_state["conversation_history"].append(
        HumanMessage(content=user_input)
    )

    with st.spinner("Thinking..."):
        result = app.invoke(
            agent_state,
            config={"configurable": {"thread_id": current_session}}
        )

    if result.get("email_draft"):
        st.session_state.email_mode = True
        st.session_state.email_draft = result["email_draft"]

    final_answer = result.get("final_answer", "No response generated.")

    with st.chat_message("assistant"):
        st.markdown(final_answer)

    chat_messages.append({"role": "assistant", "content": final_answer})

    agent_state["conversation_history"].append(
        AIMessage(content=final_answer)
    )

    MAX_MEMORY = 8
    if len(agent_state["conversation_history"]) > MAX_MEMORY:
        agent_state["conversation_history"] = \
            agent_state["conversation_history"][-MAX_MEMORY:]

    # Save updated session
    session_data["chat_messages"] = chat_messages
    session_data["agent_state"] = agent_state


# Email UI

if st.session_state.email_mode and st.session_state.email_draft:

    draft = st.session_state.email_draft

    st.divider()
    st.subheader("Email Draft Preview")

    st.markdown(f"**Subject:** {draft['subject']}")
    st.markdown(draft["body"])

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Send Email"):
            st.session_state.show_recipient = True

    if st.session_state.show_recipient:
        recipient_input = st.text_input(
            "Enter recipient emails (comma separated if multiple)"
        )

        if st.button("Confirm Send") and recipient_input:

            recipients = [
                email.strip()
                for email in recipient_input.split(",")
                if email.strip()
            ]

            if not recipients:
                st.error("Please enter at least one valid email.")
            else:
                with st.spinner("Sending email..."):
                    send_email(recipients, draft["subject"], draft["body"])

                st.success(f"Email sent successfully to {len(recipients)} recipient(s)!")

                st.session_state.email_mode = False
                st.session_state.edit_mode = False
                st.session_state.show_recipient = False
                st.session_state.email_draft = None

    with col2:
        if st.button("Edit Email"):
            st.session_state.edit_mode = True

    with col3:
        if st.button("Cancel"):
            st.session_state.email_mode = False
            st.session_state.edit_mode = False
            st.session_state.show_recipient = False
            st.session_state.email_draft = None
            st.info("Email cancelled.")


# Edit UI

if st.session_state.edit_mode and st.session_state.email_draft:

    st.divider()
    st.subheader("✏️ Modify Email")

    instruction = st.text_input(
        "What would you like to change? (e.g. make it more formal, shorten it)"
    )

    if st.button("Apply Edit") and instruction:

        draft = st.session_state.email_draft

        edit_messages = [
            SystemMessage(
                content=(
                    "You are an email editing assistant.\n"
                    "Modify the email based on user instruction.\n"
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
            HumanMessage(
                content=(
                    f"Current Email:\n"
                    f"Subject: {draft['subject']}\n\n"
                    f"{draft['body']}\n\n"
                    f"Instruction: {instruction}"
                )
            ),
        ]

        with st.spinner("Updating email..."):
            response = executor_llm.invoke(edit_messages)
            new_draft = extract_json(response.content)

        st.session_state.email_draft = new_draft
        st.session_state.email_mode = True
        st.session_state.edit_mode = False

        st.success("Email updated!")
        st.rerun()
