import pytest

from ssshelf.storages.cached import ReadCacheInMemory
from ssshelf.storages.inmemory import InMemoryStorage

"""
    async def create_key(self, *args, **kwargs):
        await self.storage.create_key(*args, **kwargs)

    async def remove_key(self, storage_key):
        await self.storage.remove_key(storage_key)
        del self._cache[storage_key]

    async def remove_keys(self, storage_keys):
        await self.storage.remove_keys(storages_keys)
        for x in storages_keys:
            del self._cache[x]

    async def get_key(self, storage_key):
        if storage_key not in self._cache:
            resp = await self.storage.get_key(storage_key)
            self._cache[storage_key] = resp

        return self._cache[storage_key]

    async def get_keys(self, *args, **kwargs):
        return await self.storage.get_keys(*args, **kwargs)
"""


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
