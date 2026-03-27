## Описание

Self-hosted TTS сервер на основе [Coqui AI TTS (форк Idiap)](https://github.com/idiap/coqui-ai-TTS) с моделью XTTS v2.
Поддерживает множество голосов, русский язык и звуковые эффекты (радио, робот, мегафон и др.).

## Требования

- Python 3.10 - 3.11
- NVIDIA GPU с поддержкой CUDA (рекомендуется) или CPU
- ffmpeg (для звуковых эффектов и конвертации аудио)

## Установка

1. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```
   Или через `install_requirements.bat`

2. Установите ffmpeg, если ещё не установлен:
   ```
   winget install ffmpeg
   ```
   Или скачайте вручную: https://ffmpeg.org/download.html
   и добавьте папку `bin` в переменную PATH.

3. При первом запуске модель XTTS v2 скачается автоматически (~1.8GB).

## Запуск

```
python tts_server.py
```
Или через `launch_server.bat`.

Сервер запустится на `http://127.0.0.1:5000/`.

## Настройка билда

Добавьте в `config.txt` проекта:
```
TTS_TOKEN_SILERO mytoken
TTS_URL_SILERO http://127.0.0.1:5000/tts/
TTS_ENABLED
TTS_CACHE
```

## API эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| POST | `/tts/` | Генерация речи |
| GET | `/speakers/` | Список доступных голосов |
| GET | `/status/` | Статус сервера и очереди |

## Голоса

XTTS v2 содержит множество встроенных голосов. Полный список доступен по адресу `http://127.0.0.1:5000/speakers/` после запуска сервера.

Некоторые примеры:
- Claribel Dervla, Daisy Studious, Gracie Wise (женские)
- Badr Odhiambo, Dionisio Schuyler, Viktor Eka (мужские)

## Звуковые эффекты

Передаются через параметр `effect` в POST-запросе:

| Код | Эффект |
|-----|--------|
| 0 | Без эффекта |
| 1 | Радио |
| 2 | Робот |
| 3 | Радио + Робот |
| 4 | Мегафон |
| 5 | Мегафон + Робот |
| 6 | Хайвмайнд |

Для работы эффектов требуется установленный ffmpeg.

## Решение проблем

**Ошибка NumPy:** убедитесь, что установлен `numpy<2` (указан в requirements.txt).

**Ошибка `isin_mps_friendly` / transformers:** нужна версия `transformers>=4.47,<5` (указана в requirements.txt).

**CUDA out of memory:** уменьшите длину текста или используйте CPU.

**Модель не скачивается:** проверьте интернет-соединение, модель весит ~1.8GB.

## Авторство

- Coqui TTS (форк Idiap): https://github.com/idiap/coqui-ai-TTS
- Оригинальный Silero сервер: https://github.com/Vladisvell
