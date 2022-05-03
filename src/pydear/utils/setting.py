from typing import Optional, Dict
import logging
import abc
import pathlib
import toml

LOGGER = logging.getLogger(__name__)


class SettingInterface(abc.ABC):
    @abc.abstractmethod
    def save(self, data: bytes):
        pass

    @abc.abstractmethod
    def load(self) -> Optional[bytes]:
        pass


class FileSetting(SettingInterface):
    def __init__(self, path: pathlib.Path) -> None:
        super().__init__()
        self.path = path

    def save(self, data: bytes):
        LOGGER.debug(f'FileSetting:save')
        self.path.write_bytes(data)

    def load(self) -> Optional[bytes]:
        LOGGER.debug(f'FileSetting:load')
        if self.path.exists():
            return self.path.read_bytes()


class BytesSetting(SettingInterface):
    def __init__(self, name: str, data=b'', ref=None) -> None:
        super().__init__()
        self.name = name
        self.data = data
        self.ref = ref

    def save(self, data: bytes):
        LOGGER.debug(f'BytesSetting:{self.name}:save')
        self.data = data

    def load(self) -> Optional[bytes]:
        return self.data


class TomlSetting:
    def __init__(self, path: pathlib.Path) -> None:
        super().__init__()
        self.path = path
        self.data: Dict[str, BytesSetting] = {}
        if self.path.exists():
            try:
                data = toml.load(self.path)
                LOGGER.debug(f'TomlSetting:load')
                for k, v in data.items():
                    self.data[k] = BytesSetting(k, v.encode('utf-8'), ref=self)
            except:
                pass

    def save(self):
        LOGGER.debug(f'TomlSetting:save: {self.path}')
        data = {}
        # self.path.write_text(toml.dumps(data), encoding='utf-8')
        with self.path.open('w', encoding='utf-8') as w:
            for k, v in self.data.items():
                value = v.load()
                if value:
                    value = value.decode('utf-8')
                    w.write(f"{k} = '''\n{value}\n'''\n\n")

    def __getitem__(self, key: str) -> BytesSetting:
        value = self.data.get(key)
        if not value:
            value = BytesSetting(key, ref=self)
            self.data[key] = value
        return value
