from cleverbotfree import Cleverbot
from googletrans import Translator
from gtts import gTTS
import random
import os
from playsound import playsound
import speech_recognition as sr
import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
import threading

translator = Translator()
rec = sr.Recognizer()
stopgif = True


class ImageLabel(tk.Label):
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []
        self.runtimes = 0

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            if not stopgif:
                self.loc += 1
            else:
                self.loc = 0
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def record():
    with sr.Microphone() as source:
        voice_rec = ''
        audio = rec.listen(source, 5, 5)
        try:
            voice_rec = rec.recognize_google(audio, language='tr-TR')
        except sr.UnknownValueError:
            speak('anlayamadım')
        except sr.RequestError:
            speak('sistem hata aldı')
        return voice_rec


def speak(text):
    global stopgif
    if text:
        stopgif = False
        tts = gTTS(text, lang='tr')
        rand = random.randint(1, 10000)
        file = 'audio' + str(rand) + '.mp3'
        tts.save(file)
        playsound(file)
        os.remove(file)
        stopgif = True
    else:
        print("Boş metin, seslendirilecek bir şey yok.")
def translate_text(who, text, lang):
    text_tranlated = translator.translate(text, dest=lang)
    print(who, '(', lang, '):', text_tranlated.text)
    return text_tranlated.text


@Cleverbot.connect
def chatbot(bot, user_prompt, bot_prompt):
    while True:
        user_input = record()
        print(user_prompt, user_input)
        user_input_en = translate_text(user_prompt, user_input, 'en')
        if user_input.lower() == "kapat":
            break
        reply = bot.single_exchange(user_input_en)
        print(bot_prompt, reply)
        bot_reply_tr = translate_text(bot_prompt, reply, 'tr')
        speak(bot_reply_tr)
    bot.close()


def display_gif():
    print(' Robot Cemile hazırlanıyor ve karşınızda.')
    root = tk.Tk()

    lbl = ImageLabel(root)
    lbl.pack()
    lbl.load('run-mailout.gif')
    root.mainloop()


def run_bot():
    print('Robot Cemile hazır lütfen konuşmaya başlayın.')
    chatbot("Siz:", "Robot Cemile:")


t1 = threading.Thread(target=display_gif)
t1.start()
t2 = threading.Thread(target=run_bot)
t2.start()