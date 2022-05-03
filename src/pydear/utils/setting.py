from typing import Optional, Dict
import struct
import logging
import pathlib


LOGGER = logging.getLogger(__name__)


class BinReader:
    def __init__(self, data: bytes) -> None:
        self.data = data
        self.pos = 0

    def is_end(self) -> bool:
        return self.pos >= len(self.data)

    def bytes(self, len: int) -> bytes:
        data = self.data[self.pos:self.pos+len]
        self.pos += len
        return data

    def str(self, len: int, encoding: str) -> str:
        data = self.bytes(len)
        return data.decode(encoding=encoding)

    def int32(self) -> int:
        data = self.bytes(4)
        return struct.unpack('i', data)[0]


MAGIC = b'PYDEARKV'


class BinSetting:
    def __init__(self, path: pathlib.Path) -> None:
        super().__init__()
        self.path = path
        self.data: Dict[str, bytes] = {}
        self.load()

    def save(self):
        LOGGER.debug(f'TomlSetting:save: {self.path}')
        with self.path.open('wb') as w:
            w.write(MAGIC)
            for k, v in self.data.items():
                # key
                key_bytes = k.encode('utf-8')
                w.write(struct.pack('i', len(key_bytes)))
                w.write(key_bytes)
                # value
                w.write(struct.pack('i', len(v)))
                w.write(v)

    def load(self):
        if self.path.exists():
            try:
                data = self.path.read_bytes()
                LOGGER.debug(f'BinSetting:load')
                r = BinReader(data)
                assert r.bytes(8) == MAGIC
                while not r.is_end():
                    key_size = r.int32()
                    key = r.str(key_size, encoding='utf-8')
                    value_size = r.int32()
                    value = r.bytes(value_size)
                    self.data[key] = value
            except:
                LOGGER.warn('fail to read settings')

    def __setitem__(self, key: str, data: bytes):
        LOGGER.debug(f'FileSetting:save')
        assert isinstance(data, bytes)
        self.data[key] = data

    def __getitem__(self, key: str) -> Optional[bytes]:
        LOGGER.debug(f'FileSetting:load')
        return self.data.get(key)
