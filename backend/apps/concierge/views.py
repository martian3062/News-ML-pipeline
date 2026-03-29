import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import ConversationSession
from .serializers import ChatMessageSerializer

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([AllowAny])
def chat(request):
    """Simple chat endpoint — processes message and returns AI response."""
    serializer = ChatMessageSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_message = serializer.validated_data["message"]
    session_id = serializer.validated_data.get("session_id")

    # Get or create session
    if session_id:
        try:
            session = ConversationSession.objects.get(id=session_id)
        except ConversationSession.DoesNotExist:
            session = ConversationSession.objects.create(
                user=request.user if request.user.is_authenticated else None
            )
    else:
        session = ConversationSession.objects.create(
            user=request.user if request.user.is_authenticated else None
        )

    # Add user message
    session.messages.append({"role": "user", "content": user_message})

    # Generate AI response
    try:
        from ai_core.llm_router import llm_router
        from langchain_core.messages import SystemMessage, HumanMessage

        system_msg = SystemMessage(content=(
            "You are an AI concierge for ET (Economic Times). "
            "Help users discover news, understand market trends, "
            "and find relevant financial products. Be friendly, concise, "
            "and helpful. Ask smart questions to understand their needs."
        ))

        messages = [system_msg]
        for msg in session.messages:
            if msg["role"] == "user":
                messages.append(HumanMessage(content=msg["content"]))

        response_text = llm_router.invoke(messages)
    except Exception as e:
        logger.warning(f"LLM failed: {e}")
        response_text = (
            "I'm your ET Concierge! I can help you discover personalized news, "
            "track market trends, and find the right financial products. "
            "What are you interested in today?"
        )

    # Add assistant response
    session.messages.append({"role": "assistant", "content": response_text})
    session.save()

    return Response({
        "session_id": str(session.id),
        "response": response_text,
        "messages": session.messages,
    })


@api_view(["GET"])
@permission_classes([AllowAny])
def get_session(request, session_id):
    """Get conversation session by ID."""
    try:
        session = ConversationSession.objects.get(id=session_id)
        return Response({
            "session_id": str(session.id),
            "messages": session.messages,
            "session_type": session.session_type,
        })
    except ConversationSession.DoesNotExist:
        return Response({"error": "Session not found"}, status=404)
