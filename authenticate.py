import os
from dotenv import load_dotenv
from ringcentral import SDK

load_dotenv()

client_id, client_secret, server_url = os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"), os.getenv("SERVER_URL")
username, extension, password = os.getenv("USERNAME"), os.getenv("EXTENSION"), os.getenv("PASSWORD")

def login_to_platform(client_id, client_secret, server_url, username, extension, password):
    sdk = SDK(client_id, client_secret, server_url)
    platform = sdk.platform()
    platform.login(username, extension, password)
    return platform
