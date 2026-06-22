import pygame
import os

class LocalMusic:
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


class OnlineMusic:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    s_list = ["user-library-modify", "user-read-playback-position", "user-top-read", "user-read-recently-played", "playlist-modify-private", "playlist-modify-public", "app-remote-control", "streaming"]

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="07f0aed99984405895de4b21283b3e05",
                                                   client_secret="ff56d648d0cc4ab39cd4831317db0d50",
                                                   redirect_uri="http://127.0.0.1:8888/callback",
                                                   scope=s_list))
    
    res = sp.current_user_playlists(limit=20)

