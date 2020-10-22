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


if __name__ == '__main__':
    def main(doi):
        return asyncio.get_event_loop().run_until_complete(works(doi))
    fire.Fire(main)
