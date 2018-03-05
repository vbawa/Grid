import webbrowser
from urllib import parse
import json
import uuid
import requests
from . import websockets

class GridPayment():
    def __init__(self):
        self.client_id = "61638403d5bee9d1479b81788e5c81956d6c93af8dd078ef7d012716409bead5"
        self.state = uuid.uuid4().int
        self.host = 'https://opengrid.ai/'
        self.redirect = self.host + '/callback'

    def authorize(self):
        return websockets.get_token()

    def send_ether(self, access_token, refresh_token, email, amount):
        send_obj = {
            'accessToken': access_token,
            'refreshToken': refresh_token,
            'email': email,
            'amount': amount
        }

        route = "/api/v0/sendEther"

        r = requests.post(self.host + route, json=send_obj)

        if r.status_code == 402:
            send_obj['two_factor_code'] = input()

            r = requests.post(host + route, json=send_obj)

            print(r.status_code)
        else:
            print(r.status_code)
