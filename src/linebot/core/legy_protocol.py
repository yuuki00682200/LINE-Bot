from frugal.protocol import FProtocol


class LegyProtocol(FProtocol):

    def write_request_headers(self, *args, **kws):
        pass

    def write_response_headers(self, *args, **kws):
        pass

    def _write_headers(self, *args, **kws):
        pass

    def read_request_headers(self):
        pass

    def read_response_headers(self, *args, **kws):
        pass


