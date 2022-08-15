import asyncio
import csv
import sys
import time
from collections.abc import Iterator
from pathlib import Path
from urllib.parse import urlparse

import aiohttp
import click
from tqdm import tqdm

"""taken from https://www.twilio.com/blog/asynchronous-http-requests-in-python-with-aiohttp"""

EXEC = "execute"
DATA_DIR = "dir"


def get_filepath(url: str, root_dir: str) -> Path:
    return Path(root_dir) / Path(urlparse(url).path[1:])  # make it relative


def get_urls(
    file_name: str,
) -> Iterator[str]:
    with open(file_name, newline="") as csvfile:
        for url in csv.reader(csvfile):
            yield url[0]


async def get_file(session, url, /, **kwargs) -> bytes:
    if not kwargs.get(EXEC):
        return bytes(f"Downloading {url}", encoding="ascii")
    async with session.get(url) as resp:
        return await resp.read()


async def save_file(session, url, /, **kwargs) -> str:
    try:
        file_response = await get_file(session, url, **kwargs)
        file_path = get_filepath(url, kwargs[DATA_DIR])
        if kwargs.get(EXEC):
            file_path.parent.mkdir(parents=True, exist_ok=True)
            wrote_bytes = file_path.write_bytes(file_response)
            return f"Downloaded {file_path}({wrote_bytes/1024} kb)"
        return f"{url} -> {file_path}"
    except aiohttp.ClientResponseError as ae:
        return f"Failed to download {url}. status:{ae.status}, message:{ae.message}"
    except Exception as e:
        return f"Unknown error occurred processing  {url}. message:{e}"


async def async_main(data_dir: str, urls: Iterator[str], execute: bool) -> None:
    tasks = []
    async with aiohttp.ClientSession(raise_for_status=True) as session:
        for url in tqdm(urls):
            tasks.append(
                asyncio.ensure_future(
                    save_file(session, url, **{DATA_DIR: data_dir, EXEC: execute})
                )
            )
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        for response in tqdm(responses):
            print(response)


@click.option(
    "--data-dir", required=True, type=click.Path(exists=True), help="directory to save downloads"
)
@click.option(
    "--urls-file", required=True, type=click.Path(exists=True), help="urls to download"
)
@click.option("--execute", is_flag=True, default=False, help="required to do something")
@click.command()
def main(data_dir: str, urls_file: str, execute: bool) -> int:
    start_time = time.time()
    asyncio.run(async_main(data_dir, get_urls(urls_file), execute))
    print("--- %s seconds ---" % (time.time() - start_time))
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
