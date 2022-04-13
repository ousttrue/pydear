def empty(*args):
    pass


class Item:
    def __init__(self, name) -> None:
        self.name = name

    def render(self, w, h):
        pass

    def show(self):
        pass

    def input(self, x, y, dx, dy, left, right, middle, wheel):
        pass
