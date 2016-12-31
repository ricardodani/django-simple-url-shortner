# -*- coding: utf-8 -*-

import string
CHARS = string.digits + string.ascii_letters

def num_to_base62(n):
    '''
    Convert a decimal number in a base62 (digits + lower & uppercase letters)
    '''
    if (n >= 62):
        return num_to_base62(int(n / 62.)) + CHARS[n % 62]
    else:
        return CHARS[n]
