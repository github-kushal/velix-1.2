import pygame
import os

class Audio:
    def __init__(self):
        pygame.mixer.init()
        print("Audio player initialized.")


    def load_file(self, file_p):
        # self.file_p = input("Please enter the file path: ")

        if not os.path.isfile(file_p):
            raise FileNotFoundError(f"{file_p} not found on its path.")
        pygame.mixer.music.load(file_p)
        print(f"Loaded file: {file_p}")
        return file_p

    def play_music(self):
        pygame.mixer.music.play()
        print("Playback started.")

    def get_duration(self):
        import time
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    def pause_music(self):
        pygame.mixer.music.pause()
        print("Playback paused.")

    def resume_music(self):
        pygame.mixer.music.unpause()
        print("Playback resumed.")

    def stop_music(self):
        pygame.mixer.music.stop()
        print("Playback stopped.")

    def online_music(self, song : str):
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        import webbrowser
        song.replace(" ", "%20")
        webbrowser.open(f"https://open.spotify.com/search/{song}")


    