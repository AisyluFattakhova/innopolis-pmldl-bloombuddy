from sentence_transformers import SentenceTransformer, util
import torch
import json
import random
from ollama import Client

# -------------------
# LOAD KB
# -------------------
with open("knowledge_base.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

KB_TEXTS = [
    f"{item['crop']} {item['disease']} {' '.join(item['symptoms'])}" 
    for item in DATA
]

# -------------------
# EMBEDDER LOCAL
# -------------------
embedder = SentenceTransformer("models/all-MiniLM-L6-v2")  # локальная модель
KB_EMBEDS = embedder.encode(KB_TEXTS, convert_to_tensor=True)

# -------------------
# LLM
# -------------------
ollama = Client()
LLM_NAME = "mistral:7b-instruct-q4_0"

# -------------------
# MEMORY
# -------------------
DIALOG_HISTORY = []

# -------------------
# RAG LLM GENERATOR
# -------------------
def llm_generate(history, item):
    prompt = (
        "You are BloomBuddy, a friendly plant assistant.\n"
        "Use ONLY the provided disease info. Do NOT invent treatments.\n\n"
        f"Disease: {item['disease']}\n"
        f"Crop: {item['crop']}\n"
        f"Symptoms: {', '.join(item['symptoms'])}\n"
        f"Treatment: {', '.join(item['treatment'])}\n"
        f"Tip: {item['chat_tip']}\n\n"
        "Conversation:\n"
    )
    prompt += "\n".join([f"{turn['role'].capitalize()}: {turn['content']}" for turn in history])
    prompt += "\nAssistant:"

    resp = ollama.generate(
        model=LLM_NAME,
        prompt=prompt,
        options={"temperature": 0.4, "num_predict": 150}
    )
    return resp["response"].strip()


# -------------------
# MAIN BOT FUNCTION
# -------------------
def generate_bot_reply(user_message: str, disease=None):
    global DIALOG_HISTORY
    user_message = user_message.strip()
    DIALOG_HISTORY.append({"role": "user", "content": user_message})

    # 1) DOCTOR MODE
    if disease:
        for item in DATA:
            if item["disease"].lower() == disease.lower():
                bot_text = llm_generate(DIALOG_HISTORY, item)
                DIALOG_HISTORY.append({"role": "assistant", "content": bot_text})
                return bot_text

    # 2) SEMANTIC SEARCH
    query_vec = embedder.encode([user_message], convert_to_tensor=True)
    sims = util.cos_sim(query_vec, KB_EMBEDS)[0]

    best_idx = int(torch.argmax(sims))
    best_score = float(sims[best_idx])

    # Low similarity → ask clarification
    if best_score < 0.25:
        reply = random.choice([
            "Could you describe the symptoms in more detail?",
            "What exactly do you see on the leaves or stems?",
            "Tell me more — spots? Color change? Wilting?"
        ])
        DIALOG_HISTORY.append({"role": "assistant", "content": reply})
        return reply

    # KB item
    item = DATA[best_idx]

    # 3) LLM generates human-like answer
    bot_text = llm_generate(DIALOG_HISTORY, item)
    DIALOG_HISTORY.append({"role": "assistant", "content": bot_text})
    return bot_text
