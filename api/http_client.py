from thrift.transport.TTransport import TMemoryBuffer
from aiohttp.client import ClientSession
from frugal.aio.transport.http_transport import FHttpTransport


class HttpClient(FHttpTransport):
    def __init__(self, url, headers={}, timeout=5000, connector=None):
        super().__init__(0)
        self._url = url
        self._timeout = timeout / 1000
        self._headers = {}
        if not connector:
            self.session = ClientSession(conn_timeout=self._timeout)
        else:
            self.session = connector
            
        if headers:
            self._headers.update(headers)

    async def request(self, context, payload):
        try:
            async with self.session.post(
                url=self._url,
                data=payload[4:],
                headers=self._headers
            ) as response:
                if response.status == 200:
                    res = await response.content.read()
                    res = TMemoryBuffer(res)
                    return res
        except BaseException:
            pass
