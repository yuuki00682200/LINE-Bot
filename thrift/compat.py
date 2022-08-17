#COMPAT  INI UNTUK STRINGIO KE BINARY
#ACIL. MOD

import sys
from functools import lru_cache

if sys.version_info[0] == 2:

    from cStringIO import StringIO as BufferIO

    @lru_cache(maxsize=10)
    def binary_to_str(bin_val):
        return bin_val

    @lru_cache(maxsize=10)
    def str_to_binary(str_val):
        return str_val

else:

    from io import BytesIO as BufferIO  # noqa

    @lru_cache(maxsize=10)
    def binary_to_str(bin_val):
        return bin_val.decode('utf8')

    @lru_cache(maxsize=10)
    def str_to_binary(str_val):
        return bytes(str_val, 'utf8')
