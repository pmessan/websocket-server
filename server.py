"""WS server example."""
import asyncio
from typing import Optional
from pathlib import Path
import ssl
import json

import websockets
from websockets import (
    WebSocketServerProtocol,
    WebSocketException,
    WebSocketServer,
)


USE_SSL = False

JSON_MESSAGE = {
  "api_version": "1.0",
  "event_type": "feedback!",
  "event_id": "02114da8-feae-46e3-8b00-a3f7ea8672df",
  "time_created": 1546300800000,
  "device_serial": "M2MR111101051",
  "feedback_action_id": "FEEDBACK_POSITIVE"
}

async def _hello(client: WebSocketServerProtocol, path: str) -> None:
    print(f'client {client.remote_address} at {path}')

    if JSON_MESSAGE:
        await client.send(json.dumps(JSON_MESSAGE).encode())

    try:
        async for message in client:
            print(f'received {message}')
    except WebSocketException as e:
        print('Websocket error', e)
    finally:
        print('client disconnected')
        await client.close()


async def _start() -> None:
    if USE_SSL:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        cert_pem = Path("cert.pem")
        cert_key = Path("key.pem")
        ssl_context.load_cert_chain(
            certfile=cert_pem,
            keyfile=cert_key,
        )
    else:
        ssl_context = None

    addr = "192.168.178.124"
    port = 4242

    server: Optional[WebSocketServer] = None
    try:
        print(f'starting server on {addr}:{port}' )
        server = await websockets.serve(
            _hello,
            addr,
            port,
            create_protocol=websockets.basic_auth_protocol_factory(
                realm="my dev server",
                credentials=("foo", "bar"),
            ),
            # ssl=ssl_context,
        )
    except asyncio.CancelledError:
        if server is not None:
            server.close()
            await server.wait_closed()


try:
    asyncio.get_event_loop().run_until_complete(_start())
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    pass
finally:
    asyncio.get_event_loop().stop()
