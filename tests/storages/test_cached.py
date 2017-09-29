import pytest

from ssshelf.storages.cached import ReadCacheInMemory
from ssshelf.storages.inmemory import InMemoryStorage


@pytest.mark.asyncio
async def test_read_cache():
    in_memory_store = InMemoryStorage()
    read_cached_store = ReadCacheInMemory(in_memory_store)

    await read_cached_store.create_key('a', 'b')
    assert 'a' in read_cached_store._cache

    assert (await in_memory_store.get_key('a'))['data'] == 'b'
    assert (await read_cached_store.get_key('a'))['data'] == 'b'
    assert 'a' in read_cached_store._cache
    assert read_cached_store._cache['a']['data'] == 'b'

    await read_cached_store.remove_key('a')
    assert 'a' not in read_cached_store._cache

    await read_cached_store.create_key('a1', 'b')
    await read_cached_store.create_key('a2', 'd')

    resp = await read_cached_store.get_keys(prefix='a')
    assert len(resp['keys']) == 2

    await read_cached_store.get_key('a1')
    await read_cached_store.get_key('a2')
    assert 'a1' in read_cached_store._cache
    assert 'a2' in read_cached_store._cache
    await read_cached_store.remove_keys(['a1', 'a2'])
    assert 'a1' not in read_cached_store._cache
    assert 'a2' not in read_cached_store._cache

    resp = await read_cached_store.get_key('b2')
    assert resp['data'] is None
