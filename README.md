# YouTube Playlist Downloader

🎵 Программа для скачивания публичных плейлистов и видео с YouTube в формате MP3.

## Особенности

- 📋 Скачивание целых плейлистов или отдельных видео
- 🎵 Автоматическое извлечение аудио в формате MP3 (192 kbps)
- 📁 Организация файлов по папкам плейлистов
- 📝 Подробное логирование процесса
- 🔄 Продолжение работы при ошибках отдельных видео
- 🌐 Поддержка различных форматов YouTube URL

## Требования

- Python 3.7 или выше
- FFmpeg (для конвертации аудио)

## Установка

### 1. Установка FFmpeg

#### Windows:
1. Скачайте FFmpeg с [официального сайта](https://ffmpeg.org/download.html)
2. Распакуйте архив
3. Добавьте путь к `ffmpeg.exe` в переменную PATH

#### macOS:
```bash
brew install ffmpeg
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install ffmpeg
```

### 2. Установка Python зависимостей

```bash
pip install -r requirements.txt
```

или установить вручную:

```bash
pip install yt-dlp
```

## Использование

### Базовое использование (плейлист должен быть публичным)

```bash
# Скачать плейлист
python youtube_playlist_downloader.py "https://www.youtube.com/playlist?list=PLrAXtmRdbe-1qVs"

# Скачать одно видео
python youtube_playlist_downloader.py "https://youtu.be/dQw4w9WgXcQ"
```

### Дополнительные опции

```bash
# Указать папку для сохранения
python youtube_playlist_downloader.py -o "my_music" "URL_PLAYLIST"

# Подробный вывод
python youtube_playlist_downloader.py -v "URL_PLAYLIST"

# Альтернативный способ указания URL
python youtube_playlist_downloader.py -u "URL_PLAYLIST" -o "downloads"
```

### Примеры

```bash
# Скачать плейлист в папку "downloads" (по умолчанию)
python youtube_playlist_downloader.py "https://www.youtube.com/playlist?list=PLrAXtmRdnbE_SzHe4Z5qU"

# Скачать плейлист в папку "Classical Music"
python youtube_playlist_downloader.py -o "Classical Music" "https://www.youtube.com/playlist?list=PLrAXtmRdnbE_SzHe4Z5qU"

# Скачать одно видео с подробным выводом
python youtube_playlist_downloader.py -v "https://youtu.be/dQw4w9WgXcQ"
```

## Структура выходных файлов

```
downloads/
├── Название Плейлиста/
│   ├── Название Трека 1.mp3
│   ├── Название Трека 2.mp3
│   └── ...
└── download.log
```

Для отдельных видео файлы сохраняются прямо в указанную папку.

## Параметры командной строки

| Параметр | Краткая форма | Описание |
|----------|---------------|----------|
| `url` | - | URL плейлиста или видео (позиционный аргумент) |
| `--url` | `-u` | URL плейлиста или видео (альтернативный способ) |
| `--output` | `-o` | Папка для сохранения файлов (по умолчанию: "downloads") |
| `--verbose` | `-v` | Подробный вывод |
| `--help` | `-h` | Показать справку |

## Логирование

Программа ведет подробный лог в файле `download.log`, который содержит:
- Информацию о скачиваемых плейлистах/видео
- Ошибки и предупреждения
- Временные метки всех операций

## Поддерживаемые форматы URL

- Плейлисты: `https://www.youtube.com/playlist?list=...`
- Видео: `https://www.youtube.com/watch?v=...`
- Короткие ссылки: `https://youtu.be/...`
- Ссылки с временными метками и дополнительными параметрами

## Решение проблем

### Ошибка "FFmpeg not found"
Убедитесь, что FFmpeg установлен и доступен из командной строки:
```bash
ffmpeg -version
```

### Ошибки скачивания отдельных видео
Программа автоматически пропускает недоступные или приватные видео и продолжает скачивание остальных.

### Проблемы с правами доступа
Убедитесь, что у вас есть права на запись в указанную папку.

## Лицензия

Эта программа предназначена только для скачивания контента, который разрешен к скачиванию правообладателями. Пользователь несет полную ответственность за соблюдение авторских прав и условий использования YouTube.

## Технические детали

- **Библиотека**: yt-dlp (современная альтернатива youtube-dl)
- **Формат аудио**: MP3, 192 kbps
- **Кодировка**: UTF-8
- **Логирование**: В файл и консоль
- **Обработка ошибок**: Graceful handling с продолжением работы 