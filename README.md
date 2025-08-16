# Personal AI Assistant

## Description
This repository contains an agentic AI personal assistant designed to help you manage your daily tasks and information with sophisticated, human-like reasoning.

## Features
- Multi-session conversation
- Short Term and Long Term Memory: Learns and persists user information, to-do list with long term Memory
- Tracing & Observability with LangSmith
- Streamlit Web UI

## Getting Started
1. clone the repository
```bash
git clone https://github.com/Harshad1994/personal-ai-assistant.git
```
2. step into personal-ai-assistant
```bash
cd personal-ai-assistant
```
3. create & activate virtual environment with uv
```bash
uv sync
```
or
create it with venv and activate and install dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
4. Create ENV file - replace keys in .env.example with your keys and rename the file to .env

5. Run services
step into personal-ai-assistant/app and run following commands in seperate terminal
```bash
python run_service.py

streamlit run streamlit_app.py user123
```

## Usage
1. Open the streamlit UI
2. Start chatting with the personal assistant
3. You can create new thread using left panel on the UI and seamlessly move between threads

## Technologies
- Python
- LangGraph
- FastAPI
- Langsmith
- trustcall
- Streamlit
- UV (python dependency manager)

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