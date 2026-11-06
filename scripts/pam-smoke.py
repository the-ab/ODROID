# SPDX-License-Identifier: GPL-2.0-only
"""Exercise the image's real ARM PAM rules without opening a login session."""
import ctypes as c
from pathlib import Path
if not __debug__:raise SystemExit('Run without Python optimization: validation must remain enabled')

stored = next(line.split(':')[1] for line in Path('/etc/shadow').read_text().splitlines()
              if line.startswith('odroid:'))
crypt = c.CDLL('libcrypt.so.1')
crypt.crypt.argtypes = [c.c_char_p, c.c_char_p]
crypt.crypt.restype = c.c_char_p
assert crypt.crypt(b'odroid', stored.encode()) == stored.encode()
assert crypt.crypt(b'not-the-default-password', stored.encode()) != stored.encode()
print('Default odroid password matches Unix hash; wrong password rejected', flush=True)

pam = c.CDLL("libpam.so.0")
libc = c.CDLL(None)
libc.calloc.argtypes = [c.c_size_t, c.c_size_t]
libc.calloc.restype = c.c_void_p
libc.strdup.argtypes = [c.c_char_p]
libc.strdup.restype = c.c_void_p


class Message(c.Structure):
    _fields_ = [("style", c.c_int), ("text", c.c_char_p)]


class Response(c.Structure):
    _fields_ = [("text", c.c_void_p), ("code", c.c_int)]


Callback = c.CFUNCTYPE(c.c_int, c.c_int, c.POINTER(c.POINTER(Message)),
                      c.POINTER(c.POINTER(Response)), c.c_void_p)


@Callback
def conversation(count, messages, responses, data):
    memory = libc.calloc(count, c.sizeof(Response))
    if not memory:
        return 19
    array = c.cast(memory, c.POINTER(Response))
    for index in range(count):
        style = messages[index].contents.style
        if style in (1, 2):
            array[index].text = libc.strdup(b"odroid")
        elif style not in (3, 4):
            return 19
    responses[0] = array
    return 0


class Conversation(c.Structure):
    _fields_ = [("callback", Callback), ("data", c.c_void_p)]


pam.pam_start.argtypes = [c.c_char_p, c.c_char_p, c.POINTER(Conversation), c.POINTER(c.c_void_p)]
pam.pam_authenticate.argtypes = [c.c_void_p, c.c_int]
pam.pam_acct_mgmt.argtypes = [c.c_void_p, c.c_int]
pam.pam_end.argtypes = [c.c_void_p, c.c_int]
conv = Conversation(conversation, None)
for service in (b"login", b"sshd", b"sudo"):
    handle = c.c_void_p()
    status = pam.pam_start(service, b"odroid", c.byref(conv), c.byref(handle))
    assert status == 0, (service, "start", status)
    try:
        status = pam.pam_authenticate(handle, 0)
        assert status == 0, (service, "authentication", status)
        status = pam.pam_acct_mgmt(handle, 0)
        assert status == 0, (service, "account", status)
    finally:
        pam.pam_end(handle, status)
    print(service.decode(), "ARM PAM authentication and account checks passed", flush=True)
