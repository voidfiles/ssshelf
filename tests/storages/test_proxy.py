from unittest.mock import create_autospec

import pytest

from ssshelf.storages.proxy import StorageProxy
from ssshelf.storages.inmemory import InMemoryStorage
from ssshelf.keys import IndexKey, PrefixKey

@pytest.mark.asyncio
async def test_storage_proxy():
    in_memory = InMemoryStorage()

    storage_proxy = StorageProxy(in_memory)

    await storage_proxy.create_key(IndexKey('a'), 'b')
    assert in_memory.t['a'] == 'b'
    assert 'b' == (await storage_proxy.get_key(IndexKey('a')))['data']
    await storage_proxy.remove_key(IndexKey('a'))
    assert 'a' not in in_memory.t
    await storage_proxy.create_key(IndexKey('a'), 'b')
    await storage_proxy.create_key(IndexKey('d'), 'c')
    assert 'a' in in_memory.t
    assert 'd' in in_memory.t
    await storage_proxy.remove_keys([IndexKey('a'), IndexKey('d')])
    assert 'a' not in in_memory.t
    assert 'd' not in in_memory.t

    await storage_proxy.create_key(IndexKey('a1'), 'b')
    await storage_proxy.create_key(IndexKey('a2'), 'c')

    blah = await storage_proxy.get_keys(PrefixKey(['a']))

    assert 'keys' in blah
    assert len(blah['keys']) == 2
    assert IndexKey(pk='a1', index_parts=[]) in blah['keys']
    assert IndexKey(pk='a2', index_parts=[]) in blah['keys']
