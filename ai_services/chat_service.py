from sentence_transformers import SentenceTransformer, util
import torch
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import re

# -------------------
# LOAD KB
# -------------------
with open("knowledge_base.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

KB_TEXTS = [
    f"{item['crop']} {item['disease']} {' '.join(item['symptoms'])}" 
    for item in DATA
]


def generate_bot_reply(
        user_message: str = None,
        crop: str = None,
        disease: str = None,
        is_first_message: bool = False
):
    user_message = (user_message or "").lower().strip()

    greeting_words = [
        "hi", "hello", "hey", "good morning", "good evening",
        "good afternoon", "hey there", "what's up", "sup"
    ]
    thanks_words = [
        "thanks", "thank you", "thx", "thanks a lot",
        "thank u", "much appreciated"
    ]
    bye_words = [
        "bye", "goodbye", "see you", "see ya", "bb",
        "later", "take care"
    ]

    greeting_replies = [
        "🌿 Hello!",
        "🍃 Hi there!",
        "🌱 Hey!",
        "🌼 Hello!"
    ]
    greeting_rep_cont = [
        "🌿 Hello! How can I help your plants today?",
        "🍃 Hi there! What plant are we taking care of?",
        "🌱 Hey! Need help diagnosing your plant?",
        "🌼 Hello! I’m here to help with any plant issues."
    ]
    thanks_replies = [
        "💚 You're welcome! Happy to help.",
        "🌿 Glad I could help!",
        "🍀 Anytime!",
        "🌱 You’re very welcome!"
    ]
    bye_replies = [
        "👋 Goodbye! Take care of your plants!",
        "🌿 See you later! Stay green!",
        "🍀 Bye-bye! Wishing your plants good health.",
        "🌱 Until next time! Let me know if you need my help."
    ]

    def starts_with_any(text, words):
        """
        True if trigger word appears within first 3 words.
        Avoids detecting 'hi' inside 'behind' or 'him'.
        """
        first_three = " ".join(text.split()[:3])
        return any(re.search(rf"\b{w}\b", first_three) for w in words)

    def contains_any(text, words):
        """General containment check using whole words."""
        return any(re.search(rf"\b{w}\b", text) for w in words)

    # More precise smalltalk detection:
    has_greeting = starts_with_any(user_message, greeting_words)
    has_thanks   = contains_any(user_message, thanks_words)
    has_bye      = contains_any(user_message, bye_words)

    def clean_message(msg):
        # Remove trigger words fully
        all_words = greeting_words + thanks_words + bye_words
        msg = re.sub(r'\b(?:' + "|".join(map(re.escape, all_words)) + r')\b', '', msg)
        return msg.strip()

    core_text = clean_message(user_message)
    only_smalltalk = len(core_text) < 3  # mostly smalltalk

    if only_smalltalk:
        if len(user_message) > 0:
            reply_parts = []

            if has_greeting:
                reply_parts.append(random.choice(greeting_rep_cont))
            if has_thanks:
                reply_parts.append(random.choice(thanks_replies))
            if has_bye:
                reply_parts.append(random.choice(bye_replies))

            if not reply_parts:
                reply_parts.append(random.choice(greeting_replies))

            return " ".join(reply_parts)

    # Mixed message → smalltalk prefix + semantic answer
    prefix_parts = []
    if has_greeting:
        prefix_parts.append(random.choice(greeting_replies))
    if has_thanks:
        prefix_parts.append(random.choice(thanks_replies))
    if has_bye:
        prefix_parts.append(random.choice(bye_replies))

    prefix = " ".join(prefix_parts)

    if crop and disease:
        for item in DATA:
            if item["crop"].lower() == crop.lower() and item["disease"].lower() == disease.lower():
                result = (
                    f"It looks like your {item['crop']} has {item['disease']}.\n"
                    + "\n".join(f"- {t}" for t in item["treatment"])
                    + f"\n{item['chat_tip']}"
                )
                return (prefix + " " + result).strip()

    user_vec = vectorizer.transform([user_message])
    sims = cosine_similarity(user_vec, matrix).flatten()
    best_match = DATA[sims.argmax()]

    result = (
        f"It looks like your plant might have {best_match['disease']}.\n"
        + "\n".join(f"- {t}" for t in best_match['treatment'])
        + f"\n{best_match['chat_tip']}"
    )

    if prefix:
        return prefix + "\n" + result

    return result
