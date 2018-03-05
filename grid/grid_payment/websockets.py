import asyncio
import websockets
import webbrowser
from urllib import parse
import json
import uuid

from ..lib import utils

base_url = "https://www.coinbase.com/oauth/authorize?"
client_id = "61638403d5bee9d1479b81788e5c81956d6c93af8dd078ef7d012716409bead5"


async def get_auth_token(future, uri, state):
    async with websockets.connect(uri) as ws:
        state_message = {
            'type': 'state',
            'state': state
        }

        state_json = json.dumps(state_message)

        await ws.send(state_json)

        while True:
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=20)
            except asyncio.TimeoutError:
                # No data in 20 seconds, check the connection.
                try:
                    pong_waiter = await ws.ping()
                    await asyncio.wait_for(pong_waiter, timeout=10)
                except asyncio.TimeoutError:
                    # No response to ping in 10 seconds, disconnect.
                    break
            else:
                print(f'got a message {msg}')
                await ws.close()
                future.set_result(msg)
                break


def get_token(hostname, redirect):
    state = str(uuid.uuid4())

    getVars = {
        'client_id': client_id,
        'redirect_uri': redirect,
        'response_type': 'code',
        'scope': 'wallet:transactions:send,wallet:accounts:read',
        'state': state,
        'account_currency': 'ETH',
        'meta[send_limit_amount]': '1',
        'meta[send_limit_currency]': 'USD',
        'meta[send_limit_period]': 'day'
    }

    url = base_url + parse.urlencode(getVars)
    print(f'making request to {url}')
    webbrowser.open(url)

    loop = asyncio.get_event_loop()
    future = asyncio.Future()
    asyncio.ensure_future(get_auth_token(future, f'ws://{hostname}', state))
    loop.run_until_complete(future)

    r = future.result()
    print(f'it is {r}')
    result = json.loads(r)

    utils.store_coinbase(result)

    ret = json.loads(future.result())
    return ret
