import json
import logging

import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


class ChatAPIError(Exception):
    """Custom exception for chat API related errors."""

    pass


def chat_with_agent(message: str, user_id: str, thread_id: str) -> dict:
    """Send a chat message to the agent and return the response.

    Args:
        message: The message to send
        user_id: The user identifier
        thread_id: The thread identifier
    Returns:
        The response from the agent
    Raises:
        ChatAPIError: If there's an error communicating with the API
    """
    headers = {"Content-Type": "application/json"}

    payload = {"thread_id": thread_id, "user_id": user_id, "message": message}

    try:
        json_data = json.dumps(payload)
        response = requests.post(
            url="http://localhost:8080/chat",
            data=json_data,
            headers=headers,
            timeout=30,  # Add timeout
        )

        response.raise_for_status()  # Raise exception for non-200 status codes
        return response.json()

    except requests.exceptions.Timeout as err:
        logger.error("Request timed out")
        raise ChatAPIError("Request timed out") from err

    except requests.exceptions.ConnectionError as err:
        logger.error("Failed to connect to the server")
        raise ChatAPIError("Failed to connect to the server") from err

    except requests.exceptions.RequestException as err:
        logger.error(f"API request failed: {err!s}")
        raise ChatAPIError(f"API request failed: {err!s}") from err

    except json.JSONDecodeError as err:
        logger.error("Failed to parse API response")
        raise ChatAPIError("Failed to parse API response") from err

    except Exception as err:
        logger.error(f"Unexpected error: {err!s}")
        raise ChatAPIError(f"Unexpected error: {err!s}") from err


def main():
    user_id = "user123"
    thread_id = "thread456"
    message = "Hello, My name is Harshad and I am a software engineer."

    try:
        response = chat_with_agent(message, user_id, thread_id)
        logger.info(f"Response received: {response}")

    except ChatAPIError as e:
        logger.error(f"Chat error occurred: {e!s}")


if __name__ == "__main__":
    main()
