import os
import subprocess
from halo import Halo
from pathlib import Path
from colorama import Fore
import pyfiglet
import random
from utils import *


class Banner:
    def __init__(self, banner):
        self.banner = banner
        self.lg = Fore.LIGHTGREEN_EX
        self.w = Fore.WHITE
        self.cy = Fore.CYAN
        self.ye = Fore.YELLOW
        self.r = Fore.RED
        self.n = Fore.RESET

    def print_banner(self):
        colors = [self.lg, self.r, self.w, self.cy, self.ye]
        f = pyfiglet.Figlet(font='slant')
        banner = f.renderText(self.banner)
        print(f'{random.choice(colors)}{banner}{self.n}')
        print(f'{self.r}  Version: v0.0.3 https://github.com/viniped/vidconverter \n{self.n}')


def get_codec(file_path, stream_type):
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', f'{stream_type}:0',
        '-show_entries', 'stream=codec_name',
        '-of', 'default=noprint_wrappers=1:nokey=1',
        file_path
    ]
    codec = subprocess.check_output(cmd).decode('utf-8').strip()
    return codec


def convert_file(file_path):
    video_codec = get_codec(file_path, 'v')
    audio_codec = get_codec(file_path, 'a')

    if video_codec == "h264" and audio_codec == "aac" and file_path.lower().endswith(".mp4"):
        return
    
    file_name, file_extension = os.path.splitext(file_path)
    output_file = f"{file_name}.mp4"
    
    cmd = [
        'ffmpeg',
        '-v', 'quiet',
        '-stats',
        '-y',
        '-i', file_path,
        '-b:a', '128k',
        '-hide_banner'
    ]
     
    if video_codec == "h264" and audio_codec == "aac":
        cmd.extend(['-c:v', 'copy', '-c:a', 'copy'])

    elif video_codec != "h264" and audio_codec == "aac":
        cmd.extend(['-c:v', 'libx264', '-preset', 'ultrafast', '-threads', '2', '-c:a', 'copy', '-crf', '23', '-maxrate', '4M'])
    
    elif video_codec == "h264" and audio_codec != "aac":
        cmd.extend(['-c:v', 'copy', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2', '-crf', '23', '-maxrate', '4M'])
    
    elif video_codec != "h264" and audio_codec != "aac":
        cmd.extend(['-c:v', 'h264', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2', '-crf', '23', '-maxrate', '4M'])
    
    else:
        cmd.extend(['-c:v', 'h264', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2', '-crf', '23', '-maxrate', '4M'])
   
    cmd.append(output_file)
    
    print(cmd)
    subprocess.run(cmd)
    os.remove(file_path)


def convert_videos_in_folder(folder_path):
    delete_videos_without_duration(folder_path)
    
    spinner = Halo(text='Verificando vídeos para conversão...', spinner='dots')
    spinner.start()

    videos_to_convert = []

    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(tuple(video_extensions)):
                file_path = os.path.join(subdir, file)
                video_codec = get_codec(file_path, 'v')
                audio_codec = get_codec(file_path, 'a')
                
                if not (video_codec == "h264" and audio_codec == "aac" and file_path.lower().endswith(".mp4")):
                    videos_to_convert.append(file_path)

    spinner.stop()

    total_videos = len(videos_to_convert)
    
    if total_videos == 0:
        print("Todos os vídeos já estão no formato correto.")
        return
    else:
        print(f"{total_videos} vídeos precisam ser convertidos.")

    for index, video_path in enumerate(videos_to_convert):
        remaining_videos = total_videos - index
        print(f"Vídeos restantes: {remaining_videos}")
        convert_file(video_path)

    print("A conversão dos vídeos foi concluída.")


def main():
    banner = Banner('VidConverter')
    banner.print_banner()    
    folder_path = input("Digite o caminho da pasta onde estão os vídeos: ")
    delete_videos_without_duration(folder_path)
    convert_videos_in_folder(folder_path)

if __name__ == '__main__':
    main()