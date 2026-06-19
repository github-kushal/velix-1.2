import zipfile as zf
import os

def zip_file(source_path, output_zip=None):
    try:
        # Set default output path if not provided
        if output_zip is None:
            output_zip = source_path + ".zip"
        
        with zf.ZipFile(output_zip, 'w', zf.ZIP_DEFLATED) as zipf:
            # If source is a directory, add all files
            if os.path.isdir(source_path):
                for root, dirs, files in os.walk(source_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_path)
                        zipf.write(file_path, arcname)
            # If source is a file, just add that file
            else:
                zipf.write(source_path, os.path.basename(source_path))
        print(f"Successfully created archive: {output_zip}")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    

def extract_zip(file_path):
    try:
        with zf.ZipFile(file_path) as zipref:
            zipref.extractall()
            print("File extracted successfully")
            for file in zipref.namelist():
                print(file)
    except Exception as e:
        print(e)

# zip_file("E:\\Velix-1.2\\velix\\skills\\browser", "E:\\Velix-1.2\\velix\\skills\\browser.zip")
# extract_zip("E:\\Velix-1.2\\velix\\skills\\browser.zip")