from aiohttp.client import ClientSession
from self_bot import Selfbot
from api import LineClient
from line_api.TalkService.ttypes import Settings
import asyncio
import aiohttp
import json
import sys
import os



def write_file(qr):
    os.system("rm .qr_code.txt")
    with open(".qr_code.txt", "w") as f:
        print(qr)
        f.write(qr)

con = aiohttp.ClientSession()
if len(sys.argv) > 3:
    client = LineClient(
            token=sys.argv[2],
            passwd=sys.argv[3],
            connector=con
            )
sb = Selfbot(client, con, sys.argv[1])
sb.main()

