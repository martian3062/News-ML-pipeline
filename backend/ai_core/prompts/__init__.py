"""
Reusable prompts for AI-Native News Platform.
"""

SUMMARIZE_TEMPLATE = """
Summarize the following article(s) into a concise briefing.
Focus on the key takeaways, business implications, and actionable insights.

Articles:
{text}

Concise Briefing:
"""

TRANSLATE_TEMPLATE = """
Translate the following business news article from English to {target_language}.
Maintain the professional tone and adapt financial terminology to the local context.

Article:
{text}

Translation:
"""

VIDEO_SCRIPT_TEMPLATE = """
Generate a broadcast-style video script for the following news article.
The script should be divided into segments, each with corresponding visual suggestions.
Format as a JSON list of segments: [{{ "text": "spoken words", "scene": "visual description", "duration": 5 }}]

Article:
{text}

Script (JSON):
"""

CONCIERGE_SYSTEM_PROMPT = """
You are an AI concierge for Economic Times. 
Help users discover news, understand market trends, and find relevant financial products. 
Be friendly, concise, and professional. 
Ask smart questions to understand their needs if points are unclear.
"""

PROFILING_TEMPLATE = """
Help build a user profile based on this conversation.
Identify their profession, financial goals, and news interests.
"""
