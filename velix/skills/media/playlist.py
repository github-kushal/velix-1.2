from pathlib import Path
import re

folder = Path(r"C:\\Users\\kusha\\Music\\fonk")

used_names = {}

for file in folder.glob("*.mp3"):
    name = file.stem

    # Remove numbering
    name = re.sub(r'^\d+\.\s*', '', name)

    # Remove [Spotitrack]
    name = re.sub(r'\[.*?\]\s*', '', name)

    # Keep text before artist names
    name = name.split(" - ")[0]

    # Remove modifiers
    for pattern in [
        r'\(.*?\)',
        r'\bSLOWED\b',
        r'\bSUPER\s*SLOWED\b',
        r'\bULTRA\s*SLOWED\b',
        r'\d+\.\d+'
    ]:
        name = re.sub(pattern, '', name, flags=re.IGNORECASE)

    name = re.sub(r'\s+', ' ', name).strip()

    # Handle duplicate names
    if name in used_names:
        used_names[name] += 1
        name = f"{name} ({used_names[name]})"
    else:
        used_names[name] = 1

    new_file = file.with_name(name + file.suffix)

    print(f"Renaming:\n{file.name}\n-> {new_file.name}\n")

    file.rename(new_file)

print("Done!")