from .utils import RAISE_NOT_IMPLEMENTED


class Manager(object):
    item_class = RAISE_NOT_IMPLEMENTED

    def __init__(self):
        self._collections = {}

    def add_collection(self, name, collection):
        self._collections[name] = collection
        setattr(self, name, collection)

    async def add_item(self, item):
        awaitable_resps = {}
        for name, collection in self.collections.items():
            awaitable_resps[name] = collection.add_item(item)

        resps = {}
        for name, resp in awaitable_resps.items():
            resps[name] = await resp

        return resps

    async def remove_item(self, item):
        awaitable_resps = {}
        for name, collection in self.collections.items():
            awaitable_resps[name] = collection.remove_item(item)

        resps = {}
        for name, resp in awaitable_resps.items():
            resps[name] = await resp

        return resps
