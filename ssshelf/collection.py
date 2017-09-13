"""
SSShelf Collections

A collections is an ordered list of items by an attribute

When you create a collection you must configure the pk attribute, and the order attribute.

The order attribute will determine where in the list the item falls.
The pk attribute is how you will look of the object.
"""
import urllib
from .utils import RAISE_NOT_IMPLEMENTED, build_url_path


def get_attr_or_die(item, attr):
    value = getattr(item, attr, None)
    if value is None:
        raise AttributeException("The item is missing a value for the '%s' attribute" % (attr))

    return value


def parse_pk_from_key(key):
    last_key_part = key.split('/')[-1]

    key_prefix, primary_key = last_key_part.split('.', 1)

    return primary_key


class Collection(object):

    key = RAISE_NOT_IMPLEMENTED
    prefix = 'collections'

    @property
    def name(self):
        return camelcase_to_dash(self.__class__.__name__)

    def get_pk(self, item):
        return item.pk

    def base_key_parts(self):
        return [self.prefix, self.name]

    def generate_keys_for_item(self, item):
        pk = self.get_pk(item)

        for key_parts in self.key(item):
            key_parts = self.base_key_parts()
            key_parts += self.get_storage_key_for_item(item)
            key_parts += [pk]

            yield build_url_path(key_parts)

    async def add_item(self, item, storage):
        keys = []
        for storage_key in self.generate_keys_for_item(item):
            keys += [key]
            reqs += [storage.create_key(key)]

        resps = [await x for x in reqs]

        return keys

    async def remove_item(self, item):
        keys = []
        for storage_key in self.generate_keys_for_item(item):
            keys += [key]
            reqs += [storage.remove_key(key)]

        resps = [await x for x in reqs]

        return keys

    async def get_items(max_items=200, continuation_key=None, storage=None):

        return await storage.get_keys(
            prefix=build_url_path(self.base_key_parts()),
            max_items=max_items,
            continuation_key=continuation_key
        )
