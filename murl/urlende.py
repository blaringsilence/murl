#!/usr/bin/env python3
import re

# This module %-encodes and decodes parts of URIs, as well as deals 
# with templating

SAFE_CHARS = 'ABCDEFGHIJKLMNOPQRSTUVWSYZ' \
            +'abcdefghijklmnopqrstuvwxyz0192837465-._~'

def encode(part, safe='/'):
# Assume we're encoding a path, so by default the safe parameter = /
# When encoding a string with certain reserved chars, include in safe
    part = part.replace('%', '%25') # so nothing gets encoded twice
    total_safe = safe + SAFE_CHARS + '%'
    for i in range(256):
        c = chr(i)
        if c not in total_safe and c in part:
            code = ('%%%02X' % i)
            part = part.replace(c, code)
    return part

def encode_query(part, plus=True, safe=''):
# Plus = True when space = + rather than '%20'
# We can use encode right away for '%20' but why not both
    part = encode(part, safe=safe+' ')
    spaceReplace = '+' if plus else '%20'
    part = part.replace(' ', spaceReplace)
    return part

def decode(part):
    all_parts = part.split('%')
    part_list = all_parts[1:]
    res = [all_parts[0]]
    for piece in part_list:
        possible_code = piece[:2]
        rest = piece[2:]
        i = int(possible_code, 16)
        add = chr(i) if i >= 0 and i < 256 else '%' + possible_code
        res.append(add + rest)
    return ''.join(res)

def decode_query(part, plus=True):
    if plus:
        part = part.replace('+', ' ')
    part = decode(part)
    return part

def template_vars(part):
    return re.match(r'\{(\d|\s|\w)+\}', part)