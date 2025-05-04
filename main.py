import winsound
import os
from config import *
from llm import generate_reply
from mic import record_after_wake_word
from tts_yandex import tts


def main():
    # silero_model = load_bark_tts()
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

        reply = generate_reply(user_phrase)

        tts_file = tts(reply)
        if tts_file and os.path.exists(tts_file):
            print("🎧 Воспроизводим...")
            winsound.PlaySound(tts_file, winsound.SND_FILENAME)
        else:
            print("🔇 Нет текста для озвучки")
            winsound.PlaySound("no_response.wav", winsound.SND_FILENAME)

if __name__ == '__main__':
    main()