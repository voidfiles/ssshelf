import attr
import string
from .utils import build_url_path, parse_url_path

ALPHABET = string.ascii_uppercase + string.ascii_lowercase
ALPHABET_REVERSE = dict((c, i) for (i, c) in enumerate(ALPHABET))
BASE = len(ALPHABET)


@attr.s
class IndexKey(object):
    pk = attr.ib()
    index_parts = attr.ib(default=attr.Factory(list))

    def as_url_path(self):
        url_parts = self.index_parts + [self.pk]

        return build_url_path(url_parts)

    @classmethod
    def from_url_path(cls, path):
        url_parts = parse_url_path(path)
        pk = url_parts.pop()

        return cls(pk, url_parts)

@attr.s
class PrefixKey(object):
    index_parts = attr.ib()

    def as_url_path(self):
        url_parts = self.index_parts

        return build_url_path(url_parts)


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
