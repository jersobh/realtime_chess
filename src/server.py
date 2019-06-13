import asyncio
import json
from aiohttp.web import Application, Response
from aiohttp_sse import sse_response
import aiohttp_cors
import sockjs


rooms = {}
users = {}

async def ws_poll(msg, session):
    if msg.type == sockjs.MSG_OPEN:
        print('new user')
        print(session.id)
    elif msg.type == sockjs.MSG_MESSAGE:
        print(msg.data)
        data = json.loads(msg.data)
        print(data)

        if data['type'] == 'new_player':
            room_name = data['room']

            if room_name not in rooms:
                rooms[room_name] = {}
                rooms[room_name]['sessions'] = []
                rooms[room_name]['white'] = None
                rooms[room_name]['black'] = None

            rooms[room_name][session.id] = {}
            rooms[room_name][session.id]['ws'] = session
            rooms[room_name]['sessions'].append(session)
            rooms[room_name][session.id]['id'] = session.id
            if session.id not in users:
                users[session.id]={}
            users[session.id]['room'] = room_name
            if rooms[room_name]['white'] == None:
                rooms[room_name]['white'] = session
                rooms[room_name][session.id]['role'] = 'white'
                users[session.id]['role'] = 'white'
            elif rooms[room_name]['black'] == None:
                rooms[room_name]['black'] = session
                rooms[room_name][session.id]['role'] = 'black'
                users[session.id]['role'] = 'black'
            else:
                rooms[room_name][session.id]['role'] = 'watcher'
                users[session.id]['role'] = 'watcher'

            rooms[room_name][session.id]['ws'].send(json.dumps({'type': 'set_player', 'id': rooms[room_name][session.id]['id'], 'role': rooms[room_name][session.id]['role']}))

        if data['type'] == 'new_move':
            room_name = data['room']
            for user in rooms[room_name]['sessions']:
                    user.send(json.dumps({'type': 'update', 'fen': data['fen']}))

        if data['type'] == 'get_rooms':
            session.manager.broadcast(rooms)

    elif msg.type == sockjs.MSG_CLOSED:
        room_name = users[session.id]['room']
        if users[session.id]['role'] == 'white':
            rooms[room_name]['white'] = None
        elif users[session.id]['role'] == 'black':
            rooms[room_name]['black'] = None

        rooms[room_name]['sessions'].remove(session)
        del rooms[room_name][session.id]
        del users[session.id]
        session.manager.broadcast(json.dumps({'type': 'user_left', 'id': session.id}))
        session.manager.broadcast(rooms)



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
