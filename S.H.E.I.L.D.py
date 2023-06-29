import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import openai
import asyncio
import re
import whisper
import boto3
import pydub
from pydub import playback
import speech_recognition as sr
from EdgeGPT import Chatbot, ConversationStyle

# Initialize the OpenAI API
openai.api_key = "[paste your OpenAI API key here]"

# Create a recognizer object and wake word variables
recognizer = sr.Recognizer()
BING_WAKE_WORD = " Sheild emerged"
GPT_WAKE_WORD = "Sheild"

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Sheild')
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet('background-color: #f7f7f7;')
        self.setGeometry(300, 200, 800, 600)

        font = QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)

        self.response_label = QLabel(self)
        self.response_label.setGeometry(QRect(50, 50, 700, 200))
        self.response_label.setText("Hello, I am Sheild. How may I assist you?")
        self.response_label.setAlignment(Qt.AlignTop)
        self.response_label.setFont(font)

        self.input_textbox = QLineEdit(self)
        self.input_textbox.setGeometry(QRect(50, 300, 700, 50))
        self.input_textbox.setFont(font)

        self.send_button = QPushButton('Send', self)
        self.send_button.setGeometry(QRect(650, 370, 100, 50))
        self.send_button.setFont(font)
        self.send_button.clicked.connect(self.send_message)

def get_wake_word(phrase):
    if BING_WAKE_WORD in phrase.lower():
        return BING_WAKE_WORD
    elif GPT_WAKE_WORD in phrase.lower():
        return GPT_WAKE_WORD
    else:
        return None
    
def synthesize_speech(text, output_filename):
    polly = boto3.client('polly', region_name='us-west-2')
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Salli',
        Engine='neural'
    )

    with open(output_filename, 'wb') as f:
        f.write(response['AudioStream'].read())

def play_audio(file):
    sound = pydub.AudioSegment.from_file(file, format="mp3")
    playback.play(sound)

async def main():
    while True:

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print(f"Waiting for wake words 'Sheild emerged' or 'Sheild'...")
            while True:
                audio = recognizer.listen(source)
                try:
                    with open("audio.wav", "wb") as f:
                        f.write(audio.get_wav_data())
                    # Use the preloaded tiny_model
                    model = whisper.load_model("tiny")
                    result = model.transcribe("audio.wav")
                    phrase = result["text"]
                    print(f"You said: {phrase}")

                    wake_word = get_wake_word(phrase)
                    if wake_word is not None:
                        break
                    else:
                        print("Not a wake word. Try again.")
                except Exception as e:
                    print("Error transcribing audio: {0}".format(e))
                    continue

            print("Speak a prompt...")
            synthesize_speech('Hello ,I am Sheild. How may i assist you?', 'response.mp3')
            play_audio('response.mp3')
            audio = recognizer.listen(source)

            try:
                with open("audio_prompt.wav", "wb") as f:
                    f.write(audio.get_wav_data())
                model = whisper.load_model("base")
                result = model.transcribe("audio_prompt.wav")
                user_input = result["text"]
                print(f"You said: {user_input}")
            except Exception as e:
                print("Error transcribing audio: {0}".format(e))
                continue

            if wake_word == BING_WAKE_WORD:
                bot = Chatbot(cookiePath='cookies.json')
                response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.precise)

                for message in response["item"]["messages"]:
                    if message["author"] == "bot":
                        bot_response = message["text"]

                bot_response = re.sub('\[\^\d+\^\]', '', bot_response)

                bot = Chatbot(cookiePath='cookies.json')
                response = await bot.ask(prompt=user_input, conversation_style=ConversationStyle.creative)
                # Select only the bot response from the response dictionary
                for message in response["item"]["messages"]:
                    if message["author"] == "bot":
                        bot_response = message["text"]
                # Remove [^#^] citations in response
                bot_response = re.sub('\[\^\d+\^\]', '', bot_response)

            else:
                # Send prompt to GPT-3.5-turbo API
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content":
                        "You are a helpful assistant."},
                        {"role": "user", "content": user_input},
                    ],
                    temperature=0.5,
                    max_tokens=150,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                    n=1,
                    stop=["\nUser:"],
                )

                bot_response = response["choices"][0]["message"]["content"]
                
        print("Bot's response:", bot_response)
        synthesize_speech(bot_response, 'response.mp3')
        play_audio('response.mp3')
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())
