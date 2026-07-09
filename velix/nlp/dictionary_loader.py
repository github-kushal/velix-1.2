import os
import json
from glob import glob

def load_dictionary(folder_path:str = "E:\\Velix-1.2\\velix\\nlp\\data\\protected"):
    """
    Purpose: load dictionary from the folder path
    """

    

    if not os.path.isdir(folder_path):
            raise NotADirectoryError(f"Provided path '{folder_path}' is not a valid directory.")
    
    files = glob(os.path.join(folder_path, "*.json"))
    # print(files)
    dictionary = []

    if not files:
            print("No JSON files found in the folder.")
            return []

    for file in files:
        try:
            with open(file, "r", encoding="utf-8") as file:
                data = json.load(file)
                dictionary.append(data)
        except json.JSONDecodeError as e:
            print(f"Skipping '{file}' due to JSON decoding error: {e}")
        except Exception as e:
            print(f"Error reading '{file}': {e}")

    return dictionary

print(load_dictionary())