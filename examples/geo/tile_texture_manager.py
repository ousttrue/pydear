from typing import Dict, Optional, NamedTuple, List, Union
import asyncio
import aiohttp
import pathlib
import io
import urllib.parse
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import logging
#
from xyztile import Tile
from pydear import glo

logger = logging.getLogger(__name__)


class ImageTask(NamedTuple):
    tile: Tile
    task: asyncio.Future


class TileTextureManager:
    def __init__(self, loop: asyncio.AbstractEventLoop, base_url: str, cache_dir: pathlib.Path) -> None:
        self.loop = loop
        self.base_url = base_url
        self.texture_map: Dict[Tile, Union[glo.Texture, asyncio.Future]] = {}
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.queue: List[ImageTask] = []
        # start loader
        self.loop.create_task(self.async_loader())

    async def async_loader(self):
        while True:
            if self.queue:
                task = self.queue.pop(0)
                url = f'{self.base_url}/{task.tile.z}/{task.tile.x}/{task.tile.y}.png'
                logger.debug(f'get: {url}')
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"}) as response:
                        match response.status:
                            case 200:
                                data = await response.read()
                                self.save_cache(task.tile, data)
                                img = PIL.Image.open(io.BytesIO(data))
                                task.task.set_result(img)

                            case _:
                                img = self.tmp_image(task.tile)
                                task.task.set_result(img)

            await asyncio.sleep(0.5)

    async def create_texture_async(self, tile: Tile):
        image = await self.create_img_async(tile)
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        texture = glo.Texture(
            image.width, image.height,  image.tobytes('raw'))
        self.texture_map[tile] = texture

    def tmp_image(self, tile: Tile) -> PIL.Image.Image:
        img = PIL.Image.new("RGBA", (256, 256))
        draw = PIL.ImageDraw.Draw(img)
        font = PIL.ImageFont.truetype("verdana.ttf", 24)
        draw.text((0, 0), f"[{tile.z}]{tile.x}:{tile.y}",
                  font=font, fill=(255, 0, 0, 255))
        return img

    async def create_img_async(self, tile: Tile) -> PIL.Image.Image:
        if self.base_url:
            data = self.get_cache(tile)
            if data:
                return PIL.Image.open(io.BytesIO(data))
            return await self.create_task(tile)
        else:
            return self.tmp_image(tile)

    def create_task(self, tile: Tile) -> asyncio.Future:
        task = self.loop.create_future()
        self.queue.append(ImageTask(tile, task))
        self.texture_map[tile] = task
        return task

    def get_or_enqueue(self, tile: Tile) -> Optional[glo.Texture]:
        match self.texture_map.get(tile):
            case glo.Texture() as texture:
                return texture
            case asyncio.Future():
                pass
            case None:
                self.loop.create_task(self.create_texture_async(tile))

    def get_cache_path(self, tile: Tile) -> pathlib.Path:
        url = urllib.parse.urlparse(self.base_url)
        return self.cache_dir / \
            f'{url.hostname}/{url.path}/{tile.z}/{tile.x}/{tile.y}.png'

    def get_cache(self, tile) -> Optional[bytes]:
        path = self.get_cache_path(tile)
        if path.exists():
            return path.read_bytes()

    def save_cache(self, tile, data):
        path = self.get_cache_path(tile)
        logger.debug(f'save: {tile} => {path}')
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
