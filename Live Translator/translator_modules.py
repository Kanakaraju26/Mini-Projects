import speech_recognition as sr
import time
import googletrans as gt
from gtts import gTTS
import pygame

output_file = "./output_audio.mp3"


def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("I'm Listening... ")
        audio = recognizer.listen(source)
        
    try:
        text = recognizer.recognize_google(audio)
        print("You said: ", text)
        return text
    
    except sr.UnknownValueError:
        print("Can't understand, What you are saying...")
    except IOError as e:
        print(f"An IOError occurred: {e}")
    except KeyboardInterrupt:
        print("Listener Stopped.")
    except sr.RequestError as e:
        print(f"Could Not Request Results From Google Speech Recognition service; {e} ")


def voice_conversion(text, targeted_lang):
    if text is None:
        return
    translator = gt.Translator()
    translation = translator.translate(text, targeted_lang)
    print("Translation: ", translation.text)
    return translation.text


def text_to_voice(translated, targeted_lang):
    if translated is None:
        return
    tts = gTTS(text=translated, lang=targeted_lang, slow=False)
    tts.save(output_file) 


def play_sound(file_path):
    pygame.init()
    pygame.mixer.init()

    try:
        sound = pygame.mixer.Sound(file_path)
        sound.play()
        time.sleep(sound.get_length())  # Wait for the sound to finish playing
        
    except OSError as e:
        print(f"An IO Error Occurred: {e}")
    except pygame.error as e:
        print(f"Error playing sound: {e}")
    finally:
        pygame.mixer.quit()
