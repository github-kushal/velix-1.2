import time
from pathlib import Path
from shutil import copytree, copy2
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from velix.skills.files.file_operation import create_folder, delete_folder, delete_file
else:
    from ..files.file_operation import create_folder, delete_folder, delete_file


class BackupManager:
    def __init__(self):
        self.backup_root = Path("../../backup")
        self.backup_root.mkdir(parents=True, exist_ok=True)

    def create_backup(self, source: Path) -> None:
        backup_folder = self._create_backup_folder()
        destination = backup_folder / source.name
        self._copy(source, destination)
        # print(f"Backup created at: {destination}")
    
    def restore_backup(self, backup_folder: Path, destination: Path) -> None:
        if not backup_folder.exists():
            print(f"Backup folder {backup_folder} does not exist.")
            return
        
        if destination.exists():
            if destination.is_dir():
                delete_folder(destination)
            else:
                delete_file(destination)
        
        self._copy(backup_folder, destination)
        # print(f"Backup restored from {backup_folder} to {destination}")

    def delete_backup(self, backup_folder: Path) -> None:
        if backup_folder.exists():
            if backup_folder.is_dir():
                delete_folder(backup_folder)
            else:
                delete_file(backup_folder)
            # print(f"Backup folder {backup_folder} deleted.")
            # print(f"Backup folder {backup_folder} does not exist.")
        
    def cleanup(self, days: int) -> None:
        now = time.time()
        for backup in self.backup_root.iterdir():
            if backup.is_dir():
                backup_age = now - backup.stat().st_mtime
                if backup_age > days * 86400:  # Convert days to seconds
                    delete_folder(backup)
                    # print(f"Deleted old backup: {backup}")

    def list_backups(self) -> None:
        if not self.backup_root.exists():
            print("No backups found.")
            return
        
        backups = sorted(self.backup_root.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
        if not backups:
            print("No backups found.")
            return
        
        print("Available backups:")
        for backup in backups:
            if backup.is_dir():
                print(f"- {backup.name} (Created on: {time.ctime(backup.stat().st_mtime)})")

    def _generate_timestamp(self) -> str:
        return time.strftime("%Y%m%d_%H%M%S")
    
    def _create_backup_folder(self) -> Path:
        timestamp = self._generate_timestamp()
        backup_folder = self.backup_root / timestamp
        create_folder(backup_folder)
        return backup_folder

    def _copy(self, source: Path, destination: Path) -> None:
        if source.is_dir():
            copytree(source, destination)
        else:
            copy2(source, destination)