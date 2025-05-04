import requests
from openai import OpenAI

from config import SYSTEM_PROMPT, NOT_UNDERSTOOD


def generate_with_groq(prompt, GROQ_API_KEY):
    print("🧠 Генерирую через Groq...")
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "user", "content": prompt}],
        "model": "llama3-70b-8192",
        "temperature": 0.7,
        "max_tokens": 256
    }
    try:
        response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"❌ Ошибка Groq: {e}")
        return NOT_UNDERSTOOD

def generate_with_yandex(user_input):
    print("🧠 Генерирую через Qwen (OpenRouter)...")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="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",
    )
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    try:
        completion = client.chat.completions.create(
            model="qwen/qwen3-235b-a22b",
            messages=messages,
            temperature=0.8,
            max_tokens=4096,
            top_p=0.9
        )
        if completion and completion.choices:
            content = completion.choices[0].message.content.strip()
            print("🧠 Qwen говорит:", content)
            return content
        else:
            return 'иди нахуй. не до тебя сейчас'
    except Exception as e:
        print(f"❌ Ошибка генерации: {e}")
        return NOT_UNDERSTOOD