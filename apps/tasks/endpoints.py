from aiohttp import web
from bson import ObjectId
from bson.errors import InvalidId
from bson.json_util import dumps as mongo_dumps
from apps.tasks.tasks import task


class Handler(web.View):

    def __init__(self, request):
        super(Handler, self).__init__(request)

        self.scheduler = request.app.scheduler
        self.db = request.mongo.asynctest

    async def get_tasks(self, id):
        if not id:
            tasks = []
            async for t in self.db.tasks.find():
                tasks.append(t)

            return web.json_response({}, dumps=mongo_dumps)

        try:
            task = await self.db.tasks.find_one({'_id': ObjectId(id)})
            if not task:
                return web.json_response({}, status=404)

            return web.json_response(task, dumps=mongo_dumps)
        except InvalidId:
            return web.json_response({'error': 'Wrong Id'}, status=400)

    async def get(self):
        data = await self.request.json()

        return await self.get_tasks(data.get('id'))

    async def post(self):
        data = await self.request.json()
        new_task = await self.db.tasks.insert_one({
            'status': 'new',
            'url': data.get('url')
        })

        await self.scheduler.spawn(task(self.db, new_task.inserted_id, url=data.get('url')))

        return web.json_response({'success': 'task created'}, status=201)