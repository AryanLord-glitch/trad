import os
import eel
import pywhatkit
import time
import pyautogui
import pyperclip

from engine.command import speak
from engine.config import ASSISTANT_NAME


# =========================
# 🔊 Assistant startup sound
# =========================
@eel.expose
def playAssistantSound():
    from playsound import playsound
    playsound("www/assets/audio/start_sound.mp3")


# =========================
# 🪟 WINDOWS APP PATHS
# =========================
APP_PATHS = {
    "notepad": "notepad.exe",

    "ms word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",
    "word": r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE",

    "notion": r"C:\Users\91859\AppData\Roaming\Notion\Notion.exe",

    # WhatsApp Desktop (Store)
    "whatsapp": "explorer.exe shell:AppsFolder\\5319275A.WhatsAppDesktop_cv1g1gvanyjgm!App",

    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
}


# =========================
# 👥 WHATSAPP CONTACTS
# =========================
CONTACTS = {
    "ma": "MA",
    "abhi": "ABHI",
    "adithyan": "ADITHYAN",
    "aswanidev": "Aswanidev",
    "hari": "Hari",
    "arun": "Arun"
}


# =========================
# 📝 WHATSAPP TEMPLATES (FEATURE B)
# =========================
TEMPLATES = {
    "busy": "I am busy right now, will text you later.",
    "reached": "I have reached safely.",
    "on my way": "I am on my way.",
    "call later": "I will call you later."
}


# =========================
# 🪟 OPEN WINDOWS APP
# =========================
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("open", "").strip().lower()

    for app in APP_PATHS:
        if app in query:
            eel.DisplayMessage(f"Opening {app}")
            speak(f"Opening {app}")
            os.system(APP_PATHS[app])
            return

    speak("Application not found")
    eel.DisplayMessage("Application not found")


# =========================
# ▶️ PLAY YOUTUBE
# =========================
def playCommand(query):
    query = query.replace(ASSISTANT_NAME, "").replace("play", "").strip()

    if query == "":
        speak("Please tell me what to play")
        return

    speak(f"Playing {query} on YouTube")
    pywhatkit.playonyt(query)


# =========================
# 🧭 OPEN WHATSAPP CHAT (FEATURE D)
# =========================
def openWhatsAppChat(contact_name):
    os.system(APP_PATHS["whatsapp"])
    time.sleep(6)

    pyautogui.hotkey("ctrl", "f")
    time.sleep(1)

    pyperclip.copy(contact_name)
    pyautogui.hotkey("ctrl", "v")
    time.sleep(1)

    pyautogui.press("enter")
    time.sleep(1)


# =========================
# 💬 SEND WHATSAPP MESSAGE (NORMAL)
# =========================
def sendWhatsAppMessage(query):
    speak("Sending WhatsApp message")
    eel.DisplayMessage("Sending WhatsApp message")

    contact = None
    for key in CONTACTS:
        if key in query:
            contact = CONTACTS[key]
            break

    if not contact:
        speak("Contact not found")
        return

    message = query
    for word in ["send", "message", "to", key]:
        message = message.replace(word, "")
    message = message.strip()

    if message == "":
        speak("Message is empty")
        return

    openWhatsAppChat(contact)

    pyperclip.copy(message)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

    speak("Message sent")
    eel.DisplayMessage("Message sent")


# =========================
# 💬 SEND TEMPLATE MESSAGE (FEATURE B)
# =========================
def sendTemplateMessage(query):
    contact = None
    template = None

    for t in TEMPLATES:
        if t in query:
            template = TEMPLATES[t]
            break

    for c in CONTACTS:
        if c in query:
            contact = CONTACTS[c]
            break

    if not contact or not template:
        return False

    speak(f"Sending message to {contact}")
    eel.DisplayMessage(f"Sending message to {contact}")

    openWhatsAppChat(contact)

    pyperclip.copy(template)
    pyautogui.hotkey("ctrl", "v")
    pyautogui.press("enter")

    speak("Message sent")
    eel.DisplayMessage("Message sent")
    return True


# =========================
# 🧠 WHATSAPP COMMAND ROUTER
# =========================
def whatsappCommand(query):
    # Feature D – quick open
    if "open whatsapp" in query or "whatsapp open" in query:
        for key in CONTACTS:
            if key in query:
                speak(f"Opening WhatsApp chat with {CONTACTS[key]}")
                eel.DisplayMessage(f"Opening {CONTACTS[key]}")
                openWhatsAppChat(CONTACTS[key])
                return True

    # Feature B – template message
    if sendTemplateMessage(query):
        return True

    return False





