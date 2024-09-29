import os
import re
import struct

RegexpNameSpecialChar = re.compile(r"[^a-z0-9]")
RegexpLabelSpecialChar = re.compile(r"[^a-z0-9A-Z-_\.]")
RegexpLabelPrefix = re.compile(r"^[^a-z0-9A-Z]*")
RegexpLabelSuffix = re.compile(r"[^a-z0-9A-Z-_\.]*[^a-z0-9A-Z]*$")


def resolve_flag(curr, env_var, def_val):
    return curr if curr else os.getenv(env_var, def_val)


def resolve_flag_bool(curr, env_var, def_val):
    return curr if curr != def_val else bool(os.getenv(env_var, def_val))


def resolve_flag_int(curr, env_var, def_val):
    return curr if curr != def_val else int(os.getenv(env_var, def_val))


def check_required_flag(n, p):
    if not p:
        raise ValueError(f'The flag "{n}" is required.')


@staticmethod
def env_def(name, def_val):
    return os.getenv(name, def_val)


def uint_to_byte_array(i):
    return struct.pack("Q", i)


def byte_array_to_uint(b):
    return struct.unpack("Q", b)[0]


def short_hash(incoming_hash):
    return incoming_hash[:7] if len(incoming_hash) >= 7 else ""


@staticmethod
def first(*strs):
    return next((s for s in strs if s), "")


def clean_name(name):
    cleaned = os.path.basename(name).lower()
    cleaned = RegexpNameSpecialChar.sub("-", cleaned).strip("-")
    return cleaned[:63]


def is_valid_name(name):
    return name == clean_name(name)


def clean_label(value):
    cleaned = os.path.basename(str(value))
    cleaned = RegexpLabelSpecialChar.sub("-", cleaned)
    cleaned = RegexpLabelPrefix.sub("", cleaned)
    cleaned = RegexpLabelSuffix.sub("", cleaned)
    return cleaned


def join(sep, *elems):
    return sep.join(filter(None, elems))


def set_bit(n, pos):
    return n | (1 << pos)


def clear_bit(n, pos):
    return n & ~(1 << pos)


def has_bit(n, pos):
    return (n & (1 << pos)) > 0
