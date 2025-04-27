import asyncio
import click
from datetime import datetime

from src.infrastructure.config import config
from src.infrastructure.logger import logger
from src.service import OKXScrapingService
from src.dto import NewsRequest
from src.domain.result_saver import FileToFolderSaver


@click.command()
@click.option('--start-date', required=True, help='Start date in ISO format (YYYY-MM-DD)')
@click.option('--end-date', required=True, help='End date in ISO format (YYYY-MM-DD)')
@click.option('--folder', required=True, type=click.Path(file_okay=False, writable=True),
              help='Output folder path')
def main(start_date, end_date, folder):
    asyncio.run(_main(start_date, end_date, folder))


async def _main(start_date, end_date, folder):
    try:
        start = datetime.fromisoformat(start_date).date()
        end = datetime.fromisoformat(end_date).date()

        if start > end:
            raise ValueError("Start date cannot be after end date")

        request = NewsRequest(
            start_date=start,
            end_date=end,
        )

        records = await OKXScrapingService().get_news_by_period(request)
        FileToFolderSaver().save_records_to_file(records, folder, filename=config.FILENAME)
        click.echo(f'Results {config.FILENAME} saved in {folder}')

    except ValueError as e:
        logger.error(
            f"Error: Invalid date format. Please use ISO format (YYYY-MM-DD). {e}", exc_info=e
        )
    except Exception as e:
        logger.error(
            f"Unexpected error. {e}", exc_info=e
        )
