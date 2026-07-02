import datetime
import sys
import threading
import time
import pygame

class Alarm:
    """Class to manage setting and playing alarms, and system restarts."""

    def __init__(self):
        self.alarm_playing = True

    def play_alarm(self, sound_file):
        """Plays the alarm sound indefinitely or until stopped/paused."""
        pygame.mixer.init()
        pygame.mixer.music.load(sound_file)
        while self.alarm_playing:
            pygame.mixer.music.play(-1)  # Play the music indefinitely
            # Wait for the music to finish or for the alarm to be paused
            while pygame.mixer.music.get_busy() and self.alarm_playing:
                time.sleep(1)  # Check every second
            pygame.mixer.music.stop()
            if not self.alarm_playing:
                # If alarm is paused, break out of the loop
                break

    def set_alarm(self, sound_file):
        """Sets an alarm for a specific time and monitors input to control it."""
        alarm_time = input("Please enter the alarm time (HH:MM): ")

        # Validate the input format
        try:
            datetime.datetime.strptime(alarm_time, "%H:%M")
        except ValueError:
            print("Invalid time format. Please use HH:MM.")
            return

        alarm_minute = datetime.datetime.strptime(alarm_time, "%H:%M").minute
        print(f"Alarm set for {alarm_time}. Waiting...")
        while True:
            now = datetime.datetime.now()
            current_minute = now.minute
            if now.strftime("%H:%M") == alarm_time:
                print("Alarm ringing. Wake Up!")
                # Start the alarm in a separate thread
                alarm_thread = threading.Thread(target=self.play_alarm, args=(sound_file,))
                alarm_thread.start()
                # Listen for user input to pause or resume the alarm
                while current_minute == alarm_minute:
                    user_input = input("Press 'p' to pause/restart the alarm or 's' to stop it: ").strip().lower()
                    if user_input == 'p':
                        # Toggle the alarm state
                        self.alarm_playing = not self.alarm_playing
                    elif user_input == 's':
                        # Stop the alarm
                        self.alarm_playing = False
                        break
                    time.sleep(1)  # Sleep for a second and check again
                    current_minute = datetime.datetime.now().minute
                pygame.mixer.music.stop()  # Stop the alarm when the minute changes or when user stops it
                break
            time.sleep(1)

    @staticmethod
    def restart_program():
        """Restarts the current program, with file objects and descriptors."""
        import subprocess
        try:
            p = subprocess.run([sys.executable] + sys.argv)
        except AttributeError:
            p = subprocess.Popen([sys.executable] + sys.argv)
        sys.exit(p.returncode)
 