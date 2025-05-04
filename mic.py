import speech_recognition as sr
import time
import winsound
import os

from config import LANGUAGE, WAKE_WORD, MICROPHONE_INDEX, TIMEOUT
from utils import is_wake_word


def get_microphone_device():
    print("🔍 Ищу подходящий микрофон...")
    mics = sr.Microphone.list_microphone_names()
    if MICROPHONE_INDEX is not None and MICROPHONE_INDEX < len(mics):
        selected_name = mics[MICROPHONE_INDEX]
        print(f"🟢 Использую микрофон #{MICROPHONE_INDEX}: {selected_name}")
        return MICROPHONE_INDEX
    for idx, name in enumerate(mics):
        if 'microphone' in name.lower() or 'mic' in name.lower():
            print(f"🟢 Нашел микрофон #{idx}: {name}")
            return idx
    print("⚠️ Микрофон не найден — попробую использовать дефолтный")
    return None


def record_after_wake_word():
    r = sr.Recognizer()
    mic_index = get_microphone_device()
    print("🎙️ Готов к активации по голосу...")

    with sr.Microphone(device_index=mic_index) as source:
        while True:
            try:
                print('🔇 Подстраиваюсь под фон...')
                r.adjust_for_ambient_noise(source, duration=0.5)
                print("💤 Жду команду...")
                audio = r.listen(source, timeout=TIMEOUT, phrase_time_limit=10)
                text = r.recognize_google(audio, language=LANGUAGE).lower()
                print(f"🗣️ Распознано: {text}")

                if is_wake_word(text):
                    print("🟢 Команда активирована!")
                    full_text = text.split(WAKE_WORD, 1)[-1].strip()
                    if not full_text:
                        print("⚠️ Ничего нет после команды")
                        winsound.PlaySound("not_understood.wav", winsound.SND_FILENAME)
                        continue
                    print(f"📝 Полученная команда: {full_text}")
                    return full_text
            except sr.UnknownValueError:
                print("❌ Не могу распознать речь.")
            except sr.RequestError:
                print("🌐 Ошибка связи с Google STT.")
            except Exception as e:
                print(f"⚠️ Ошибка микрофона: {e}")
                continue
