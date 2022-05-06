import ctypes


def create_font_range() -> ctypes.Array:

    # font load
    # https://github.com/ryanoasis/nerd-fonts/wiki/Glyph-Sets-and-Code-Points
    range = []

    def push_range(*values):
        match values:
            case (value,):
                range.append(value)
                range.append(value)
            case (v0, v1):
                range.append(v0)
                range.append(v1)
            case _:
                raise NotImplementedError()
    push_range(0x23fb, 0x23fe)  # IEC Power Symbols
    push_range(0x2665)  # Octicons
    push_range(0x26a1)  # Octicons
    push_range(0x2b58)  # IEC Power Symbols
    push_range(0xe000, 0xe00a)  # Pomicons
    push_range(0xe0a0, 0xe0a2)  # Powerline
    push_range(0xe0a3)  # Powerline Extra
    push_range(0xe0b0, 0xe0b3)  # Powerline
    push_range(0xe0b4, 0xe0c8)  # Powerline Extra
    push_range(0xe0b4, 0xe0c8)  # Powerline Extrax
    push_range(0xe0cc, 0xe0d4)  # Powerline Extra
    push_range(0xe200, 0xe2a9)  # Font Awesome Extension
    push_range(0xe300, 0xe3eb)  # Weather Icons
    push_range(0xe5fa, 0xe631)  # Seti-UI + Custom
    push_range(0xe700, 0xe7c5)  # Devicons
    push_range(0xea60, 0xebeb)  # Codicons
    push_range(0xf000, 0xf2e0)  # Font Awesome
    push_range(0xf300, 0xf32d)  # Font Logos
    push_range(0xf400, 0xf4a8)  # Octicons
    push_range(0xf4a9)  # Octicons
    push_range(0xf500, 0xfd46)  # Material Design

    return (ctypes.c_ushort * (len(range)+1))(*range, 0)
