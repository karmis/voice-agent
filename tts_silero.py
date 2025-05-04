# import torch
# import numpy as np
# from scipy.io import wavfile
#
# def load_silero_tts():
#     print("🧠 Загружаю Silero TTS...")
#     model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts', language='ru', speaker='v3_1_ru')
#     print("🟢 Модель загружена!")
#     return model
#
# def tts(text, silero_model, speaker='eugene', output_path="output.wav"):
#     print("🔊 Озвучиваю через Silero...")
#     if not text.strip():
#         print("⚠️ Пустой текст для озвучки")
#         return None
#
#     try:
#         max_length = 998
#         if len(text) > max_length:
#             text = text[:max_length] + "..."
#             print(f"✂️ Текст обрезан до {max_length} символов.")
#
#         audio = silero_model.apply_tts(
#             text=text + '.', sample_rate=48000,
#             speaker=speaker, put_accent=True, put_yo=True
#         )
#         wavfile.write(output_path, 48000, (audio.numpy().flatten() * 32767).astype(np.int16))
#         print(f"✅ Аудио сохранено как {output_path}")
#         return output_path
#     except Exception as e:
#         print(f"❌ Ошибка синтеза речи: {e}")
#         return None