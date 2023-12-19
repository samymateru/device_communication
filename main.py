import asyncio
from websocket import Websocket
from sockets import Socket


async def main():
    websocket_ = Websocket()
    socket_ = Socket()
    await asyncio.gather(websocket_.main(), socket_.main())


if __name__ == "__main__":
    asyncio.run(main())
