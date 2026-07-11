from pathlib import Path
from shutil import copytree, copy2
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from velix.skills.ai_editor.backup import BackupManager
else:
    from .backup import BackupManager


class FileManager:
    def __init__(self):
        self.backup_manager = BackupManager()

    def _backup_if_exists(self, target: Path) -> None:
        if target.exists():
            self.backup_manager.create_backup(target)

    def read(self, file_path: Path) -> str:
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist.")

        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def write(self, file_path: Path, content: str) -> None:
        self._backup_if_exists(file_path)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def append(self, file_path: Path, content: str) -> None:
        self._backup_if_exists(file_path)

        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(content)

    def delete(self, file_path: Path) -> None:
        self._backup_if_exists(file_path)

        if file_path.exists():
            file_path.unlink()
        else:
            raise FileNotFoundError(f"File {file_path} does not exist.")

    def rename(self, old_path: Path, new_path: Path) -> None:
        self._backup_if_exists(old_path)
        self._backup_if_exists(new_path)

        if not old_path.exists():
            raise FileNotFoundError(f"File {old_path} does not exist.")

        old_path.rename(new_path)

    def move(self, source: Path, destination: Path) -> None:
        self._backup_if_exists(source)
        self._backup_if_exists(destination)

        if not source.exists():
            raise FileNotFoundError(f"Source {source} does not exist.")

        if source.is_dir():
            copytree(source, destination)
            for item in source.iterdir():
                if item.is_file():
                    item.unlink()
                else:
                    self.delete(item)
            source.rmdir()
        else:
            copy2(source, destination)
            source.unlink()

    def copy(self, source: Path, destination: Path) -> None:
        self._backup_if_exists(destination)

        if not source.exists():
            raise FileNotFoundError(f"Source {source} does not exist.")

        if source.is_dir():
            copytree(source, destination)
        else:
            copy2(source, destination)

    def exists(self, file_path: Path) -> bool:
        return file_path.exists()

    def create_directory(self, dir_path: Path) -> None:
        self._backup_if_exists(dir_path)

        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    def delete_directory(self, dir_path: Path) -> None:
        self._backup_if_exists(dir_path)

        if dir_path.exists() and dir_path.is_dir():
            for item in dir_path.iterdir():
                if item.is_file():
                    item.unlink()
                else:
                    self.delete_directory(item)
            dir_path.rmdir()
        else:
            raise FileNotFoundError(f"Directory {dir_path} does not exist.")

    def list_directory(self, dir_path: Path) -> list:
        if not dir_path.exists() or not dir_path.is_dir():
            raise FileNotFoundError(f"Directory {dir_path} does not exist.")

        return [item.name for item in dir_path.iterdir()]

    def get_metadata(self, file_path: Path) -> dict:
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist.")

        metadata = {
            "name": file_path.name,
            "size": file_path.stat().st_size,
            "created": file_path.stat().st_ctime,
            "modified": file_path.stat().st_mtime,
            "is_directory": file_path.is_dir()
        }
        return metadata

    def detect_file_type(self, file_path: Path) -> str:
        if not file_path.exists():
            raise FileNotFoundError(f"File {file_path} does not exist.")

        if file_path.is_dir():
            return "directory"
        else:
            return file_path.suffix[1:]  # Return the file extension without the dot