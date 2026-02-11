# chatbot.py

def get_bot_response(user_message, conversation_history=None):
    """
    Generates a contextual chatbot response based on the user's message
    and previous conversation history.

    Args:
        user_message (str): The current message sent by the user.
        conversation_history (list): Previous messages in the conversation
        in the format [{"role": "user/bot", "content": "..."}].

    Returns:
        str: Context-aware chatbot response.
    """

    user_message_lower = user_message.lower().strip()

    # ---------------- CONTEXT HANDLING ----------------
    last_user_message = None
    last_bot_message = None

    if conversation_history:
        for msg in reversed(conversation_history):
            if msg["role"] == "user" and not last_user_message:
                last_user_message = msg["content"].lower()
            if msg["role"] == "bot" and not last_bot_message:
                last_bot_message = msg["content"].lower()
            if last_user_message and last_bot_message:
                break

    # Follow-up handling
    if user_message_lower in ["ok", "okay", "hmm", "huh"]:
        return "Alright 🙂 If you have a question or want to know something, just ask."

    if user_message_lower in ["no", "nah"]:
        return "No problem 👍 Let me know whenever you need help."

    if user_message_lower in ["yes", "yeah", "yep"]:
        if last_bot_message and "help" in last_bot_message:
            return "Great! You can ask me about technology, fun facts, time, or general questions."
        return "Awesome 😊 What would you like to talk about?"

    if user_message_lower in ["what", "why", "how"]:
        return "Could you please ask a complete question? That will help me understand better 🙂"

    # ---------------- RULE-BASED RESPONSES ----------------

    if any(word in user_message_lower for word in ["hello", "hi", "hey", "greetings"]):
        return "Hello! How can I assist you today?"

    elif "how are you" in user_message_lower:
        return "I'm doing great 😄 Thanks for asking! How can I help you today?"

    elif any(word in user_message_lower for word in ["bye", "goodbye", "see you"]):
        return "Goodbye! Have a great day 👋"

    elif "help" in user_message_lower or "what can you do" in user_message_lower:
        return (
            "I can help with explanations, fun facts, time & date, "
            "technology topics, and general questions. Would you like some help?"
        )

    elif user_message_lower.startswith("what is"):
        topic = user_message_lower.replace("what is", "").strip()
        return (
            f"{topic.capitalize()} is an interesting topic. "
            f"I can explain it in simple terms or in detail—just tell me 😊"
        )

    elif "quantum" in user_message_lower:
        return (
            "Quantum computing uses principles like superposition and entanglement "
            "to solve certain problems faster than classical computers."
        )

    elif "fun fact" in user_message_lower or "fact" in user_message_lower:
        import random
        facts = [
            "Honey never spoils.",
            "Octopuses have three hearts.",
            "A day on Venus is longer than its year.",
            "Bananas are berries, strawberries are not.",
            "The shortest war in history lasted only 38 minutes."
        ]
        return random.choice(facts)

    elif "your name" in user_message_lower or "who are you" in user_message_lower:
        return "I'm ChatBot AI 🤖, here to chat with you and help answer your questions."

    elif "time" in user_message_lower or "date" in user_message_lower:
        from datetime import datetime
        now = datetime.now()
        return now.strftime("Today is %B %d, %Y and the time is %I:%M %p")

    elif "thank" in user_message_lower:
        return "You're welcome! 😊 Happy to help."

    # ---------------- CONTEXTUAL FALLBACK ----------------

    if last_user_message and last_user_message != user_message_lower:
        return (
            f"You earlier mentioned '{last_user_message}'. "
            f"Could you tell me what exactly you want to know about it?"
        )

    return (
        "I’m still learning 🤖 Could you please rephrase or ask a complete question?"
    )
