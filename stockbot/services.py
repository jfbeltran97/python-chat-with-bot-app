import requests

from conf import (
    BOT_USERNAME,
    BOT_PASSWORD,
    SERVER_HOST,
    SERVER_API_LOGIN_ENDPOINT,
    SERVER_API_CHATROOM_LIST_ENDPOINT,
    SERVER_SCHEMA,
)


def build_url(endpoint, schema=SERVER_SCHEMA, host=SERVER_HOST):
    return f'{schema}://{host}{endpoint}'
 

class APIService:
    def __init__(self, token=None):
        self.token = token
       
    @property
    def headers(self):
        if self.token == None:
            return None
        return {'Authorization': f'Token {self.token}'}


class AuthService(APIService):
    url = build_url(SERVER_API_LOGIN_ENDPOINT)
    username = BOT_USERNAME
    password = BOT_PASSWORD
    token = None

    def login(self):
        response = requests.post(self.url, json={
            'username': self.username,
            'password': self.password,
        })
        if response.ok:
            response = response.json()
            self.token = response['token']
        return self.token


class ChatService(APIService):
    url = build_url(SERVER_API_CHATROOM_LIST_ENDPOINT)

    def list_chatrooms(self):
        """
        Gets a list of chatrooms
        """
        response = requests.get(self.url, headers={
            'Authorization': f'Token {self.token}'
        })
        if response.ok:
            response = response.json()
            return response
        return []
