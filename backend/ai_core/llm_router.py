"""
AI LLM Router — Groq-Only Architecture (Text & Vision).
"""
import logging
from typing import Optional
from django.conf import settings

from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langchain_core.language_models import BaseChatModel

logger = logging.getLogger(__name__)

class LLMRouter:
    """Routes AI requests to Groq text or vision models."""

    def __init__(self):
        self._text_model = None
        self._vision_model = None

    @property
    def text_model(self) -> ChatGroq:
        if not self._text_model:
            config = settings.AI_CONFIG["text_model"]
            self._text_model = ChatGroq(
                model_name=config["model"],
                groq_api_key=config["api_key"],
                max_tokens=config["max_tokens"],
                temperature=config["temperature"],
                max_retries=1,
            )
        return self._text_model

    @property
    def vision_model(self) -> ChatGroq:
        if not self._vision_model:
            config = settings.AI_CONFIG["vision_model"]
            self._vision_model = ChatGroq(
                model_name=config["model"],
                groq_api_key=config["api_key"],
                max_tokens=config["max_tokens"],
                temperature=config["temperature"],
                max_retries=1,
            )
        return self._vision_model

    def invoke(self, messages: list[BaseMessage], use_vision: bool = False) -> str:
        """Send messages to Groq text model."""
        try:
            model = self.vision_model if use_vision else self.text_model
            response = model.invoke(messages)
            return response.content
        except Exception as e:
            model_type = "Vision" if use_vision else "Text"
            logger.error(f"Groq {model_type} Model Failed: {e}")
            return "I apologize, but I am currently unable to process your request."

# Singleton instance
llm_router = LLMRouter()
