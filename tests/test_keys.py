from ssshelf.keys import (encode_int_as_str, decode_str_as_int,
                          reverse, IndexKey)


def test_encode_int_as_str():
    b = 123
    b_str = encode_int_as_str(b)
    assert decode_str_as_int(b_str) == b


def test_reverse():
    bbb = [
        3,
        2,
        1,
        4,
        5
    ]

    bbb_encoded = [reverse(encode_int_as_str(x)) for x in bbb]

    ccc = list(zip(bbb, bbb_encoded))
    ccc = sorted(ccc, key=lambda x: x[1])

    assert [x[0] for x in ccc] == [5, 4, 3, 2, 1]


def test_index_key():
    a = IndexKey(pk='d', index_parts=['a', 'b', 'c'])
    assert a.as_url_path() == 'a/b/c/d'

    b = IndexKey.from_url_path('a/b/c/d')

    assert a == b
