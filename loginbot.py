from auto_login import LoginBot
from api import LineClient
import aiohttp

t, p = "hoge.com", "password"

client = LineClient(
    token=t,
    passwd=p,
    connector=aiohttp.ClientSession())
lb = LoginBot(client)
lb.main()
