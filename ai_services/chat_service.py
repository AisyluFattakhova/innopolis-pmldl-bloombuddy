import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open("knowledge_base.json", "r") as f:
    DATA = json.load(f)

texts = [
    f"{item['crop']} {item['disease']} {' '.join(item['symptoms'])}"
    for item in DATA
]
vectorizer = TfidfVectorizer().fit(texts)
matrix = vectorizer.transform(texts)

def generate_bot_reply(user_message: str = None, crop: str = None, disease: str = None):
    user_message = user_message.lower().strip() if user_message else ""


    greetings = ["hi", "hello", "hey", "what's up", "hey there"]
    thanks = ["thanks", "thank you", "thx"]
    bye = ["bye", "goodbye", "see you", "bb"]

    if any(word in user_message for word in greetings):
        return "🌿 Hello! I’m BloomBuddy — your plant health assistant. How can I help your plants today?"
    if any(word in user_message for word in thanks):
        return "💚 You’re very welcome! Glad to help your plants stay healthy."
    if any(word in user_message for word in bye):
        return "👋 Goodbye! Remember to water your plants regularly!"

    # 🌱 If disease info is known (from CV model)
    if crop and disease:
        for item in DATA:
            if item["crop"].lower() == crop.lower() and item["disease"].lower() == disease.lower():
                return (
                    f"It looks like your {item['crop']} has **{item['disease']}**.\n"
                    + "\n".join(f"- {t}" for t in item["treatment"])
                    + f"\n\n{item['chat_tip']}"
                )

    # If it's a text-based query
    user_vec = vectorizer.transform([user_message])
    sims = cosine_similarity(user_vec, matrix).flatten()
    best_match = DATA[sims.argmax()]
    return (
        f"It looks like your {best_match['crop']} might have **{best_match['disease']}**.\n"
        + "\n".join(f"- {t}" for t in best_match['treatment'])
        + f"\n\n{best_match['chat_tip']}"
    )
