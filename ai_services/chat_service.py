import json
import random
import torch
from ollama import Client
from sentence_transformers import SentenceTransformer, util

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

KB_TEXTS = [
    f"{item['crop']} {item['disease']} {' '.join(item['symptoms'])}"
    for item in DATA
]

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
KB_EMBEDS = embedder.encode(KB_TEXTS, convert_to_tensor=True)



ollama = Client()
LLM_NAME = "mistral"

# 💾 MEMORY FOR DIALOG
DIALOG_HISTORY = []


# ==========================
# LLM: RAG RESPONSE BUILDER
# ==========================
def llm_generate(history, item):
    """Generate a natural answer strictly based on the retrieved KB item."""
    prompt = (
        "You are BloomBuddy, a friendly helpful plant assistant.\n"
        "Use ONLY the following information from the plant disease database.\n"
        "Do NOT invent new chemicals or treatments.\n\n"
        f"Disease: {item['disease']}\n"
        f"Crop: {item['crop']}\n"
        f"Symptoms: {', '.join(item['symptoms'])}\n"
        f"Treatment: {', '.join(item['treatment'])}\n"
        f"Tip: {item['chat_tip']}\n\n"
        "Answer the user's question clearly and conversationally.\n\n"
        "Conversation:\n"
    )

    prompt += "\n".join([f"{turn['role'].capitalize()}: {turn['content']}" for turn in history])
    prompt += "\nAssistant:"

    response = ollama.generate(
        model=LLM_NAME,
        prompt=prompt,
        options={
            "temperature": 0.5,
            "num_predict": 150
        }
    )

    return response["response"].strip()


# ==========================
# MAIN ENTRYPOINT
# ==========================
def generate_bot_reply(user_message: str, disease=None):
    global DIALOG_HISTORY

    user_message = user_message.strip()

    # Save user message
    DIALOG_HISTORY.append({"role": "user", "content": user_message})

    # ===============================
    # 1) DOCTOR MODE (YOLO predicts)
    # ===============================
    if disease:
        for item in DATA:
            if item["disease"].lower() == disease.lower():
                bot_text = llm_generate(DIALOG_HISTORY, item)
                DIALOG_HISTORY.append({"role": "assistant", "content": bot_text})
                return bot_text

    # ===============================
    # 2) SEMANTIC RETRIEVAL
    # ===============================
    query_emb = embedder.encode([user_message], convert_to_tensor=True)
    sims = util.cos_sim(query_emb, KB_EMBEDS)[0]

    best_idx = int(torch.argmax(sims))
    best_score = float(sims[best_idx])

    # If irrelevant user question
    if best_score < 0.25:
        reply = random.choice([
            "Could you describe the symptoms in more detail?",
            "What exactly do you see on the leaves or stems?",
            "Tell me more — spots? Color change? Rotting?"
        ])
        DIALOG_HISTORY.append({"role": "assistant", "content": reply})
        return reply

    # Retrieved KB item
    item = DATA[best_idx]

    # ===============================
    # 3) LLM GENERATION USING KB
    # ===============================
    bot_text = llm_generate(DIALOG_HISTORY, item)

    DIALOG_HISTORY.append({"role": "assistant", "content": bot_text})
    return bot_text
