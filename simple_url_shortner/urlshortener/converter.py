# -*- coding: utf-8 -*-

CHARS = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHUJKLMNOPQRSTUVWXYZ'

def num_to_base62(n):
    '''
    Convert a decimal number in a base62 (decimals + lower + uppercase letters)
    '''
    if (n >= 62):
        return num_to_base62(int(n / 62.)) + CHARS[n % 62]
    else:
        return CHARS[n]
