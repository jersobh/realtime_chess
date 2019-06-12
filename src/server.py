import asyncio
import json
from aiohttp.web import Application, Response
from aiohttp_sse import sse_response
import aiohttp_cors
import sockjs


users = []

async def ws_poll(msg, session):
    if msg.type == sockjs.MSG_OPEN:
        user = {}
        user['session'] = session
        if len(users) == 0:
            user['color'] = 'white'
        else:
            user['color'] = 'black'
        users.append(user)
        print(users)
        session.manager.broadcast(user)

    elif msg.type == sockjs.MSG_MESSAGE:
        print(msg.data)
        data = json.loads(msg.data)
        session.manager.broadcast(data)
    elif msg.type == sockjs.MSG_CLOSED:
        session.manager.broadcast({"type": "message", "data": "Someone left"})


async def factory():
    loop = asyncio.get_event_loop()
    app = Application(loop=loop)

    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
    })

    sockjs.add_endpoint(app, ws_poll, name='ws', prefix='/ws/')
    return app
