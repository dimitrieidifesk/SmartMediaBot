import moviepy.editor
from pathlib import Path

async def get_mp3_from_mp4(filename = 'test.mp4'):
    """Получение звуковой дорожки из mp4 файла"""
    video_file = Path('./input/' + filename)
    video = moviepy.editor.VideoFileClip(f'{video_file}')
    audio = video.audio
    new_file = f'./output/{video_file.stem}.mp3'
    audio.write_audiofile(new_file)