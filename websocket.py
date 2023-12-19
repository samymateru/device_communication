import asyncio
import websockets
import jwt
from urllib.parse import parse_qs
from collections import deque

SECRET_KEY = "1234567890"


class Websocket:

    def __init__(self):
        self.client_connections = deque()
        self.devices_list = {}

    async def websocket_handler(self, websocket, path):
        is_authenticated = await self.authenticate(websocket, path)
        if not is_authenticated:
            await websocket.close()
            return
        try:
            async for _ in websocket:
                message = await websocket.recv()

        except websockets.exceptions.ConnectionClosed:
            self.client_connections.remove(websocket)
            print(f"Connection closed for {websocket}")

    async def authenticate(self, websocket, path) -> bool:
        try:
            query_params = parse_qs(path[2:])
            authentication_token = query_params.get("authorization", [""])[0]
            decoded_payload = jwt.decode(authentication_token, SECRET_KEY, algorithms=['HS256'])
            self.client_connections.append(websocket)
            for device in decoded_payload.get("devices"):
                self.devices_list[device] = websocket
            return True
        except jwt.ExpiredSignatureError:
            return False
        except jwt.InvalidTokenError:
            return False

    async def loop(self):
        while 1:
            print(len(self.client_connections))
            await asyncio.sleep(1)

    async def main(self):
        server = await websockets.serve(self.websocket_handler, "localhost", 5000)
        task = asyncio.create_task(self.loop())
        await asyncio.gather(task, server.wait_closed())
        await server.wait_closed()
