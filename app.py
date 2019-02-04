import asyncio

import aiohttp_jinja2
import aiojobs
import jinja2
from aiojobs.aiohttp import setup as job_setup
from aiohttp import web

import motor.motor_asyncio
import pathlib
from main.routes import routes
from main.middlewares import middlewares


async def init_mongo(app, config={}):
    client = motor.motor_asyncio.AsyncIOMotorClient(
        io_loop=app.loop,
        **config
    )
    return client


async def close_mongo(app):
    app.mongo.close()


async def startup(app):
    app.mongo = await init_mongo(app)
    app.scheduler = await aiojobs.create_scheduler(limit=4)


async def shutdown(app):
    await close_mongo(app)
    await app.scheduler.close()


async def create_app(loop):
    app = web.Application(loop=loop)

    job_setup(app)

    app.on_startup.append(startup)
    app.on_shutdown.append(shutdown)

    app.middlewares.extend(middlewares)

    for route in routes:
        app.router.add_route(**route)

    return app


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    web.run_app(create_app(loop))
