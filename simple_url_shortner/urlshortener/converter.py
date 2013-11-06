# Based on http://code.activestate.com/recipes/111286/

_DECIMALS = '0123456789'
_B62CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'

def encode(i):
    '''
    Encode an integer in a base62 string.
    '''
    return _convert(i, _DECIMALS, _B62CHARS)

def decode(s):
    '''
    Decode an base62 string in a decimal integer.
    '''
    return int(_convert(s, _B62CHARS, _DECIMALS))

def _convert(number, fromdigits, todigits):
    x = 0
    for digit in str(number):
        x = x * len(fromdigits) + fromdigits.index(digit)

    res = ''
    if x == 0:
        return todigits[0]
    while x > 0:
        digit = x % len(todigits)
        res = todigits[digit] + res
        x = int(x / len(todigits))
    return res
