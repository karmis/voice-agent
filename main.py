import winsound
import os
from config import *
from llm import generate_with_groq, generate_with_yandex
from mic import record_after_wake_word
from tts import load_silero_tts, tts
def main():
    silero_model = load_silero_tts()
    print("🤖 Голосовой агент запущен!")

    while True:
        user_phrase = record_after_wake_word()
        if not user_phrase:
            continue
        print(f"🗣️ Вы сказали: {user_phrase}")

        if user_phrase.lower() == "давай с начала":
            print("🔄 Новый чат открыт.")
            winsound.PlaySound("new_chat.wav", winsound.SND_FILENAME)
            continue

        if LLM_PROVIDER == "groq":
            reply = generate_with_groq(user_phrase, GROQ_API_KEY)
        elif LLM_PROVIDER == "yandex":
            reply = generate_with_yandex(user_phrase)
        else:
            reply = NOT_UNDERSTOOD

        print("🧠 Qwen говорит:", reply)

        tts_file = tts(reply, silero_model, SELECTED_SPEAKER)
        if tts_file and os.path.exists(tts_file):
            print("🎧 Воспроизводим...")
            winsound.PlaySound(tts_file, winsound.SND_FILENAME)
        else:
            print("🔇 Нет текста для озвучки")
            winsound.PlaySound("no_response.wav", winsound.SND_FILENAME)

if __name__ == '__main__':
    main()