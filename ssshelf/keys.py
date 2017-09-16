import string

ALPHABET = string.ascii_uppercase + string.ascii_lowercase
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)


def encode_int_as_str(n):
    s = []

    while True:
        n, r = divmod(n, BASE)
        s.append(ALPHABET[r])
        if n == 0:
            break

    return ''.join(reversed(s))


def decode_str_as_int(s):
    n = 0

    for c in s:
        n = n * BASE + ALPHABET_REVERSE[c]

    return n


def reverse(s):
    n = []
    for i in s:
        ind = ALPHABET.index(i)
        new_ind = len(ALPHABET) - ind - 1
        n += [ALPHABET[new_ind]]

    return ''.join(n)
