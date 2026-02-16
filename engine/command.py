import eel
import speech_recognition as sr
import time


# =========================
# 🔊 SPEAK
# =========================
def speak(text):
    import pyttsx3
    engine = pyttsx3.init("sapi5")
    engine.say(text)
    engine.runAndWait()


# =========================
# 🎙️ TAKE VOICE COMMAND
# =========================
def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        eel.DisplayMessage("Listening...")
        audio = r.listen(source)

    try:
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        eel.DisplayMessage(query)
        return query.lower()

    except Exception:
        eel.DisplayMessage("Say that again please...")
        return ""


# =========================
# 🧠 CORE COMMAND BRAIN
# =========================
def processCommand(query):
    from engine.features import (
        openCommand,
        playCommand,
        playSpotify,
        sendWhatsAppMessage,
        whatsappCommand,
        checkWeather,
        controlVolume,
        controlBrightness
    )

    reply = "Command not supported yet"

    # 🎧 Spotify
    if "spotify" in query:
        playSpotify(query)
        reply = "Playing on Spotify"

    # 🌦️ Weather
    elif "weather" in query:
        checkWeather(query)
        reply = "Showing weather"

    # 🔊 Volume
    elif "volume" in query:
        if controlVolume(query):
            reply = "Volume updated"

    # 💡 Brightness
    elif "brightness" in query:
        if controlBrightness(query):
            reply = "Brightness updated"

    # 💬 WhatsApp
    elif "whatsapp" in query or "message" in query or "send" in query:
        if not whatsappCommand(query):
            sendWhatsAppMessage(query)
        reply = "WhatsApp message processed"

    # 🪟 Open apps
    elif "open" in query:
        openCommand(query)
        reply = "Opening application"

    # ▶️ YouTube
    elif "play" in query:
        playCommand(query)
        reply = "Playing on YouTube"

    speak(reply)
    return reply


# =========================
# 🎤 VOICE ENTRY
# =========================
@eel.expose
def allCommands():
    query = takecommand()

    if query == "":
        eel.ShowHood()
        return

    reply = processCommand(query)
    time.sleep(1)
    eel.ShowHood()
    return reply


# =========================
# ⌨️ TEXT ENTRY
# =========================
@eel.expose
def textCommand(query):
    query = query.lower()
    reply = processCommand(query)
    return reply
