## Описание
Это self-hosted версия TTS сервера на основе Coqui AI TTS (XTTS v2).

## Требования

Python 3.10 - 3.11 (Coqui TTS требует Python 3.10+)

- ffmpeg (Устанавливать вручную)
- TTS (Coqui AI TTS)
- torch
- soundfile
- pydub
- flask

Подробнее в `requirements.txt`

## Установка

1. Воспользуйтесь в командной строке, открытой в папке tools\ttsServer:
   ```
   pip install -r requirements.txt
   ```
   Или воспользуйтесь файлом `install_requirements.bat`

2. Если не установлен ffmpeg, установите его: https://ffmpeg.org/download.html
   Или через: `winget install ffmpeg`

3. При первом запуске модель XTTS v2 будет скачана автоматически (~1.5GB)

## Как пользоваться

1. Включите в конфигурации билда в `config.txt`:
   ```
   TTS_TOKEN_SILERO mytoken
   TTS_URL_SILERO http://127.0.0.1:5000/tts/
   TTS_ENABLED
   TTS_CACHE
   ```

2. Запустите сервер:
   ```
   python tts_server.py
   ```
   Или через `launch_server.bat`

3. Сервер выведет URL для подключения (по умолчанию `http://127.0.0.1:5000/tts/`)

## Голоса (Speakers)

XTTS v2 содержит множество встроенных голосов. Для просмотра доступных голосов:
- Откройте в браузере: `http://127.0.0.1:5000/speakers/`
- Или при запуске сервера в консоли выведется список

Примеры голосов в XTTS v2:
- Claribel Dervla (женский)
- Daisy Studious (женский)
- Gracie Wise (женский)
- Tammie Ema (женский)
- Alison Dietlinde (женский)
- Ana Florence (женский)
- Annmarie Nele (женский)
- Badr Odhiambo (мужской)
- Dionisio Schuyler (мужской)
- Royston Min (мужской)
- Viktor Eka (мужской)
- И другие...

## GPU Ускорение

Если у вас есть NVIDIA GPU с CUDA, сервер автоматически использует GPU для ускорения.
Для CPU-only работы модель также работает, но медленнее.

## Примечания

- Первый запрос может быть медленнее из-за "прогрева" модели
- Производительность зависит от вашего оборудования
- На CPU ожидайте задержки 1-3 секунды, на GPU 0.3-1 секунда

## Решение возможных проблем

```
Ругается на Numpy:
pip install "numpy<2"

Не устанавливается TTS:
Используйте Python 3.10 или 3.11

Ошибка CUDA out of memory:
Используйте CPU режим или уменьшите длину текста

Модель не скачивается:
Проверьте интернет-соединение, модель ~1.5GB
```

## Установка FFmpeg

1. Скачайте FFmpeg: https://ffmpeg.org/download.html
2. Распакуйте в папку, например `C:\ffmpeg`
3. Добавьте `C:\ffmpeg\bin` в переменную PATH
4. Проверьте: `ffmpeg -version`

## Авторство

- Coqui TTS: https://github.com/idiap/coqui-ai-TTS
- Оригинальный код Silero сервера: https://github.com/Vladisvell
