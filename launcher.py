import threading
import uvicorn
import sys
import os
import time
import socket
import flet as ft

def port_in_use(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0

# Detect PyInstaller

FROZEN = getattr(sys, 'frozen', False)

if FROZEN:
    BASE_DIR = sys._MEIPASS
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

sys.path.append(os.path.join(BASE_DIR, "backend"))
sys.path.append(os.path.join(BASE_DIR, "ai_services"))

# -------------- BACKEND ----------------

def run_backend():
    print("Starting backend on http://127.0.0.1:8000")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=False)

# -------------- FRONTEND ----------------

def run_frontend():
    print("Launching frontend...")
    # Импорт фронта как модуля
    import frontend.app as app_module
    ft.app(target=app_module.main)

# -------------- MAIN ----------------

if __name__ == "__main__":
    print("=== BloomBuddy Launcher ===")

    # ---------- Запуск backend ----------
    if port_in_use(8000):
        print("Backend already running. Skipping backend.")
    else:
        threading.Thread(target=run_backend, daemon=True).start()
        time.sleep(5)

    # ---------- Запуск frontend ----------
    run_frontend()
