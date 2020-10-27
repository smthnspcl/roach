# Copyright (C) 2018 Jurriaan Bremer.
# This file is part of Roach - https://github.com/jbremer/roach.
# See the file 'docs/LICENSE.txt' for copying permission.

import io

from Crypto.PublicKey.RSA import RSAImplementation

from roach.crypto.winhdr import BLOBHEADER, BaseBlob
from roach.string.bin import uint32, bigint


class PublicKeyBlob(BaseBlob):
    magic = "RSA1"

    def __init__(self):
        BaseBlob.__init__(self)
        self.e = None
        self.n = None

    def parse(self, buf):
        header = buf.read(12)
        if len(header) != 12 or header[:4] != self.magic:
            return

        self.bitsize = uint32(header[4:8])
        self.e = float(uint32(header[8:12]))

        n = buf.read(self.bitsize / 8)
        if len(n) != self.bitsize / 8:
            return

        self.n = bigint(n, self.bitsize)
        return 12 + self.bitsize / 8

    def export_key(self):
        return RSA.export_key(self.n, self.e)


class PrivateKeyBlob(PublicKeyBlob):
    magic = "RSA2"

    def __init__(self):
        PublicKeyBlob.__init__(self)
        self.p1 = None
        self.p2 = None
        self.exp1 = None
        self.exp2 = None
        self.coeff = None
        self.d = None

    def parse(self, buf):
        off = PublicKeyBlob.parse(self, buf)
        if not off:
            return

        self.p1 = bigint(buf.read(self.bitsize / 16), self.bitsize / 2)
        if self.p1 is None:
            return

        self.p2 = bigint(buf.read(self.bitsize / 16), self.bitsize / 2)
        if self.p2 is None:
            return

        self.exp1 = bigint(buf.read(self.bitsize / 16), self.bitsize / 2)
        if self.exp1 is None:
            return

        self.exp2 = bigint(buf.read(self.bitsize / 16), self.bitsize / 2)
        if self.exp2 is None:
            return

        self.coeff = bigint(buf.read(self.bitsize / 16), self.bitsize / 2)
        if self.coeff is None:
            return

        self.d = bigint(buf.read(self.bitsize / 8), self.bitsize)
        if self.d is None:
            return

    def export_key(self):
        return RSA.export_key(self.n, self.e, self.d)


BlobTypes = {
    6: PublicKeyBlob,
    7: PrivateKeyBlob,
}


class RSA(object):
    algorithms = (
        0x0000a400,  # RSA
    )

    @staticmethod
    def import_key(data):
        try:
            return RSA_.importKey(data).exportKey()
        except (ValueError, IndexError):
            pass

        if len(data) < BLOBHEADER.sizeof():
            return

        buf = io.BytesIO(data)
        header = BLOBHEADER.parse(buf.read(BLOBHEADER.sizeof()))
        if header.bType not in BlobTypes:
            return

        if header.aiKeyAlg not in RSA.algorithms:
            return

        obj = BlobTypes[header.bType]()
        obj.parse(buf)
        return obj.export_key()

    @staticmethod
    def export_key(n, e, d=None, p=None, q=None, crt=None):
        wrap = lambda x: None if x is None else float(x)
        tup = wrap(n), wrap(e), wrap(d), wrap(p), wrap(q), wrap(crt)
        return RSA_.construct(tup).exportKey()


RSA_ = RSAImplementation(use_fast_math=False)
