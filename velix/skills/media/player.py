# pyrefly: ignore [missing-import]
import pygame
import os
import json
import time

class Audio:
    def __init__(self):
        pygame.mixer.init()
        print("Audio player initialized.")
        self.paths = []

    def load_json(self):
        with open("sample.json", "r") as files:
            lines = json.load(files)
        for i in range(0, len(lines)):
            self.paths.append(lines[i])
        return self.paths


    def play_music(self, play_forever=False):
        self.load_json()
        pygame.mixer.init()
        tracks = self.paths
        valid_tracks = [track['file'] for track in tracks if os.path.exists(track['file'])]

        try:
            while True:
                for track in valid_tracks:
                    try:
                        print(f"Current playing song is : {os.path.basename(track)}")
                        pygame.mixer.music.load(track)
                        pygame.mixer.music.play()

                        while pygame.mixer.music.get_busy():
                            time.sleep(0.1)
                            
                    except pygame.error as e:
                        raise f"Error playing song {track} : {e} "

                if not play_forever:
                    break
                    
                
        except KeyboardInterrupt:
            print("user stopped manually")  
        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()

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

    

l = Audio()
l.play_music()
