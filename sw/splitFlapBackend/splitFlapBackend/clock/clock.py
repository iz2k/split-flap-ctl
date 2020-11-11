from splitFlapBackend.splitFlap.splitFlap import SplitFlap


class clock:

    hh = SplitFlap(i2cAddress=0x16, nFlaps=24)
    mm = SplitFlap(i2cAddress=0x17, nFlaps=60)