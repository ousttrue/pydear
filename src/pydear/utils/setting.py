from typing import Optional, Dict
import logging
import abc
import pathlib
import toml

LOGGER = logging.getLogger(__name__)


class SettingInterface(abc.ABC):
    @abc.abstractmethod
    def save(self, key: str, data: bytes):
        pass

    @abc.abstractmethod
    def load(self, key: str) -> Optional[bytes]:
        pass


class FileSetting(SettingInterface):
    def __init__(self, path: pathlib.Path) -> None:
        super().__init__()
        self.path = path

    def save(self, _: str, data: bytes):
        LOGGER.debug(f'FileSetting:save')
        self.path.write_bytes(data)

    def load(self, _: str) -> Optional[bytes]:
        LOGGER.debug(f'FileSetting:load')
        if self.path.exists():
            return self.path.read_bytes()


class TomlSetting(SettingInterface):
    def __init__(self, path: pathlib.Path) -> None:
        super().__init__()
        self.path = path
        self.data: Dict[str, bytes] = {}
        if self.path.exists():
            try:
                data = toml.load(self.path)
                LOGGER.debug(f'TomlSetting:load')
                for k, v in data.items():
                    assert isinstance(v, str)
                    self.data[k] = v.encode('utf-8')
            except:
                pass

    def save(self, key: str, data: bytes):
        LOGGER.debug(f'FileSetting:save')
        self.data[key] = data

    def load(self, key: str) -> Optional[bytes]:
        LOGGER.debug(f'FileSetting:load')
        return self.data.get(key)

    def write(self):
        LOGGER.debug(f'TomlSetting:save: {self.path}')
        data = {}
        # self.path.write_text(toml.dumps(data), encoding='utf-8')
        with self.path.open('w', encoding='utf-8') as w:
            for k, v in self.data.items():
                value = v.decode('utf-8')
                w.write(f"{k} = '''\n{value}\n'''\n\n")
