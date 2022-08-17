from auto_login import LoginBot
from api import LineClient
import aiohttp

t, p = "lemon22@simaenaga.com", "kaiw0081"

client = LineClient(
    token=t,
    passwd=p,
    connector=aiohttp.ClientSession())
lb = LoginBot(client)
lb.main()
