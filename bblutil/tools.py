from struct import pack, unpack

def toint32(word):
    return unpack('i', pack('I', word))[0]


def sign_extend_24bit(bits: int):
    return toint32(bits | 0xFF000000) if bits & 0x800000 else bits


def sign_extend_16bit(word: int):
    return toint32(word | 0xFFFF0000) if word & 0x8000 else word


def sign_extend_14bit(word: int):
    return toint32(word | 0xFFFFC000) if word & 0x2000 else word


def sign_extend_8bit(byte: int):
    return toint32(byte | 0xFFFFFF00) if byte & 0x80 else byte


def sign_extend_7bit(byte: int):
    return toint32(byte | 0xFFFFFF80) if byte & 0x40 else byte


def sign_extend_6bit(byte: int):
    return toint32(byte | 0xFFFFFFC0) if byte & 0x20 else byte


def sign_extend_5bit(byte: int):
    return toint32(byte | 0xFFFFFFE0) if byte & 0x10 else byte


def sign_extend_4bit(nibble: int):
    return toint32(nibble | 0xFFFFFFF0) if nibble & 0x08 else nibble


def sign_extend_2bit(byte: int) -> int:
    return toint32(byte | 0xFFFFFFFC) if byte & 0x02 else byte

