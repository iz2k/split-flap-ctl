from babel.util import get_localzone

from splitFlapBackend.splitFlap.splitFlap import SplitFlap


class Clock:

    hh = SplitFlap(i2cAddress=0x16, nFlaps=24)
    mm = SplitFlap(i2cAddress=0x17, nFlaps=60)

    mode = 'clock'

    timezone = None

    def __init__(self):
        self.timezone = get_localzone()