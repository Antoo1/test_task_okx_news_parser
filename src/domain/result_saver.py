from typing import Iterable
from pathlib import Path
import json

from src.dto import NewsRecord


class FileToFolderSaver:
    def save_records_to_file(
        self,
        records: Iterable[NewsRecord],
        folder: str,
        filename: str,
    ) -> None:
        output_folder = Path(folder)
        output_folder.mkdir(parents=True, exist_ok=True)
        with open(f'{folder}/{filename}', 'w') as f:
            payload = [r.dump_dict() for r in records]
            json.dump(payload, f)
