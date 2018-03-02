import asyncio
import requests
import uuid

base_url = "https://www.coinbase.com/oauth/authorize?"
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
                print(f'got a message??? {msg}')
				await ws.close()
				future.set_reseult(msg)
				break
				

def get_token():
	
	state = str(uuid.uuid4())
	
	url = base_url + parse.urlencode(getVars)
	print(f'making request to {url}')
	webbrowser.open(url)
	
	loop = asyncio.get_event_loop()
	future = asyncio.Future()
	asyncio.ensure_future(get_auth_token(future, 'ws://localhost:3000', state))
	loop.run_until_complete(future)
	
	print(f'future result: {future}')
	loop.close()