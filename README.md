# Personal AI Assistant

## Description
This repository implements an advanced AI personal assistant powered by LLM agents. It's designed to assist with daily tasks, information management, and decision-making through natural conversations while maintaining context and memory across sessions.

## Features
- **Intelligent Conversations**: Natural, context-aware dialogue with sophisticated reasoning
- **Memory Management**:
    - Short-term memory for ongoing conversations
    - Long-term memory for user preferences and historical data
    - Persistent todo lists and user profiles
- **Multi-Session Support**: Maintain multiple parallel conversation threads
- **Observability**: Complete tracing and monitoring via LangSmith
- **Modern Architecture**:
    - Fast and responsive Streamlit web interface
    - RESTful backend with FastAPI
    - Efficient LLM interactions through Groq

## Getting Started
1. **Clone the repository**
    ```bash
    git clone https://github.com/Harshad1994/personal-ai-assistant.git
    cd personal-ai-assistant
    ```

2. **Set up the environment**
    ```bash
    # Using UV (recommended)
    uv sync

    # OR using venv
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Configure environment variables**
    - Copy `.env.example` to `.env`
    - Replace placeholder values with your actual API keys

4. **Run the services**
    ```bash
    # Terminal 1: Start the backend service
    cd app
    python run_service.py

    # Terminal 2: Launch the Streamlit UI
    cd app
    streamlit run streamlit_app.py user123
    ```

## Usage
1. **Open the Streamlit UI**
    - Navigate to http://localhost:8501 after starting the services
    - Enter your username or ID when prompted

2. **Interact with the Assistant**
    - Type your messages in the chat interface
    - The assistant will maintain context across conversations
    - Use natural language to communicate your needs

3. **Manage Conversations**
    - Create new conversation threads using the sidebar
    - Switch between different threads to manage multiple topics
    - Each thread maintains its own context and history
    - Todo List and User Profile is maintained across threads.

4. **Access Features**
    - Use the assistant for task management
    - Store and retrieve information across sessions
    - Get help with various daily activities

## Technologies
- **Python** - Primary programming language
- **LangGraph** - LLM framework for building conversational AI Agents
- **FastAPI** - Backend API framework
- **Groq API** - Free LLM Usage
- **LangSmith** - Observability and debugging platform
- **Streamlit** - Web interface framework
- **UV** - Modern Python package installer and resolver

## Architecture
High-level overview of system architecture and components.

## Development
Guidelines for development and contribution.

## Testing
Information about testing procedures and frameworks.

## License
MIT License

## Contributing
Guidelines for contributing to the project.

## Contact
harshadkunjir@gmail.com\
https://www.linkedin.com/in/harshad1994/