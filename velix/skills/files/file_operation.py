import shutil
import os

def copy_file(file_path, destination_path):
    shutil.copy(file_path, destination_path)
    return

def copy_folder(folder_path, destination_path):
    shutil.copytree(folder_path, destination_path)
    return

def delete_folder(folder_path):
    shutil.rmtree(folder_path)
    return

def delete_file(file):
    os.remove(file)

def move(src, dest):
    shutil.move(src, dest)
    return

def create_file(file_name):
    open(file_name, 'w')

def create_folder(folder_name):
    os.mkdir(folder_name)

def rename(src, dest):
    os.rename(src, dest)

def search(file_path):
    location = shutil.which(file_path)
    print(location)