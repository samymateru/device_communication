import asyncio
from websocket import Websocket
from sockets import Socket
from dotenv import load_dotenv
import os

load_dotenv()

server_ipaddress = os.environ.get("SERVER_IPADDRESS")
websocket_port = os.environ.get("WEBSOCKET_PORT")
tcp_socket_port = os.environ.get("TCP_SOCKET_PORT")
async def main():
    websocket_ = Websocket(server_ipaddress, websocket_port)
    socket_ = Socket(server_ipaddress, tcp_socket_port)
    await asyncio.gather(websocket_.main(), socket_.main())


if __name__ == "__main__":
    asyncio.run(main())
