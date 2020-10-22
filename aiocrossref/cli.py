import asyncio

import fire
from aiocrossref.client import CrossrefClient


async def works(doi):
    c = CrossrefClient()
    try:
        await c.start()
        return await c.works(doi)
    finally:
        await c.stop()


def cli(doi):
    return asyncio.get_event_loop().run_until_complete(works(doi))


def main():
    fire.Fire(cli)


if __name__ == '__main__':
    main()
