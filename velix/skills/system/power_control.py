import os

class SystemPower:
    def shutdown(delay:int=0):
        os.system(f"shutdown /s /t {delay}")
    
    def restart(delay:int=0):
        os.system(f"shutdown /r /t {delay}")

    def sleep():
        os.system('shutdown /h')

class CodeControl:
    def reset():
        import time
        try:
            print("\nRestarting script...\n")
            time.sleep(0.5)
            # Replace current process with a new one running the same script
            os.execv(sys.executable, [sys.executable] + sys.argv)
        except Exception as e:
            print(f"Error restarting script: {e}")
            sys.exit(1)
        