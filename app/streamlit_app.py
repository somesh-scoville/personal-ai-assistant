import streamlit as st
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import os

# Initialize session state for chat history and threads
if 'chat_threads' not in st.session_state:
    st.session_state.chat_threads = {'Main Thread': []}
if 'current_thread' not in st.session_state:
    st.session_state.current_thread = 'Main Thread'


def create_new_thread(thread_name):
    if thread_name not in st.session_state.chat_threads:
        st.session_state.chat_threads[thread_name] = []
        st.session_state.current_thread = thread_name

def get_chat_history():
    return st.session_state.chat_threads[st.session_state.current_thread]


def my_agent_function(prompt):
    # This function should contain the logic to get a response from your agent.
    # For demonstration, we'll just return a simple response.
    return f"Response to: {prompt}"

def main():
    st.title("Chat Assistant")

    # Sidebar for thread management
    with st.sidebar:
        st.header("Thread Management")
        new_thread_name = st.text_input("New Thread Name")
        if st.button("Create New Thread"):
            if new_thread_name:
                create_new_thread(new_thread_name)

        # Thread selection
        st.header("Select Thread")
        selected_thread = st.selectbox(
            "Choose a thread",
            options=list(st.session_state.chat_threads.keys())
        )
        if selected_thread != st.session_state.current_thread:
            st.session_state.current_thread = selected_thread

    # Display chat history
    for message in get_chat_history():
        if isinstance(message, HumanMessage):
            with st.chat_message("user"):
                st.write(message.content)
        elif isinstance(message, AIMessage):
            with st.chat_message("assistant"):
                st.write(message.content)

    # Chat input
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to chat history
        st.session_state.chat_threads[st.session_state.current_thread].append(HumanMessage(content=prompt))
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        # Get AI response using the existing agent
        response = my_agent_function(prompt)
        ai_message = AIMessage(content=response)

        # Add AI response to chat history
        st.session_state.chat_threads[st.session_state.current_thread].append(ai_message)
        
        # Display AI response
        with st.chat_message("assistant"):
            st.write(response)

if __name__ == "__main__":
    main()
