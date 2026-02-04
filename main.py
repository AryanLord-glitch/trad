import eel
import threading

from engine.features import playAssistantSound
from engine.hotword import hotword_detect


def start_hotword():
    """Run hotword engine in background thread"""
    hotword_detect()


def start():
    eel.init("www")

    # 🔊 Startup sound
    playAssistantSound()

    # 🔥 Start hotword listener in background
    hotword_thread = threading.Thread(target=start_hotword, daemon=True)
    hotword_thread.start()

    # 🌐 Start UI
    eel.start(
        "index.html",

    host="localhost",
        port=8000,
        block=True
    )


if __name__ == "__main__":
    start()

