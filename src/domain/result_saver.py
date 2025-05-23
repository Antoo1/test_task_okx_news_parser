from typing import Iterable
from pathlib import Path
import json

from src.dto import NewsRecord
from src.infrastructure.logger import logger


class FileToFolderSaver:
    def save_records_to_file(
        self,
        records: Iterable[NewsRecord],
        folder: str,
        filename: str,
    ) -> None:
        output_folder = Path(folder.rstrip('/'))
        output_folder.mkdir(parents=True, exist_ok=True)
        path = f'{folder}/{filename}'
        with open(path, 'w') as f:
            payload = [r.dump_dict() for r in records]
            json.dump(payload, f)
        logger.info(f'results saved at {path}')
