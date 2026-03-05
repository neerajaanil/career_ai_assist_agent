"""Tool definitions and handlers for the career agent."""

import json
import logging
from typing import Dict, Any
import requests
from .config import Config

logger = logging.getLogger(__name__)


def send_pushover_notification(message: str) -> None:
    """Send a notification via Pushover."""
    if not Config.PUSHOVER_TOKEN or not Config.PUSHOVER_USER:
        logger.warning("Pushover credentials not configured. Skipping notification.")
        return
    
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": Config.PUSHOVER_TOKEN,
                "user": Config.PUSHOVER_USER,
                "message": message,
            },
            timeout=10
        )
        response.raise_for_status()
        logger.info("Pushover notification sent successfully")
    except requests.RequestException as e:
        logger.error(f"Failed to send Pushover notification: {e}")


def record_user_details(
    email: str,
    name: str = "Name not provided",
    notes: str = "not provided"
) -> Dict[str, str]:
    """Record user contact details."""
    message = f"New contact: {name} ({email})\nNotes: {notes}"
    send_pushover_notification(message)
    logger.info(f"Recorded user details: {name} ({email})")
    return {"recorded": "ok", "status": "success"}


def record_unknown_question(question: str) -> Dict[str, str]:
    """Record a question that couldn't be answered."""
    message = f"Unanswered question: {question}"
    send_pushover_notification(message)
    logger.info(f"Recorded unknown question: {question}")
    return {"recorded": "ok", "status": "success"}


RECORD_USER_DETAILS_TOOL = {
    "type": "function",
    "function": {
        "name": "record_user_details",
        "description": (
            "Use this tool to record that a user is interested in being in touch "
            "and provided an email address. Always use this when a user provides "
            "their contact information or expresses interest in connecting."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "The email address of this user"},
                "name": {"type": "string", "description": "The user's name, if they provided it"},
                "notes": {"type": "string", "description": "Any additional information about the conversation"}
            },
            "required": ["email"],
            "additionalProperties": False
        }
    }
}

RECORD_UNKNOWN_QUESTION_TOOL = {
    "type": "function",
    "function": {
        "name": "record_unknown_question",
        "description": (
            "Always use this tool to record any question that couldn't be answered "
            "as you didn't know the answer. Use this even for trivial or unrelated questions."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {"type": "string", "description": "The question that couldn't be answered"}
            },
            "required": ["question"],
            "additionalProperties": False
        }
    }
}

AVAILABLE_TOOLS = [RECORD_USER_DETAILS_TOOL, RECORD_UNKNOWN_QUESTION_TOOL]

TOOL_HANDLERS = {
    "record_user_details": record_user_details,
    "record_unknown_question": record_unknown_question,
}
