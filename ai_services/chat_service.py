import json
import random
import torch
from sentence_transformers import SentenceTransformer, util
from transformers import AutoModelForCausalLM, AutoTokenizer

with open("knowledge_base.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

KB_TEXTS = [
    f"{item['crop']} {item['disease']} {' '.join(item['symptoms'])}"
    for item in DATA
]

embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
KB_EMBEDS = embedder.encode(KB_TEXTS, convert_to_tensor=True)

from ollama import Client

ollama = Client()
LLM_NAME = "mistral"

# 💾 MEMORY FOR DIALOG
DIALOG_HISTORY = []  # or dict for multi-user


def llm_generate(history):
    prompt = "You are BloomBuddy, a friendly helpful plant assistant.\n"
    prompt += "Continue the conversation naturally.\n\n"
    prompt += "\n".join([f"{turn['role'].capitalize()}: {turn['content']}" for turn in history])
    prompt += "\nAssistant:"

       # --- FIX STARTS HERE ---
    response = ollama.generate(
        model=LLM_NAME,
        prompt=prompt,
        options={ # Pass generation parameters inside the 'options' dictionary
            "temperature": 0.7,
            "num_predict": 120 # max_tokens usually maps to num_predict in Ollama
        }
    )
    # --- FIX ENDS HERE ---
    return response["response"].strip()



def generate_bot_reply(user_message: str, disease=None):
    global DIALOG_HISTORY

    user_message = user_message.strip()

    # store user message
    DIALOG_HISTORY.append({"role": "user", "content": user_message})

    # If DOCTOR MODE (from YOLO)
    if disease:
        for item in DATA:
            if item["disease"].lower() == disease.lower():
                bot_text = (
                    f"Your plant has {item['disease']}. "
                    f"{' '.join(item['treatment'])}. {item['chat_tip']}"
                )

                DIALOG_HISTORY.append({"role": "assistant", "content": bot_text})
                return bot_text

    # Otherwise do semantic search
    query_emb = embedder.encode([user_message], convert_to_tensor=True)
    sims = util.cos_sim(query_emb, KB_EMBEDS)[0]

    best_idx = int(torch.argmax(sims))
    best_score = float(sims[best_idx])

    if best_score < 0.25:
        reply = random.choice([
            "Could you describe the symptoms in more detail?",
            "What exactly do you see on the leaves or stems?",
            "Tell me more — spots? Color change? Rotting?"
        ])
        DIALOG_HISTORY.append({"role": "assistant", "content": reply})
        return reply

    item = DATA[best_idx]

    # Let LLM write a nice human answer
    bot_text = llm_generate(DIALOG_HISTORY)

    # store in history
    DIALOG_HISTORY.append({"role": "assistant", "content": bot_text})

    return bot_text
