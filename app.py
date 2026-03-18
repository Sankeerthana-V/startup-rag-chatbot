import streamlit as st
from chatbot import get_chat_response
from db import save_chat_log
import uuid

st.set_page_config(page_title="Indian Startup Chatbot", page_icon="💡", layout="wide")
st.title("Indian Startup Chatbot")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for msg in st.session_state.chat_history:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input("Ask a question about Indian startups")

if user_input:
    st.chat_message("user").write(user_input)

    answer = get_chat_response(user_input, st.session_state.chat_history)

    st.chat_message("assistant").write(answer)

    save_chat_log(
      st.session_state.session_id,
      user_input,
      answer
    )

    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.session_state.chat_history.append({"role": "assistant", "content": answer})