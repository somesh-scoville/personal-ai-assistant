import requests
import json
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ChatAPIError(Exception):
    """Custom exception for chat API related errors"""
    pass

def chat_with_agent(message: str, user_id: str, thread_id: str) -> Dict:
    """
    Send a chat message to the agent and return the response.
    
    Args:
        message (str): The message to send
        user_id (str): The user identifier
        thread_id (str): The thread identifier
    
    Returns:
        Dict: The response from the agent
    
    Raises:
        ChatAPIError: If there's an error communicating with the API
    """
    headers = {
        "Content-Type": "application/json"
    }
    
    payload = {
        "thread_id": thread_id,
        "user_id": user_id,
        "message": message
    }

    try:
        json_data = json.dumps(payload)
        response = requests.post(
            url="http://localhost:8080/chat",
            data=json_data,
            headers=headers,
            timeout=30  # Add timeout
        )
        
        response.raise_for_status()  # Raise exception for non-200 status codes
        return response.json()
        
    except requests.exceptions.Timeout:
        logger.error("Request timed out")
        raise ChatAPIError("Request timed out")
        
    except requests.exceptions.ConnectionError:
        logger.error("Failed to connect to the server")
        raise ChatAPIError("Failed to connect to the server")
        
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        raise ChatAPIError(f"API request failed: {str(e)}")
        
    except json.JSONDecodeError:
        logger.error("Failed to parse API response")
        raise ChatAPIError("Failed to parse API response")
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise ChatAPIError(f"Unexpected error: {str(e)}")

def main():
    user_id = "user123"
    thread_id = "thread456"
    message = "Hello, My name is Harshad and I am a software engineer."
    
    try:
        response = chat_with_agent(message, user_id, thread_id)
        logger.info(f"Response received: {response}")
        
    except ChatAPIError as e:
        logger.error(f"Chat error occurred: {str(e)}")
        
if __name__ == "__main__":
    main()
