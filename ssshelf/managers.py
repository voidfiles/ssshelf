from .utils import RAISE_NOT_IMPLEMENTED


class CManager(object):
    item_manager = RAISE_NOT_IMPLEMENTED

    def __init__(self, storage):
        self._collections = {}
        self.storage = storage

    def add_collection(self, name, collection):
        self._collections[name] = collection

    async def add_item(self, item):
        await self.item_manager.add_item(item, self.storage)
        awaitable_resps = {}
        for name, collection in self._collections.items():
            awaitable_resps[name] = collection.add_item(item, self.storage)

        resps = {}
        for name, resp in awaitable_resps.items():
            resps[name] = await resp

        return resps

    async def remove_item(self, item):
        awaitable_resps = {}
        for name, collection in self._collections.items():
            awaitable_resps[name] = collection.remove_item(item, self.storage)

        resps = {}
        for name, resp in awaitable_resps.items():
            resps[name] = await resp

        await self.item_manager.remove_item(item, self.storage)

        return resps

    async def get_items_for_collection(self, name, max_keys=200, continuation_token=None):
        if name not in self._collections:
            raise Exception("No collection by that name: %s" % (name))

        resp = await self._collections[name].get_items(
            max_keys=max_keys,
            continuation_token=continuation_token,
            storage=self.storage
        )

        reqs = [self.item_manager.get_item(x, self.storage) for x in resp['keys']]

        items = [await req for req in reqs]

        ret = {
            'items': items,
        }

        if 'continuation_token' in resp:
            ret['continuation_token'] = resp['continuation_token']

        return ret
