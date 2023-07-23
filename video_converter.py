import os
from pathlib import Path
from tqdm import tqdm
from colorama import Fore
import pyfiglet
import random
import subprocess

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
        print(f'{self.r}  Version: v0.0.2 https://github.com/viniped \n{self.n}')

def main():
    banner = Banner('VidConverter')
    banner.print_banner()

    # Ask the user for the input folder path
    input_folder_path = input("Enter the path to the input folder: ")

    # Set the output folder inside the script's directory
    output_folder = Path(__file__).resolve().parent / "output"

    # Convert the user input to a Path object
    input_folder = Path(input_folder_path)

    # Loop through all the subfolders and files in the input folder
    for path in input_folder.glob("**/*"):
        # Check if the path is a file and ends with a video file extension
        if path.is_file() and path.suffix in [".avi", ".mkv", ".mov", ".wmv", ".flv", ".mpg", ".mpeg", ".webm", ".m4v", ".ts"]:
            # Create the output path by changing the file extension to .mp4
            relative_path = path.relative_to(input_folder)
            output_path = output_folder / relative_path.with_suffix(".mp4")

            # Create the output directory if it doesn't exist
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Run the ffmpeg command to convert the video to mp4 and remove original file
            subprocess.run(
            ["ffmpeg", "-v", "quiet", "-stats", "-y", "-i", str(path), "-vcodec", "h264", "-acodec", "aac", "-b:a", "128k", str(output_path)],
            check=True
            )

            # Remove the original file
            path.unlink()
            
if __name__ == "__main__":
    main()
    banner = Banner('VidConverter')
    banner.print_banner()