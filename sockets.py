import asyncio


class Socket:
    def __init__(self, ip, port):
        self.client_connections = set()
        self.ip = ip
        self.port = port

    async def handle_client(self, reader, writer):
        self.client_connections.add(writer)
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break

                message = data.decode()
                print(f"Received {message!r}")

        except asyncio.CancelledError:
            self.client_connections.remove(writer)
        finally:
            writer.close()

    async def main(self):
        server = await asyncio.start_server(
            lambda r, w: asyncio.create_task(self.handle_client(r, w)),
            host=self.ip, port=self.port)

        async with server:
            await server.serve_forever()
