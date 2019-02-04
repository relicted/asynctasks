import random
import asyncio
import aiohttp

from aiohttp.client import InvalidURL

async def fetch(session, url):
    async with session.get(url) as response:
        return response


async def task(db, _id, url=''):
    await db.tasks.find_one_and_update(
        {'_id': _id},
        {'$set': {'status': 'pending'}}
    )
    await asyncio.sleep(random.randint(5, 10))
    session = aiohttp.ClientSession()
    try:
        async with session.get(url) as resp:

            update = {
                'content_length':  resp.content_length,
                'response_status': resp.status,
                'status': 'completed',
                'response_body': await resp.text()
            }

            await db.tasks.find_one_and_update(
                {'_id': _id},
                {'$set': update}
            ),

    except (InvalidURL,):
        await db.tasks.find_one_and_update(
            {'_id': _id},
            {'$set': {'status': 'error'}}
        )

    await session.close()
