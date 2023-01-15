import asyncio
import csv
import sys
import time
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
import click
from more_itertools import batched
from tqdm import tqdm


EXEC = 'execute'
DATA_DIR = 'dir'


def get_filepath(url: str, root_dir: str) -> Path:
    return Path(root_dir) / Path(urlparse(url).path[1:])  # make it relative


def get_urls(
    file_name: str,
) -> Iterator[str]:
    with open(file_name, newline='') as csvfile:
        for url in csv.reader(csvfile):
            try:
                yield url[0]
            except Exception:
                sys.stderr.write(
                    f'\nError processing record "{url}" from "{file_name}"'
                )


async def get_file(session, url, /, **kwargs) -> bytes:
    if not kwargs.get(EXEC):
        return bytes(f'Downloading {url}', encoding='ascii')
    async with session.get(url) as resp:
        return await resp.read()


async def save_file(session, url, /, **kwargs) -> str:
    try:
        file_response = await get_file(session, url, **kwargs)
        file_path = get_filepath(url, kwargs[DATA_DIR])
        if kwargs.get(EXEC):
            file_path.parent.mkdir(parents=True, exist_ok=True)
            wrote_bytes = file_path.write_bytes(file_response)
            return f'Downloaded {file_path}({(wrote_bytes/1024):.2f} kb)'
        return f'{url} -> {file_path}'
    except aiohttp.ClientResponseError as ae:
        return f'Failed to download {url}. status:{ae.status}, message:{ae.message}'
    except Exception as e:
        return f'Unknown error occurred processing  {url}. message:{e}'


async def heads(session, url) -> str:
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=5)) as resp:
            return f'{url} {resp.status}'
    except aiohttp.ServerTimeoutError:
        return f'{url}. 408'
    except Exception as e:
        return f'Unknown error occurred processing  {url}. message:{e}'


async def async_main(
        data_dir: str, urls: Iterator[str], execute: bool, validate: bool, batch_size: int
) -> None:
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        total_urls = 0
        for batch_count, batch in enumerate(batched(urls, batch_size), 1):
            tasks = set()
            for total, url in enumerate(batch, 1):
                tasks.add(
                    asyncio.create_task(
                        heads(session, url)
                        if validate
                        else save_file(session, url, **{DATA_DIR: data_dir, EXEC: execute})
                    )
                )
            total_urls += total
            for result in tqdm(asyncio.as_completed(tasks), total=total):
                response = await result
                tqdm.write(response)
        tqdm.write(f'Processed {total_urls} urls within {batch_count} batches')


@click.option(
    '--data-dir',
    default=Path.cwd(),
    type=click.Path(exists=True),
    help='directory to save downloads',
)
@click.option(
    '--urls-file', required=True, type=click.Path(exists=True), help='urls to download'
)
@click.option('--execute', is_flag=True, default=False, help='required to do something')
@click.option(
    '--validate',
    is_flag=True,
    default=False,
    help='HEAD request validates urls returning https.status',
)
@click.option(
    '--batch-size',
    type=int,
    default=1000,
    help='number of concurrent requests (default: 1000)',
)
@click.command()
def main(data_dir: str, urls_file: str, execute: bool, validate: bool, batch_size: int) -> int:
    start_time = time.time()
    asyncio.run(async_main(data_dir, get_urls(urls_file), execute, validate, batch_size))
    print(f'Time: {(time.time() - start_time):.3f} secs')
    return 0


if __name__ == '__main__':
    sys.exit(main())  # pragma: no cover
