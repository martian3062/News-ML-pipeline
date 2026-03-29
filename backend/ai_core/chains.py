"""
Reusable LangChain chains for the Video Maker Pipeline.
"""

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser

from ai_core.llm_router import llm_router
from ai_core.prompts import VIDEO_SCRIPT_TEMPLATE

def get_video_script_chain():
    """Generate broadcast-style video scripts from articles."""
    prompt = ChatPromptTemplate.from_template(VIDEO_SCRIPT_TEMPLATE)
    return prompt | llm_router.text_model | JsonOutputParser()

def get_video_validation_chain():
    """Validates if an image matches a video scene using Groq Vision."""
    return llm_router.vision_model | StrOutputParser()

