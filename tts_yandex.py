import torch
import numpy as np
from scipy.io import wavfile
from speechkit import configure_credentials, model_repository
from speechkit.common.utils import creds

from config import YA_IAM_TOKEN


def load_silero_tts():
    print("🧠 Загружаю Silero TTS...")
    model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts', language='ru', speaker='v3_1_ru')
    print("🟢 Модель загружена!")
    return model

def tts(text, output_path="output.wav"):
    print("🔊 Озвучиваю через Yandex...")
    if not text.strip():
        print("⚠️ Пустой текст для озвучки")
        return None

    try:
        max_length = 510
        if len(text) > max_length:
            text = text[:max_length] + "..."
            print(f"✂️ Текст обрезан до {max_length} символов.")

        configure_credentials(
            yandex_credentials=creds.YandexCredentials(
                api_key=YA_IAM_TOKEN
            )
        )
        model = model_repository.synthesis_model()

        # Задайте настройки синтеза.
        model.voice = 'anton'
        model.role = 'good'
        model.unsafe_mode = True
        model.speed = 1.25

        # Синтез речи и создание аудио с результатом.
        result = model.synthesize(text, raw_format=False)

        result.export(output_path, 'wav')
        print(f"✅ Аудио сохранено как {output_path}")
        return output_path
    except Exception as e:
        print(f"❌ Ошибка синтеза речи: {e}")
        return None