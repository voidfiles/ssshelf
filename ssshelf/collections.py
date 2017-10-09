"""
Collections
-----------

Collections allow you to put items into
queryable ordered lists.

"""

from .utils import RAISE_NOT_IMPLEMENTED, camelcase_to_dash, build_url_path
from .keys import IndexKey, PrefixKey

class Collection(object):

    key = RAISE_NOT_IMPLEMENTED

    def __init__(self, storage=None, prefix='collections', name=None, item_manager=None):
        self.prefix = prefix
        self.storage = storage
        self.name = name if name else camelcase_to_dash(self.__class__.__name__)
        self.item_manager = item_manager

    def set_storage(self, storage):
        self.storage = storage

    def set_item_manager(self, item_manager):
        self.item_manager = item_manager

    def get_pk(self, item):
        return str(item.pk)

    def parse_pk_from_key(self, key):
        return key.pk

    def base_key_parts(self):
        return [self.prefix, self.name]

    def generate_keys_for_item(self, item):
        pk = self.get_pk(item)

        for key in self.key(item):
            if not key:
                continue

            key_parts = self.base_key_parts()
            key_parts += key

            yield IndexKey(pk, key_parts)

    async def add_item(self, item):
        keys = []
        reqs = []
        for storage_key in self.generate_keys_for_item(item):
            keys += [storage_key]
            reqs += [self.storage.create_key(storage_key)]

        resps = [await x for x in reqs]

        return keys

    async def remove_item(self, item):
        keys = []
        reqs = []
        for storage_key in self.generate_keys_for_item(item):
            keys += [storage_key]
            reqs += [self.storage.remove_key(storage_key)]

        resps = [await x for x in reqs]

        return keys

    async def get_keys(self, max_keys=200, after=None, prefix_parts=None):
        prefix_parts = prefix_parts if prefix_parts else []

        resp = await self.storage.get_keys(
            prefix=PrefixKey(self.base_key_parts() + prefix_parts),
            max_keys=max_keys,
            after=after
        )

        resp['keys'] = [self.parse_pk_from_key(x) for x in resp['keys']]

        return resp

    async def get_items(self, max_keys=200, after=None, prefix_parts=None):

        resp = await self.get_keys(
            max_keys=max_keys,
            after=after,
            prefix_parts=prefix_parts,
        )

        reqs = [self.item_manager.get_item(x) for x in resp['keys']]

        items = [await req for req in reqs]

        ret = {
            'items': items,
        }

        if 'after' in resp:
            ret['after'] = resp['after']

        return ret
