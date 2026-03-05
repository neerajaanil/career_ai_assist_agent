"""Career agent for answering questions about career background."""

import json
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI
from .config import Config
from .data_loader import DataLoader
from .tools import AVAILABLE_TOOLS, TOOL_HANDLERS

logger = logging.getLogger(__name__)


class CareerAgent:
    """AI agent that answers questions about career background and experience."""
    
    def __init__(
        self,
        name: Optional[str] = None,
        linkedin_pdf_path: Optional[str] = None,
        summary_txt_path: Optional[str] = None,
        openai_model: Optional[str] = None
    ):
        self.name = name or Config.AGENT_NAME
        self.openai = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.model = openai_model or Config.OPENAI_MODEL
        
        linkedin_path = linkedin_pdf_path or Config.LINKEDIN_PDF_PATH
        summary_path = summary_txt_path or Config.SUMMARY_TXT_PATH
        self.data_loader = DataLoader(linkedin_path, summary_path)
        
        logger.info("Loading career data...")
        self.linkedin_content = self.data_loader.load_linkedin_profile()
        self.summary_content = self.data_loader.load_summary()
        logger.info("Career data loaded successfully")
    
    def _get_system_prompt(self) -> str:
        """Generate the system prompt for the agent."""
        return (
            f"You are acting as {self.name}. You are answering questions on "
            f"{self.name}'s website, particularly questions related to {self.name}'s "
            f"career, background, skills and experience.\n\n"
            f"Your responsibility is to represent {self.name} for interactions on "
            f"the website as faithfully as possible. You are given a summary of "
            f"{self.name}'s background and LinkedIn profile which you can use to "
            f"answer questions.\n\n"
            f"Be professional and engaging, as if talking to a potential client or "
            f"future employer who came across the website.\n\n"
            f"If you don't know the answer to any question, use your "
            f"record_unknown_question tool to record the question that you couldn't "
            f"answer, even if it's about something trivial or unrelated to career.\n\n"
            f"If the user is engaging in discussion, try to steer them towards getting "
            f"in touch via email; ask for their email and record it using your "
            f"record_user_details tool.\n\n"
            f"## Summary:\n{self.summary_content}\n\n"
            f"## LinkedIn Profile:\n{self.linkedin_content}\n\n"
            f"With this context, please chat with the user, always staying in "
            f"character as {self.name}."
        )
    
    def _handle_tool_calls(self, tool_calls: List[Any]) -> List[Dict[str, Any]]:
        """Handle tool calls from the OpenAI response."""
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse tool arguments: {e}")
                continue
            
            logger.info(f"Tool called: {tool_name} with arguments: {arguments}")
            
            handler = TOOL_HANDLERS.get(tool_name)
            if not handler:
                logger.warning(f"Unknown tool: {tool_name}")
                result = {"error": f"Unknown tool: {tool_name}"}
            else:
                try:
                    result = handler(**arguments)
                except Exception as e:
                    logger.error(f"Error executing tool {tool_name}: {e}")
                    result = {"error": str(e)}
            
            results.append({
                "role": "tool",
                "content": json.dumps(result),
                "tool_call_id": tool_call.id
            })
        
        return results
    
    def _convert_gradio_history(self, history: Optional[List]) -> List[Dict[str, str]]:
        """Convert Gradio chat history to OpenAI message format."""
        messages = []
        if not history:
            return messages
        
        for item in history:
            user_msg = None
            bot_msg = None
            
            if isinstance(item, (list, tuple)):
                if len(item) >= 2:
                    user_msg = item[0]
                    bot_msg = item[1]
            elif isinstance(item, dict):
                role = item.get("role")
                content = item.get("content")
                if role == "user":
                    user_msg = content
                elif role == "assistant":
                    bot_msg = content
            
            if user_msg:
                messages.append({"role": "user", "content": user_msg})
            if bot_msg:
                messages.append({"role": "assistant", "content": bot_msg})
        
        return messages
    
    def chat(self, message: str, history: Optional[List] = None) -> str:
        """Process a chat message and return a response."""
        messages = [{"role": "system", "content": self._get_system_prompt()}]
        history_messages = self._convert_gradio_history(history)
        messages.extend(history_messages)
        messages.append({"role": "user", "content": message})
        
        max_iterations = 10
        iteration = 0
        
        while iteration < max_iterations:
            iteration += 1
            
            try:
                response = self.openai.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    tools=AVAILABLE_TOOLS,
                    temperature=0.7
                )
            except Exception as e:
                logger.error(f"OpenAI API error: {e}")
                return "I apologize, but I'm experiencing technical difficulties. Please try again later."
            
            message_obj = response.choices[0].message
            finish_reason = response.choices[0].finish_reason
            
            if finish_reason == "tool_calls" and message_obj.tool_calls:
                tool_calls = message_obj.tool_calls
                results = self._handle_tool_calls(tool_calls)
                messages.append(message_obj)
                messages.extend(results)
                continue
            
            if message_obj.content:
                return message_obj.content
            else:
                return "I apologize, but I couldn't generate a response. Please try again."
        
        logger.warning("Exceeded maximum tool call iterations")
        return "I apologize, but I'm having trouble processing your request. Please try rephrasing your question."
