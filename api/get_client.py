from thrift.protocol.TCompactProtocol import TCompactProtocolAcceleratedFactory
from thrift.transport.THttpClient import THttpClient
from thrift.protocol import TCompactProtocol
from .legy_factory import LegyProtocolFactory
from frugal.provider import FServiceProvider
from .http_client import HttpClient


class Client:
    def __init__(self, host, context, headers, connector):
        self._host = host
        self._context = context
        self._headers = headers
        self._connector = connector

    def update_header(self, header):
        self._headers.update(header)

    def get_client_with_sync(self, path, service):
        transport = THttpClient(self._host + path)
        transport.setCustomHeaders(self._headers)
        protocol = TCompactProtocol.TCompactProtocol(transport)
        return service.Client(protocol)

    def get_client(self, path, service):
        transport = HttpClient(self._host + path, headers=self._headers, connector=self._connector)
        protocol = TCompactProtocolAcceleratedFactory()
        wrapper = LegyProtocolFactory(protocol)
        service_provider = FServiceProvider(transport, wrapper)
        return service.Client(service_provider)
