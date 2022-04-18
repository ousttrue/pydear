def empty(*args):
    pass


class Item:
    def __init__(self, name) -> None:
        self.name = name

    def render(self, camera):
        pass

    def show(self):
        pass
