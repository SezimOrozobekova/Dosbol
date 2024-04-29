import os
import tempfile
import pygame
import speech_recognition as sr
from gtts import gTTS
from g4f.client import Client


class ChatSession:
    def __init__(self):
        self.client = Client()
        self.messages = []

    def send_message(self, content):
        self.messages.append({"role": "user", "content": content})
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo", messages=self.messages
        )
        bot_message = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": bot_message})

        # Convert the response to audio and play it
        tts = gTTS(bot_message, lang='ru')
        temp_path = tempfile.gettempdir()
        temp_file = os.path.join(temp_path, "response.mp3")
        tts.save(temp_file)
        pygame.mixer.init()
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()

        # Wait for audio playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

        # Clean up
        pygame.mixer.quit()
        os.remove(temp_file)

        return bot_message


def recognize_speech_from_microphone(chat_session):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Скажите что-нибудь или скажите 'пока', чтобы завершить разговор...")

        while True:
            audio_data = recognizer.listen(source)
            try:
                print("Слушаю...")
                text = recognizer.recognize_google(audio_data, language='ru-RU')
                print(f"Вы сказали: {text}")

                # Check if the user wants to exit
                if text.lower() == 'пока':
                    print("Разговор завершен.")
                    break

                # Send the text to the chatbot and get the response
                response = chat_session.send_message(text)
                print("Dosbol:", response)

            except sr.UnknownValueError:
                print("Не удалось распознать речь.")
            except sr.RequestError as e:
                print(f"Ошибка запроса к службе распознавания: {e}")


# Initialize the chat session
session = ChatSession()

# Start recognizing speech from the microphone
recognize_speech_from_microphone(session)
