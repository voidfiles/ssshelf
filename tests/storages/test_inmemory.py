import json
import pytest
from ssshelf.storages.inmemory import InMemoryStorage


def test_my_model_save(loop):
    storage = InMemoryStorage()
    document = {
        "x": "y"
    }

    document_str = bytes(json.dumps(document), 'utf8')
    loop.run_until_complete(storage.create_key('test', data=document_str))

    resp = loop.run_until_complete(storage.get_key('test'))

    body_json = json.loads(resp['data'])

    assert document == body_json

    loop.run_until_complete(storage.remove_key('test'))

    loop.run_until_complete(storage.get_key('test'))


@pytest.mark.moto
def test_multiple_keys(loop):
    storage = InMemoryStorage()
    document = {
        "x": "y"
    }

    document_str = bytes(json.dumps(document), 'utf8')
    for i in range(0, 20):
        loop.run_until_complete(storage.create_key('bulk_test%03d' % (i), data=document_str))

    resp = loop.run_until_complete(storage.get_keys('bulk_test', max_keys=10))

    assert len(resp['keys']) == 10
    for i in range(0, 10):
        assert resp['keys'][i] == 'bulk_test%03d' % (i)

    assert 'continuation_token' in resp
    print(resp)
    resp2 = loop.run_until_complete(
        storage.get_keys('bulk_test', max_keys=10,
                         continuation_token=resp['continuation_token'])
    )
    print(resp2)
    assert len(resp2['keys']) == 10
    for i in range(0, 9):
        assert resp2['keys'][i] == 'bulk_test%03d' % (i + 10)

    assert 'continuation_token' not in resp2

    keys_to_delete = ['bulk_test%03d' % (i) for i in range(0, 20)]

    loop.run_until_complete(storage.remove_keys(keys_to_delete))

    resp3 = loop.run_until_complete(
        storage.get_keys('bulk_test', max_keys=10,
                         continuation_token=resp['continuation_token'])
    )

    assert len(resp3['keys']) == 0
