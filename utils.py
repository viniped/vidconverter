import os
import subprocess
from pathlib import Path

video_extensions = [
    '.mp4', '.ts', '.mpg', '.mpeg', '.avi', '.mkv', '.flv', '.3gp',
    '.rmvb', '.webm', '.vob', '.ogv', '.rrc', '.gifv', '.mng',
    '.mov', '.qt', '.wmv', '.yuv', '.rm', '.asf', '.amv', '.m4p',
    '.m4v', '.mp2', '.mpe', '.mpv', '.m4v', '.svi', '.3g2',
    '.mxf', '.roq', '.nsv', '.f4v', '.f4p', '.f4a', '.f4b'
]

def has_duration(file_path):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', str(file_path)], capture_output=True, text=True)
    duration = result.stdout.strip()
    return duration!= ''

def file_is_corrupted(file_path):
    try:
        subprocess.run(['ffprobe', '-v', 'error', '-i', str(file_path)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        if 'moov atom not found' in str(e):
            return True
    return False

def delete_videos_without_duration(folder_path):
    folder_path = Path(folder_path)
    for path in folder_path.rglob('*'):
        if path.is_file() and path.suffix.lower() in video_extensions and (not has_duration(path) or file_is_corrupted(path)):
            print(f'Deleting {path}')
            os.remove(str(path))
