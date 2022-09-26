from gtts import gTTS
from playsound import playsound
import pathlib


def speak(mytext, language):
    my_path = pathlib.Path(__file__).parent.resolve() / "assets"
    tts = gTTS(text=mytext, lang=language)
    new_path = str(my_path) + "\\temp_speak.mp3"
    tts.save(new_path)
    playsound(new_path)
