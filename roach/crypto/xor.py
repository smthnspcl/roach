# Copyright (C) 2018 Jurriaan Bremer.
# This file is part of Roach - https://github.com/jbremer/roach.
# See the file 'docs/LICENSE.txt' for copying permission.

import six

def xor(key, data):
    if not isinstance(data, six.string_types):
        raise RuntimeError("data value must be a string!")

    if isinstance(key, six.integer_types):
        key = chr(key)

    return "".join(
        chr(ord(data[x]) ^ ord(key[x % len(key)])) for x in range(len(data))
    )
