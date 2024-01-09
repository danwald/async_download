from abc import ABC
from abc import abstractmethod
import asyncio
from collections.abc import Iterator
import csv
from functools import wraps
from itertools import filterfalse
from pathlib import Path
import sys
import time
from typing import Any
from typing import Callable
from urllib.parse import urlparse

import aiohttp
import click
from more_itertools import batched
from tqdm import tqdm


# workaround from https://github.com/pallets/click/issues/85
def coro(f: Callable) -> Callable:  # type: ignore
    @wraps(f)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = asyncio.run(f(*args, **kwargs))
        print(f"Time: {(time.time() - start_time):.3f} secs")
        return result

    return wrapper


class UrlProcessor(ABC):
    def __init__(self, url_file: str, batch_size: int):
        self.url_file = url_file
        self.batch_size = batch_size

    def get_urls(self) -> Iterator[str]:
        with open(self.url_file, newline="") as csvfile:
            for url in csv.reader(csvfile):
                try:
                    yield url[0]
                except Exception:
                    sys.stderr.write(
                        f'\nError processing record "{url}" from "{self.url_file}"'
                    )

    @abstractmethod
    async def handler(self, sesssion: aiohttp.ClientSession, url: str) -> str:
        ...

    async def runner(self, *args: Any, **kwargs: Any) -> None:
        async with aiohttp.ClientSession(raise_for_status=True) as session:
            total_urls = 0
            for batch_count, batch in enumerate(
                batched(self.get_urls(), self.batch_size), 1
            ):
                tasks = set()
                for total, url in enumerate(batch, 1):
                    tasks.add(asyncio.create_task(self.handler(session, url)))
                total_urls += total
                for result in tqdm(asyncio.as_completed(tasks), total=total):
                    response = await result
                    tqdm.write(response)
            tqdm.write(f"Processed {total_urls} urls within {batch_count} batches")


class Downloader(UrlProcessor):
    def __init__(self, execute: bool, out_dir: str, *args: Any, **kwargs: Any):
        self.execute = execute
        self.out_dir = out_dir
        super().__init__(*args, **kwargs)

    def get_filepath(self, url: str, root_dir: str) -> Path:
        return Path(root_dir) / Path(urlparse(url).path[1:])  # make it relative

    async def get_file(self, session: aiohttp.ClientSession, url: str) -> Any:
        if not self.execute:
            return bytes(f"Downloading {url}", encoding="ascii")
        async with session.get(url) as resp:
            return await resp.read()

    async def handler(self, session: aiohttp.ClientSession, url: str) -> str:
        try:
            file_response = await self.get_file(session, url)
            file_path = self.get_filepath(url, self.out_dir)
            if self.execute:
                file_path.parent.mkdir(parents=True, exist_ok=True)
                wrote_bytes = file_path.write_bytes(file_response)
                return f"Downloaded {file_path}({(wrote_bytes/1024):.2f} kb)"
            return f"{url} -> {file_path}"
        except aiohttp.ClientResponseError as ae:
            return f"Failed to download {url}. status:{ae.status}, message:{ae.message}"
        except Exception as e:
            return f"Unknown error occurred processing  {url}. message:{e}"


class Header(UrlProcessor):
    def __init__(self, headers: tuple[str], *args: Any, **kwargs: Any):
        self.headers = headers
        super().__init__(*args, **kwargs)

    def filter_headers(self, resp_headers: dict[str, str]) -> dict[str, str]:
        return dict(
            filterfalse(lambda kv: kv[0] not in self.headers, resp_headers.items())
        )

    async def handler(self, session: aiohttp.ClientSession, url: str) -> str:
        try:
            async with session.head(
                url, timeout=aiohttp.ClientTimeout(total=5)
            ) as resp:
                headers = self.filter_headers(resp.headers)
                return f"{url} {resp.status} {headers}"
        except aiohttp.ServerTimeoutError:
            return f"{url}. 408"
        except Exception as e:
            return f"Unknown error occurred processing  {url}. message:{e}"


@click.group()  # type: ignore
def main() -> int:
    return 0


@click.argument("urls", required=True, type=click.Path(exists=True))  # type: ignore
@click.option(
    "--batch-size",
    type=int,
    default=1000,
    help="number of concurrent requests (default: 1000)",
)  # type: ignore
@click.option(
    "--header",
    multiple=True,
    default=(
        "Content-Length",
        "Server",
    ),
    help="Headers to extract (default: Content-Length, Server)",
)  # type: ignore
@main.command()  # type: ignore
@coro
async def headers(urls: str, batch_size: int, header: tuple[str]) -> None:
    await Header(header, urls, batch_size).runner()


@click.argument(
    "out_dir",
    default=Path.cwd(),
    type=click.Path(exists=True),
)  # type: ignore
@click.argument("urls", required=True, type=click.Path(exists=True))  # type: ignore
@click.option(
    "--execute", is_flag=True, default=False, help="required to do something"
)  # type: ignore
@click.option(
    "--batch-size",
    type=int,
    default=1000,
    help="number of concurrent requests (default: 1000)",
)  # type: ignore
@main.command()  # type: ignore
@coro
async def download(
    urls: str,
    out_dir: str,
    execute: bool,
    batch_size: int,
) -> None:
    await Downloader(execute, out_dir, urls, batch_size).runner()
