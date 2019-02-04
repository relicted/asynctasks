import os
from aiohttp import web


@web.middleware
async def default_db(request, handler):
    DATABASE = os.getenv('DEFAULT_DATABASE')
    if not DATABASE:
        raise ValueError('Provide DATABASE env. variable')

    request.mongo = request.app.mongo
    request.db = request.app.mongo[DATABASE]
    resp = await handler(request)
    return resp


@web.middleware
async def handle_error(request, handler):
    try:
        response = await handler(request)
        return response
    except web.HTTPException as ex:
        message = ex.reason
        return web.json_response({'error': message}, status=ex.status)


middlewares = [
    default_db,
    handle_error
]