import json
import pytest
from ssshelf.storages.inmemory import InMemoryStorage
from ssshelf.keys import IndexKey, PrefixKey

def test_my_model_save(loop):
    storage = InMemoryStorage()
    document = {
        "x": "y"
    }

    document_str = bytes(json.dumps(document), 'utf8')
    loop.run_until_complete(storage.create_key(IndexKey('test'), data=document_str))

    resp = loop.run_until_complete(storage.get_key(IndexKey('test')))

    body_json = json.loads(resp['data'])

    assert document == body_json

    loop.run_until_complete(storage.remove_key(IndexKey('test')))

    loop.run_until_complete(storage.get_key(IndexKey('test')))


@pytest.mark.moto
def test_multiple_keys(loop):
    storage = InMemoryStorage()
    document = {
        "x": "y"
    }
    keys = sorted([x for x in "abcdefghijklmnopqrst"], reverse=True)
    document_str = bytes(json.dumps(document), 'utf8')
    for i in keys:
        loop.run_until_complete(storage.create_key(
            IndexKey('bulk_test%s' % (i)), data=document_str))

    resp = loop.run_until_complete(
        storage.get_keys(PrefixKey(['bulk_test']), max_keys=10))

    reverse_keys = sorted(keys)
    assert len(resp['keys']) == 10

    for i, key in enumerate(reverse_keys[0:9]):
        assert resp['keys'][i] == IndexKey(pk='bulk_test%s' % (key),
                                           index_parts=[])

    assert 'after' in resp
    print(resp)
    resp2 = loop.run_until_complete(
        storage.get_keys(PrefixKey(['bulk_test']), max_keys=10,
                         after=resp['after'])
    )
    assert len(resp2['keys']) == 10
    for i, key in enumerate(reverse_keys[10:]):
        assert resp2['keys'][i] == IndexKey(pk='bulk_test%s' % (key),
                                            index_parts=[])

    assert 'after' not in resp2
    print(resp2)
    keys_to_delete = [IndexKey('bulk_test%s' % (i)) for i in keys]

    loop.run_until_complete(storage.remove_keys(keys_to_delete))

    resp3 = loop.run_until_complete(
        storage.get_keys(PrefixKey(['bulk_test']), max_keys=10,
                         after=resp['after'])
    )

    assert len(resp3['keys']) == 0
