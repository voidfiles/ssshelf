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
