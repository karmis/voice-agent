import os
import torch
import numpy as np
from scipy.io import wavfile
from speechkit import configure_credentials, model_repository
from speechkit.common.utils import creds

from config import YA_IAM_TOKEN

# ================================
# Конфигурация
# ================================

TTS_OUTPUT_FILE = "output.wav"
FALLBACK_AUDIO = "not_understood.wav"  # можно добавить предупреждение

# Настройки Silero
SILERO_LANGUAGE = 'ru'
SILERO_MODEL_ID = 'v3_1_ru'
SILERO_SPEAKER = 'baya'  # можно использовать 'eugene', 'kseniya' и др.
MAX_TEXT_LENGTH = 510

# ================================
# 1. Загрузка Silero модели
# ================================

_silero_model = None

def load_silero_tts():
    global _silero_model
    print("🧠 Загружаю Silero TTS...")
    try:
        _silero_model, _ = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language=SILERO_LANGUAGE,
            speaker=SILERO_MODEL_ID
        )
        print("🟢 Silero модель загружена!")
        return _silero_model
    except Exception as e:
        print(f"❌ Ошибка загрузки Silero: {e}")
        return None


# ================================
# 2. Yandex TTS
# ================================

def tts_yandex(text, output_path=TTS_OUTPUT_FILE):
    print("🔊 Озвучиваю через Yandex...")

    if not text.strip():
        print("⚠️ Пустой текст для озвучки")
        return None

    try:
        # Обрезаем длинный текст
        if len(text) > MAX_TEXT_LENGTH:
            text = text[:MAX_TEXT_LENGTH] + "..."

        # Настройки Yandex
        configure_credentials(
            yandex_credentials=creds.YandexCredentials(api_key=YA_IAM_TOKEN)
        )

        model = model_repository.synthesis_model()
        model.voice = 'anton'
        model.role = 'good'
        model.unsafe_mode = True
        model.speed = 1.25

        result = model.synthesize(text, raw_format=False)
        result.export(output_path, 'wav')
        print(f"✅ Аудио сохранено как {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Ошибка Yandex TTS: {e}")
        return None


# ================================
# 3. Silero Fallback
# ================================

def tts_silero(text, output_path=TTS_OUTPUT_FILE, speaker=SILERO_SPEAKER):
    print("🔊 Озвучиваю через Silero (fallback)...")

    global _silero_model
    if _silero_model is None:
        print("⚠️ Silero модель не загружена")
        return None

    if not text.strip():
        print("⚠️ Пустой текст для озвучки")
        return None

    try:
        if len(text) > MAX_TEXT_LENGTH:
            text = text[:MAX_TEXT_LENGTH] + "..."

        audio = _silero_model.apply_tts(
            text=text + '.',
            sample_rate=48000,
            speaker=speaker,
            put_accent=True,
            put_yo=True
        )

        wavfile.write(output_path, 48000, (audio.numpy().flatten() * 32767).astype(np.int16))
        print(f"✅ Аудио сохранено как {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Ошибка Silero: {e}")
        return None


# ================================
# 4. Unified TTS API
# ================================

def tts(text, output_path=TTS_OUTPUT_FILE, speaker=SILERO_SPEAKER):
    """
    Основной метод TTS: сначала пробует Yandex, потом падает на Silero
    :param text: текст для озвучки
    :param output_path: путь к выходному файлу
    :param speaker: голос для Silero
    :return: путь к аудиофайлу или None
    """

    # Попробуем Yandex
    result = tts_yandex(text, output_path)

    if result and os.path.exists(result):
        return result

    # Если Yandex не сработал — попробуем Silero
    print("🔁 Переключаюсь на Silero (fallback)")
    result = tts_silero(text, output_path, speaker)

    if result and os.path.exists(result):
        return result

    # Если ничего не сработало — воспроизводим fallback
    if os.path.exists(FALLBACK_AUDIO):
        print("🔇 Использую запасное сообщение.")
        return FALLBACK_AUDIO

    print("❌ Не удалось озвучить текст ни одним из способов.")
    return None