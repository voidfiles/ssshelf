"""
SSShelf Collections

A collections is an ordered list of items by an attribute

When you create a collection you must configure the pk attribute, and the order attribute.

The order attribute will determine where in the list the item falls.
The pk attribute is how you will look of the object.
"""
from .utils import RAISE_NOT_IMPLEMENTED, build_url_path, camelcase_to_dash


class Collection(object):

    key = RAISE_NOT_IMPLEMENTED
    prefix = 'collections'

    @property
    def name(self):
        return camelcase_to_dash(self.__class__.__name__)

    def get_pk(self, item):
        return str(item.pk)

    def parse_pk_from_key(self, key):
        return key.split('/')[-1]

    def base_key_parts(self):
        return [self.prefix, self.name]

    def generate_keys_for_item(self, item):
        pk = self.get_pk(item)

        for key in self.key(item):
            key_parts = self.base_key_parts()
            key_parts += key
            key_parts += [pk]

            yield build_url_path(key_parts)

    async def add_item(self, item, storage):
        keys = []
        reqs = []
        for storage_key in self.generate_keys_for_item(item):
            keys += [storage_key]
            reqs += [storage.create_key(storage_key)]

        resps = [await x for x in reqs]

        return keys

    async def remove_item(self, item, storage):
        keys = []
        reqs = []
        for storage_key in self.generate_keys_for_item(item):
            keys += [storage_key]
            reqs += [storage.remove_key(storage_key)]

        resps = [await x for x in reqs]

        return keys

    async def get_items(self, max_keys=200, continuation_token=None, storage=None):

        resp = await storage.get_keys(
            prefix=build_url_path(self.base_key_parts()),
            max_keys=max_keys,
            continuation_token=continuation_token
        )

        resp['keys'] = [self.parse_pk_from_key(x) for x in resp['keys']]

        return resp
