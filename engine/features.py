import os
import eel
import pywhatkit
import time
import pyautogui
import pyperclip
import webbrowser
import urllib.parse



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
# 📝 WHATSAPP TEMPLATES
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
            speak(f"Opening {app}")
            eel.DisplayMessage(f"Opening {app}")
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
# 🎧 PLAY MUSIC ON SPOTIFY (WEB SAFE)
# =========================
def playSpotify(query):
    query = query.replace("play", "")
    query = query.replace("on spotify", "")
    query = query.replace("spotify", "")
    song = query.strip()

    if song == "":
        speak("Opening Spotify")
        eel.DisplayMessage("Opening Spotify")
        webbrowser.open("https://open.spotify.com")
        return True

    url = f"https://open.spotify.com/search/{song.replace(' ', '%20')}"
    speak(f"Playing {song} on Spotify")
    eel.DisplayMessage(f"Playing {song} on Spotify")
    webbrowser.open(url)
    return True


# =========================
# 🧭 OPEN WHATSAPP CHAT
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
# 💬 SEND WHATSAPP MESSAGE
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
# 💬 TEMPLATE MESSAGE
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
# 🧠 WHATSAPP ROUTER
# =========================
def whatsappCommand(query):
    if "open whatsapp" in query or "whatsapp open" in query:
        for key in CONTACTS:
            if key in query:
                speak(f"Opening WhatsApp chat with {CONTACTS[key]}")
                eel.DisplayMessage(f"Opening {CONTACTS[key]}")
                openWhatsAppChat(CONTACTS[key])
                return True

    if sendTemplateMessage(query):
        return True

    return False


# =========================
# 🌦️ WEATHER UPDATE
# =========================
def checkWeather(query):
    speak("Fetching weather information")
    eel.DisplayMessage("Fetching weather...")

    location = "your location"

    if "in" in query:
        location = query.split("in")[-1].strip()

    url = "https://www.google.com/search?q=" + urllib.parse.quote(
        f"weather in {location}"
    )

    webbrowser.open(url)
    return True


# =========================
# 🔊 VOLUME CONTROL
# =========================
def controlVolume(query):
    if "mute" in query:
        pyautogui.press("volumemute")
        speak("Volume muted")
        return True

    if "increase" in query or "up" in query:
        for _ in range(5):
            pyautogui.press("volumeup")
        speak("Volume increased")
        return True

    if "decrease" in query or "down" in query:
        for _ in range(5):
            pyautogui.press("volumedown")
        speak("Volume decreased")
        return True

    if "max" in query:
        for _ in range(15):
            pyautogui.press("volumeup")
        speak("Volume set to maximum")
        return True

    return False
# =========================
# 💡 BRIGHTNESS CONTROL (STABLE)
# =========================
def controlBrightness(query):
    try:
        if "increase brightness" in query:
            speak("Increasing brightness")
            eel.DisplayMessage("Increasing brightness")

            os.system(
                'powershell "(Get-WmiObject -Namespace root/WMI '
                '-Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 80)"'
            )
            return True

        if "decrease brightness" in query:
            speak("Decreasing brightness")
            eel.DisplayMessage("Decreasing brightness")

            os.system(
                'powershell "(Get-WmiObject -Namespace root/WMI '
                '-Class WmiMonitorBrightnessMethods).WmiSetBrightness(1, 30)"'
            )
            return True

    except Exception as e:
        print("Brightness Error:", e)
        speak("Brightness control failed")

    return False

