import os
import openai
from gtts import gTTS
from pygame import mixer
import tempfile

def __talk(sentence,lang):
    with tempfile.NamedTemporaryFile(delete=True) as f:
        tts=gTTS(text=sentence, lang=lang)
        tts.save(f'{f.name}.mp3')
        mixer.init()
        mixer.music.load(f'{f.name}.mp3')
        mixer.music.play(loops=0)

def chatgpt(text:str)->str:
    if os.getenv("OPENAI_API_KEY")==None:
        return None
    openai.api_key=os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "system",
                "content": "使用繁體中文"},
                    {"role": "user", "content": text}
                ]
    )
    print(completion["choices"][0]["message"]["content"])
    __talk(completion["choices"][0]["message"]["content"], 'zh-TW')
    return completion["choices"][0]["message"]["content"]

"""
pip install openai

from ChatGPT import chatgpt

傳入問題，會回傳答案
chatgpt()
"""