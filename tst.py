from argparse import ArgumentParser

from speechkit import model_repository, configure_credentials, creds

from config import YA_IAM_TOKEN

# Аутентификация через API-ключ.
configure_credentials(
    yandex_credentials=creds.YandexCredentials(
        api_key=YA_IAM_TOKEN
    )
)


def synthesize(text, export_path):
    model = model_repository.synthesis_model()

    # Задайте настройки синтеза.
    model.voice = 'jane'
    model.role = 'good'

    # Синтез речи и создание аудио с результатом.
    result = model.synthesize(text, raw_format=False)
    result.export(export_path, 'wav')


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--text', type=str, help='text to synthesize', required=True)
    parser.add_argument('--export', type=str, help='export path for synthesized audio', required=False)

    args = parser.parse_args()

    synthesize(args.text, args.export)
