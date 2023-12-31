import os
import openai

def chatgpt(text:str)->str:
    openai.api_key=os.getenv("OPENAI_API_KEY")
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        messages=[{"role": "system",
                "content": "Only Use Traditional Chinese"},
                    {"role": "user", "content": input()}
                ]
    )
    print(completion["choices"][0]["message"]["content"])
    return completion["choices"][0]["message"]["content"]

"""
pip install openai

from ChatGPT import chatgpt

傳入問題，會回傳答案
chatgpt()
"""