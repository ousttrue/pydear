import pathlib
import sys

HERE = pathlib.Path(__file__).absolute().parent

sys.path.append(str(HERE / 'src'))

import pydeer.impl
print(pydeer.impl.CreateContext(None))
