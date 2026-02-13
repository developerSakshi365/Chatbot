# chatbot.py

def get_bot_response(user_message, conversation_history=None):
    """
    Customer Support / FAQ Chatbot
    Provides contextual responses for support-related queries.
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

    # ---------------- GREETINGS ----------------

    if any(word in user_message_lower for word in ["hello", "hi", "hey"]):
        return "Hello 👋 Welcome to Customer Support. How can I assist you today?"

    if "how are you" in user_message_lower:
        return "I'm here and ready to assist you 😊 How may I help you today?"

    if any(word in user_message_lower for word in ["bye", "goodbye"]):
        return "Thank you for contacting support. Have a great day! 👋"

    # ---------------- ORDER SUPPORT ----------------

    if "track" in user_message_lower or "order status" in user_message_lower:
        return (
            "Sure 📦 Please provide your Order ID so I can help you track your order."
        )

    if "order id" in user_message_lower:
        return (
            "Thank you for providing your Order ID. "
            "Your order is currently being processed and will be shipped within 24-48 hours."
        )

    if "cancel order" in user_message_lower:
        return (
            "I can help you cancel your order. "
            "Please provide your Order ID. Orders can only be canceled before shipping."
        )

    # ---------------- SHIPPING ----------------

    if "shipping" in user_message_lower or "delivery time" in user_message_lower:
        return (
            "🚚 Standard delivery takes 3-5 business days. "
            "Express delivery takes 1-2 business days."
        )

    if "international shipping" in user_message_lower:
        return (
            "🌍 Yes, we offer international shipping. "
            "Delivery times vary depending on your country."
        )

    # ---------------- RETURNS & REFUNDS ----------------

    if "refund" in user_message_lower:
        return (
            "💰 Refunds are processed within 5-7 business days after we receive the returned item."
        )

    if "return policy" in user_message_lower:
        return (
            "🔄 You can return products within 30 days of purchase. "
            "Items must be unused and in original packaging."
        )

    # ---------------- ACCOUNT SUPPORT ----------------

    if "reset password" in user_message_lower or "forgot password" in user_message_lower:
        return (
            "🔐 To reset your password, click on 'Forgot Password' on the login page "
            "and follow the instructions sent to your email."
        )

    if "update email" in user_message_lower:
        return (
            "📧 To update your email address, go to Account Settings > Personal Information."
        )

    if "delete account" in user_message_lower:
        return (
            "⚠️ We're sorry to see you go. Please contact our support team at support@example.com "
            "to request account deletion."
        )

    # ---------------- PAYMENT ----------------

    if "payment methods" in user_message_lower:
        return (
            "💳 We accept Credit/Debit Cards, UPI, Net Banking, and PayPal."
        )

    if "payment failed" in user_message_lower:
        return (
            "If your payment failed, please check your bank balance or try another payment method."
        )

    # ---------------- FAQ GENERIC ----------------

    if "help" in user_message_lower or "what can you do" in user_message_lower:
        return (
            "I can assist with:\n"
            "• Order tracking\n"
            "• Shipping information\n"
            "• Returns & refunds\n"
            "• Account issues\n"
            "• Payment support\n\n"
            "How can I help you today?"
        )

    # ---------------- CONTEXTUAL FOLLOW-UP ----------------

    if user_message_lower in ["yes", "okay", "ok"]:
        if last_bot_message:
            return "Sure 🙂 Could you please provide more details so I can assist you better?"
        return "Alright 🙂 How can I assist you further?"

    if user_message_lower in ["no", "not really"]:
        return "No problem 😊 Let me know if you need anything else."

    # ---------------- DEFAULT RESPONSE ----------------

    return (
        "I'm sorry, I didn't fully understand your request. "
        "Could you please provide more details so I can assist you better?"
    )
