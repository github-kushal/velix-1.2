import screen_brightness_control as sbc 

def set_brightness(level:int):
    try:
        brightness = sbc.get_brightness()

        sbc.set_brightness(level)
        print("Brightness set to " + str(level))
    except Exception as e:
        return str(e)

def set_volume(level):
    try:
        level = float(level)/100
        from pycaw.pycaw import AudioUtilities
        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        print(f"Audio output: {device.FriendlyName}")
        print(f"- Muted: {bool(volume.GetMute())}")
        print(f"- Volume level: {volume.GetMasterVolumeLevel()} dB")
        print(f"- Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
        volume.SetMasterVolumeLevelScalar(level, None)
    except Exception as e:
        raise e

