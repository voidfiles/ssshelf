
class StorageProxy(object):
    def __init__(self, storage):
        self.storage = storage

    async def create_key(self, storage_key, data=None):
        return await self.storage.create_key(storage_key, data)

    async def remove_key(self, storage_key):
        await self.storage.remove_key(storage_key)

    async def remove_keys(self, storage_keys):
        await self.storage.remove_keys(storage_keys)

    async def get_key(self, storage_key):
        return await self.storage.get_key(storage_key)

    async def get_keys(self, *args, **kwargs):
        return await self.storage.get_keys(*args, **kwargs)
