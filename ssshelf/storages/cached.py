import pygtrie

from .proxy import StorageProxy

class ReadKeyCacheInMemory(StorageProxy):
    def __init__(self, storage):
        super(ReadKeyCacheInMemory, self).__init__(storage)
        self._cache = {}

    async def create_key(self, storage_key, data=None):
        data = await self.storage.create_key(storage_key, data)
        self._cache[storage_key.as_url_path()] = {
            'data': data,
        }
        return data

    async def remove_key(self, storage_key):
        await self.storage.remove_key(storage_key)
        del self._cache[storage_key.as_url_path()]

    async def remove_keys(self, storage_keys):
        await self.storage.remove_keys(storage_keys)
        for x in storage_keys:
            if x.as_url_path() in self._cache:
                del self._cache[x.as_url_path()]

    async def get_key(self, storage_key):
        if storage_key.as_url_path() not in self._cache:
            resp = await self.storage.get_key(storage_key)
            self._cache[storage_key.as_url_path()] = resp

        return self._cache[storage_key.as_url_path()]
