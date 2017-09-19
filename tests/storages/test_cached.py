from ssshelf.storages.cached import ReadCacheInMemory
from ssshelf.storages.inmemory import InMemoryStorage


def test_read_cache(loop):
    in_memory_store = InMemoryStorage()
    read_cached_store = ReadCacheInMemory(in_memory_store)

    loop.run_until_complete(read_cached_store.create_key('a', 'b'))

    assert loop.run_until_complete(in_memory_store.get_key('a'))['data'] == 'b'
    assert loop.run_until_complete(read_cached_store.get_key('a'))['data'] == 'b'
    assert 'a' in read_cached_store._cache
    assert read_cached_store._cache['a']['data'] == 'b'
