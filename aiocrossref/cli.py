import fire
from aiocrossref.client import CrossrefClient
from aiokit.utils import sync_fu


async def works(doi):
    async with CrossrefClient() as c:
        return await c.works(doi)


def main():
    fire.Fire(sync_fu(works))


if __name__ == '__main__':
    main()
