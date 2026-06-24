class Library:
    """docstring for Library."""
    def __init__(self):
        self.files = []

    def scan_music_folder(self, folder_path = "C:\\Users\\kusha\\Music"):
        try:
            import glob
            import os

            if os.path.isdir(folder_path):
                pattern = os.path.join(folder_path, "**", "*.mp3")
            else:
                pattern = folder_path

            self.files = glob.glob(pattern, recursive=True)
            

            return self.files
        except Exception as e:
            raise e
        
    def get_all_aongs(self):
        try:
            print(f"Number of total songs: {len(self.files)}")
            for idx, fl in enumerate(self.files):
                print(f"{idx} : {fl}")
        except Exception as e:
            raise e
        
    


import json
def json_list():
    lib = Library()
    files = lib.scan_music_folder()
    with open("sample.json", "w") as outfile:
        d = {}
        for idx, fl in enumerate(files):
            idx = idx + 1
            d[idx] = fl
        json.dump(d, outfile, indent=1)

json_list()