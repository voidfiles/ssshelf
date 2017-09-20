
class ReadCacheInMemory(object):
    def __init__(self, storage):
        self.storage = storage
        self._cache = {}

    async def create_key(self, storage_key, data=None):
        data = await self.storage.create_key(storage_key, data)
        self._cache[storage_key] = {
            'data': data,
        }
        return data

    async def remove_key(self, storage_key):
        await self.storage.remove_key(storage_key)
        del self._cache[storage_key]

    async def remove_keys(self, storage_keys):
        await self.storage.remove_keys(storage_keys)
        for x in storage_keys:
            if x in self._cache:
                del self._cache[x]

    async def get_key(self, storage_key):
        if storage_key not in self._cache:
            resp = await self.storage.get_key(storage_key)
            self._cache[storage_key] = resp

        return self._cache[storage_key]

    async def get_keys(self, *args, **kwargs):
        return await self.storage.get_keys(*args, **kwargs)
