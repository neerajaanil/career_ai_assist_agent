"""Gradio application for the career AI agent."""

import logging
import gradio as gr
from .config import Config
from .agent import CareerAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def create_app() -> gr.ChatInterface:
    """Create and configure the Gradio chat interface."""
    try:
        Config.validate()
    except (ValueError, FileNotFoundError) as e:
        logger.error(f"Configuration error: {e}")
        raise
    
    logger.info("Initializing career agent...")
    agent = CareerAgent()
    logger.info(f"Career agent initialized for {agent.name}")
    
    interface = gr.ChatInterface(
        fn=agent.chat,
        title=f"Chat with {agent.name}",
        description=f"Ask me anything about {agent.name}'s career, background, skills, and experience.",
        examples=[
            "What is your background?",
            "Tell me about your experience",
            "What skills do you have?",
            "What projects have you worked on?",
        ],
    )
    
    return interface


def main():
    """Main entry point for running the application."""
    try:
        interface = create_app()
        interface.launch(
            server_name=Config.SERVER_HOST,
            server_port=Config.SERVER_PORT,
            share=Config.SHARE,
            show_error=True
        )
    except Exception as e:
        logger.error(f"Failed to launch application: {e}")
        raise


if __name__ == "__main__":
    main()
