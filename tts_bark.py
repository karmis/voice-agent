# import torch
# from bark import generate_audio
# from scipy.io.wavfile import write as write_wav
# import numpy as np
# import os
# os.environ["SUNO_USE_SMALL_MODELS"] = "True"
#
# from bark import preload_models
#
# TTS_OUTPUT_FILE = "output.wav"
#
# def load_bark_tts():
#     print("🧠 Bark предзагрузка моделей...")
#     preload_models()
#     print("🧠 Bark готов к работе!")
#     return True  # Bark не требует загрузки модели заранее
#
#
# def tts(text, model=None, speaker="v2/ru_speaker_1", output_path=TTS_OUTPUT_FILE):
#     print("🔊 Озвучиваю через Bark...")
#     if not text.strip():
#         print("⚠️ Пустой текст для озвучки")
#         return None
#
#     try:
#         # Обрезаем длинный текст (защита от перегрузки модели)
#         max_length = 250
#         if len(text) > max_length:
#             text = text[:max_length] + "..."
#             print(f"✂️ Текст обрезан до {max_length} символов.")
#
#         # Генерируем аудио
#         audio_array = generate_audio(text, history_prompt=speaker)
#         audio_array = (audio_array * 32767).astype(np.int16)
#
#         # Сохраняем как WAV
#         write_wav(output_path, rate=24000, data=audio_array)
#         print(f"✅ Аудио сохранено как {output_path}")
#         return output_path
#     except Exception as e:
#         print(f"❌ Ошибка синтеза речи: {e}")
#         return None