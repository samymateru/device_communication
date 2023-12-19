import asyncio


class Socket:
    def __init__(self):
        self.client_connections = set()

    async def handle_client(self, reader, writer):
        self.client_connections.add(writer)
        try:
            while True:
                data = await reader.read(1024)
                if not data:
                    break

                message = data.decode()
                print(f"Received {message!r}")
                print(len(self.client_connections))

        except asyncio.CancelledError:
            self.client_connections.remove(writer)
        finally:
            writer.close()

    async def main(self):
        server = await asyncio.start_server(
            lambda r, w: asyncio.create_task(self.handle_client(r, w)),
            '127.0.0.1', 4000)

        async with server:
            await server.serve_forever()
