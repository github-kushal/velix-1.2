import pygame
import os

class LocalMusic:
    def init_player(self):
        self.pygame.mixer.init()
        print("Audio player initialized.")


    def load_file(self, file_path):
        self.file_p = input("Please enter the file path: ")
        self.file_p = file_path

        if not os.path.isfile(self.file_p):
            raise FileNotFoundError(f"{self.file_p} not found on its path.")
        self.pygame.mixer.music.load(self.file_p)
        print(f"Loaded file: {self.file_p}")
        return self.file_p

    def play_music(self):
        self.pygame.mixer.music.play()
        print("Playback started.")

    def pause_music(self):
        self.pygame.mixer.music.pause()
        print("Playback paused.")

    def resume_music(self):
        self.pygame.mixer.music.unpause()
        print("Playback resumed.")

    def stop_music(self):
        self.pygame.mixer.music.stop()
        print("Playback stopped.")


class OnlineMusic:
    