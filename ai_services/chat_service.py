def generate_bot_reply(message: str) -> str:
    # TODO: заменить на вызов модели
    if "hello" in message.lower():
        return "Hello there 🌿"
    return "Your plant thanks you for the message 🌱"
