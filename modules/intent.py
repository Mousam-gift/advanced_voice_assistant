def detect_intent(command):
    if any(word in command for word in["weather", "temperature", "forecast"]):
        return "weather"
    elif "hello" in command or "hi" in command:
        return "greeting"
    elif "send email" in command or "email" in command:
        return "email"
    elif "reminder" in command:
        return "reminder"
    elif "close" in command or "quit" in command:
        return "close_app"
    elif "open" in command:
        return "open_app"
    elif "time" in command:
        return "time"
    elif "google" in command or "search" in command:
        return "google_search"
    elif "exit" in command or "stop" in command or "shutdown" in command:
        return "exit"
    elif any(word in command for word in ["resume", "pause", "next", "previous", "back", "mute", "unmute", "volume up", "volume down", "louder"]):
        return "music_control"
    elif "play" in command:
        return "play_music"
    elif "thanks" in command or "thank " in command:
        return "thank_you"
    else:
        return "unknown"