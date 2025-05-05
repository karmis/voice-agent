import openai
from openai import OpenAI

from config import SYSTEM_PROMPT, SAMBANOVA_API_KEY, OPENAI_API_KEY


def generate_reply(user_input):
    # reply = None

    reply = generate_with_nova(user_input)
    if reply is None:
        reply = generate_with_qwen(user_input)

    if reply is None:
        reply = "Я сломался бро, ничего не могу ответить"

    return reply

def generate_with_nova(user_input):
    print("🧠 Генерирую через Nova (OpenRouter)...")
    try:
        client = openai.OpenAI(api_key=SAMBANOVA_API_KEY, base_url="https://api.sambanova.ai/v1", )

        response = client.chat.completions.create(model="DeepSeek-V3-0324",
                                                  messages=[{"role": "system", "content": SYSTEM_PROMPT},
                                                            {"role": "user", "content": user_input}], temperature=0.1,
                                                  top_p=0.1)
        if response and response.choices:
            content = response.choices[0].message.content.strip()
            print("🧠 Nova говорит:", content)
            return content
        else:
            return None
    except Exception as e:
        print(f"❌ Ошибка генерации: {e}")
        return None


def generate_with_qwen(user_input):
    print("🧠 Генерирую через Qwen (OpenRouter)...")
    try:
        client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=OPENAI_API_KEY)
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user_input}]

        completion = client.chat.completions.create(model="qwen/qwen3-235b-a22b", messages=messages, temperature=0.8,
                                                    max_tokens=4096, top_p=0.9)
        if completion and completion.choices:
            content = completion.choices[0].message.content.strip()
            print("🧠 Qwen говорит:", content)
            return content
        else:
            return None

    except Exception as e:
        print(f"❌ Ошибка генерации: {e}")
        return None
