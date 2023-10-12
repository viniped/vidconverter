import os
from pathlib import Path
from tqdm import tqdm
from colorama import Fore
import pyfiglet
import random
import subprocess
from utils import delete_videos_without_duration

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
    
    cmd = [
        'ffmpeg',
        '-v', 'quiet',    
        '-stats',        
        '-y',            
        '-i', file_path, 
        '-b:a', '128k'   
    ]

    # se video_codec = h264 e audio_codec = aac copiar ambos os codecs
    if video_codec == "h264" and audio_codec == "aac":
        cmd.extend(['-c:v', 'copy', '-c:a', 'copy'])
    # se video_codec diferente de h264 e audio codec = aac transformar codec de video para h264 e copiar o codec de audio
    elif video_codec != "h264" and audio_codec == "aac":
        cmd.extend(['-c:v', 'libx264', '-preset', 'ultrafast', '-threads', '2', '-c:a', 'copy','crf' '23', 'maxrate' '4'])
    # se audio_codec diferente de aac e video_codec = h264 transformar codec de audio para aac e copiar o codec de video
    elif video_codec == "h264" and audio_codec != "aac":
        cmd.extend(['-c:v', 'copy', '-c:a', 'aac', '-preset', 'ultrafast', '-threads', '2','crf' '23', 'maxrate' '4'])
    
    output_file = f"{os.path.splitext(file_path)[0]}.mp4"
    cmd.append(output_file)
    
    subprocess.run(cmd)
    os.remove(file_path)

def main():

    banner = Banner('VidConverter')
    banner.print_banner()
    
    folder_path = input("Digite o caminho da pasta onde estão os vídeos: ")

    delete_videos_without_duration(folder_path)
    
    # Percorrer o diretório de forma recursiva
    for subdir, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((".mp4", ".ts", ".mpg", ".mpeg", ".avi", ".mkv", ".flv", ".3gp", ".rmvb", ".webm", ".vob", ".ogv", ".rrc",
    ".gifv", ".mng", ".mov", ".qt", ".wmv", ".yuv", ".rm", ".asf", ".amv", ".m4p", ".m4v", ".mp2", ".mpe",
    ".mpv", ".m4v", ".svi", ".3g2", ".mxf", ".roq", ".nsv", ".f4v", ".f4p", ".f4a", ".f4b")):
                file_path = os.path.join(subdir, file)
                convert_file(file_path)

if __name__ == '__main__':
    main()
