from pydear.utils.item import Item, Input


class TeaPot(Item):
    def __init__(self) -> None:
        super().__init__('teapot')

    def render(self):
        pass

    def input(self, input: Input):
        pass
