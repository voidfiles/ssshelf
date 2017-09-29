from unittest.mock import create_autospec

import pytest

from ssshelf.storages.proxy import StorageProxy
from ssshelf.storages.inmemory import InMemoryStorage


@pytest.mark.asyncio
async def test_storage_proxy():
    in_memory = InMemoryStorage()

    storage_proxy = StorageProxy(in_memory)

    await storage_proxy.create_key('a', 'b')
    assert in_memory.t['a'] == 'b'
    assert 'b' == (await storage_proxy.get_key('a'))['data']
    await storage_proxy.remove_key('a')
    assert 'a' not in in_memory.t
    await storage_proxy.create_key('a', 'b')
    await storage_proxy.create_key('d', 'c')
    assert 'a' in in_memory.t
    assert 'd' in in_memory.t
    await storage_proxy.remove_keys(['a', 'd'])
    assert 'a' not in in_memory.t
    assert 'd' not in in_memory.t

    await storage_proxy.create_key('a1', 'b')
    await storage_proxy.create_key('a2', 'c')

    blah = await storage_proxy.get_keys('a')

    assert 'keys' in blah
    assert len(blah['keys']) == 2
    assert 'a1' in blah['keys']
    assert 'a2' in blah['keys']
