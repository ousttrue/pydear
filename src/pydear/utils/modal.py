MODALS = []


def push(modal):
    MODALS.append(modal)


def remove(modal):
    MODALS.remove(modal)


def show():
    for modal in MODALS:
        modal()
