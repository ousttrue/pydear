def empty(*args):
    pass


class Item:
    def __init__(self, name) -> None:
        self.name = name

    def render(self, w, h):
        pass

    def show(self):
        pass

    def drag(self, x, y, dx, dy, left, right, middle):
        pass

    def input(self, wheel):
        pass
