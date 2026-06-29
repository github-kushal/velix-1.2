import screen_brightness_control as sbc 

def set_brightness(level:int):
    try:
        brightness = sbc.get_brightness()

        sbc.set_brightness(level)
        print("Brightness set to " + str(level))
    except Exception as e:
        return str(e)

def set_volume(level : float):
    try:
        level = level/100
        from pycaw.pycaw import AudioUtilities
        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        print(f"volume set to {level:.2f}%")
        volume.SetMasterVolumeLevelScalar(level, None)
    except Exception as e:
        raise e