from .proxy import StorageProxy
from ssshelf.keys import get_path_from_storage_key

class ReadCacheInMemory(StorageProxy):
    def __init__(self, storage):
        super(ReadCacheInMemory, self).__init__(storage)
        self._cache = {}

    async def create_key(self, storage_key, data=None):
        data = await self.storage.create_key(storage_key, data)
        storage_key = get_path_from_storage_key(storage_key)
        self._cache[storage_key] = {
            'data': data,
        }
        return data

    async def remove_key(self, storage_key):
        await self.storage.remove_key(storage_key)
        storage_key = get_path_from_storage_key(storage_key)
        del self._cache[storage_key]

    async def remove_keys(self, storage_keys):
        await self.storage.remove_keys(storage_keys)
        storage_keys = [get_path_from_storage_key(x) for x in storage_keys]
        for x in storage_keys:
            if x in self._cache:
                del self._cache[x]

    async def get_key(self, storage_key):
        storage_key = get_path_from_storage_key(storage_key)
        if storage_key not in self._cache:
            resp = await self.storage.get_key(storage_key)
            self._cache[storage_key] = resp

        return self._cache[storage_key]
