# Copyright (C) 2018 Jurriaan Bremer.
# This file is part of Roach - https://github.com/jbremer/roach.
# See the file 'docs/LICENSE.txt' for copying permission.

import re
import six
import socket

from roach.string.bin import uint32

ipv4_regex = re.compile(
    b"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}"
    b"([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
)

def ipv4(s):
    if isinstance(s, (bytes, six.string_types)):
        if len(s) == 4:
            return socket.inet_ntoa(s)
        if re.match(ipv4_regex, s):
            return s.decode()
    if isinstance(s, six.integer_types):
        return socket.inet_ntoa(uint32(s)[::-1])
