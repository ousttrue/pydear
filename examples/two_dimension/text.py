from typing import NamedTuple, Dict
import string
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont


class Letter(NamedTuple):
    letter: str
    x: int
    y: int
    ox: int
    oy: int
    w: int
    h: int
    size: int

    @property
    def width(self):
        return self.ox+self.w


class AsciiLetters:
    def __init__(self, fontfile: str, fontsize: int, w: int, h: int, padding: int) -> None:
        self.padding = padding
        self.fontsize = fontsize
        self.img = PIL.Image.new("RGB", (w, h))
        self.draw = PIL.ImageDraw.Draw(self.img)
        self.font = PIL.ImageFont.truetype(fontfile, fontsize)
        self.x = 0
        self.y = 0
        self.letters: Dict[str, Letter] = {}

    @staticmethod
    def create(fontfile: str, fontsize: int, w: int, h: int, padding: int, box=False):
        image = AsciiLetters(fontfile, fontsize, w, h, padding)
        for letter in string.digits:
            image.write_letter(letter, box)
        for letter in string.ascii_letters:
            image.write_letter(letter, box)
        for letter in string.punctuation:
            image.write_letter(letter, box)
        return image

    def write_letter(self, l, write_box: bool = False):
        bbox = self.draw.textbbox((self.x, self.y), l, font=self.font)
        letter = Letter(
            l, self.x, self.y, bbox[0]-self.x, bbox[1]-self.y, bbox[2]-bbox[0], bbox[3]-bbox[1], self.fontsize)

        assert(letter.oy + letter.h <= self.fontsize + self.padding)

        if bbox[2] > self.img.width:
            self.x = 0
            self.y += self.fontsize + self.padding

        self.letters[l] = letter

        self.draw.text((self.x, self.y), l, font=self.font)

        if write_box:
            self.draw.rectangle(bbox, fill=None, outline=(255, 0, 0))

        # advance
        self.x += letter.width + self.padding

    def save(self, name):
        self.img.save(name)


if __name__ == '__main__':
    image = AsciiLetters.create("DejaVuSans.ttf", 10, 256, 64, 2)
    image.save('tmp.png')
    print(image.letters)
