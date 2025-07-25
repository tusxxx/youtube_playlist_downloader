#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube Playlist Downloader
Программа для скачивания публичных плейлистов с YouTube в формате MP3
"""

import os
import sys
import argparse
import logging
from pathlib import Path
import yt_dlp
from yt_dlp.utils import DownloadError


class YouTubePlaylistDownloader:
    """Класс для скачивания плейлистов YouTube в формате MP3"""
    
    def __init__(self, output_dir="downloads"):
        """
        Инициализация загрузчика
        
        Args:
            output_dir (str): Директория для сохранения файлов
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Настройка логирования
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('download.log', encoding='utf-8'),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def get_ydl_opts(self):
        """Получить опции для yt-dlp"""
        return {
            'format': 'bestaudio/best',  # Скачиваем лучшее аудио
            'extractaudio': True,
            'audioformat': 'mp3',
            'audioquality': '192',  # Качество MP3
            'outtmpl': str(self.output_dir / '%(playlist_title)s/%(title)s.%(ext)s'),
            'ignoreerrors': True,  # Продолжать при ошибках
            'no_warnings': False,
            'writeinfojson': False,  # Не сохранять JSON метаданные
            'writethumbnail': False,  # Не сохранять миниатюры
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    
    def download_playlist(self, playlist_url):
        """
        Скачать плейлист с YouTube
        
        Args:
            playlist_url (str): URL плейлиста YouTube
            
        Returns:
            bool: True если скачивание успешно, False иначе
        """
        try:
            self.logger.info(f"Начинаю скачивание плейлиста: {playlist_url}")
            
            with yt_dlp.YoutubeDL(self.get_ydl_opts()) as ydl:
                # Получаем информацию о плейлисте
                playlist_info = ydl.extract_info(playlist_url, download=False)
                playlist_title = playlist_info.get('title', 'Unknown Playlist')
                video_count = len(playlist_info.get('entries', []))
                
                self.logger.info(f"Плейлист: {playlist_title}")
                self.logger.info(f"Количество видео: {video_count}")
                
                # Скачиваем плейлист
                ydl.download([playlist_url])
                
                self.logger.info("Скачивание завершено успешно!")
                return True
                
        except DownloadError as e:
            self.logger.error(f"Ошибка скачивания: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка: {e}")
            return False
    
    def download_single_video(self, video_url):
        """
        Скачать одно видео с YouTube
        
        Args:
            video_url (str): URL видео YouTube
            
        Returns:
            bool: True если скачивание успешно, False иначе
        """
        try:
            self.logger.info(f"Начинаю скачивание видео: {video_url}")
            
            opts = self.get_ydl_opts()
            opts['outtmpl'] = str(self.output_dir / '%(title)s.%(ext)s')
            
            with yt_dlp.YoutubeDL(opts) as ydl:
                # Получаем информацию о видео
                video_info = ydl.extract_info(video_url, download=False)
                video_title = video_info.get('title', 'Unknown Video')
                
                self.logger.info(f"Видео: {video_title}")
                
                # Скачиваем видео
                ydl.download([video_url])
                
                self.logger.info("Скачивание завершено успешно!")
                return True
                
        except DownloadError as e:
            self.logger.error(f"Ошибка скачивания: {e}")
            return False
        except Exception as e:
            self.logger.error(f"Неожиданная ошибка: {e}")
            return False


def main():
    """Главная функция программы"""
    parser = argparse.ArgumentParser(
        description='Скачивание плейлистов и видео с YouTube в формате MP3',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python youtube_playlist_downloader.py "https://www.youtube.com/playlist?list=PLrAXtmRdbe-1qVs"
  python youtube_playlist_downloader.py "https://youtu.be/dQw4w9WgXcQ" -o "my_music"
  python youtube_playlist_downloader.py -u "https://www.youtube.com/playlist?list=PLrAXtmRdbe-1qVs" -o "downloads"
        """
    )
    
    parser.add_argument(
        'url',
        nargs='?',
        help='URL плейлиста или видео YouTube'
    )
    
    parser.add_argument(
        '-u', '--url',
        dest='url_arg',
        help='URL плейлиста или видео YouTube (альтернативный способ)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='downloads',
        help='Директория для сохранения файлов (по умолчанию: downloads)'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Подробный вывод'
    )
    
    args = parser.parse_args()
    
    # Определяем URL
    url = args.url or args.url_arg
    
    if not url:
        print("Ошибка: Необходимо указать URL плейлиста или видео!")
        print("Используйте -h для просмотра справки.")
        sys.exit(1)
    
    # Настройка уровня логирования
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Создаем загрузчик
    downloader = YouTubePlaylistDownloader(args.output)
    
    print(f"🎵 YouTube Playlist Downloader")
    print(f"📁 Папка сохранения: {args.output}")
    print(f"🔗 URL: {url}")
    print("-" * 50)
    
    # Определяем тип URL и скачиваем
    if 'playlist' in url:
        success = downloader.download_playlist(url)
    else:
        success = downloader.download_single_video(url)
    
    if success:
        print("\n✅ Скачивание завершено успешно!")
        print(f"📁 Файлы сохранены в: {os.path.abspath(args.output)}")
    else:
        print("\n❌ Произошла ошибка при скачивании!")
        print("📋 Проверьте файл download.log для подробностей.")
        sys.exit(1)


if __name__ == "__main__":
    main() 