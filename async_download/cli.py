"""Console script for async_download."""
import sys
import pathlib
import time


import click
import aiohttp
import asyncio
import tqdm




async def get_file(session, url):
    async with session.get(url) as resp:
        return await resp.data()


async def async_main(urls):

    async with aiohttp.ClientSession() as session:

        tasks = []
        for url in urls:
            tasks.append(asyncio.ensure_future(get_file(session, url)))

        files = await asyncio.gather(*tasks)
        for file in files:
            (pokemon)


@@click.option('--data-dir', required=True, default='./data', type=click.Path(exists=True), help='cred filename')
@click.option('--urls-file', required=True, type=click.Path(exists=True), help='urls in file one')
@click.option('--execute', is_flag=True, default=False, help='required to delete objects')
@click.command()
def main(data_dir, urls_file, workers, execute, container):
	print("--- %s seconds ---" % (time.time() - start_time))
	asyncio.run(async_main())
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
