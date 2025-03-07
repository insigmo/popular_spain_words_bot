import logging
import pickle
import sys
from typing import Any

import brotli


class Compressor:
    @classmethod
    def compress(cls, data: Any) -> bytes:
        before_size = sys.getsizeof(data)
        data = brotli.compress(pickle.dumps(data))
        after_size = sys.getsizeof(data)
        cls._logger().debug(f'{before_size=} {after_size=} and compressed about {before_size - after_size} bytes')
        return data

    @classmethod
    def decompress(cls, data: bytes) -> Any:
        return pickle.loads(brotli.decompress(data))

    @classmethod
    def _logger(cls) -> logging.Logger:
        return logging.getLogger(__name__)


if __name__ == '__main__':
    d = [1234]
    da = Compressor.compress(d)
    print(Compressor.decompress(da))
