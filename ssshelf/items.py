"""
Item Managers
-------------

An item manager allows you persist items, and retrieve
them by keys.

"""

from .utils import camelcase_to_dash, build_url_path


class IManager(object):
    def __init__(self, prefix='items', name=None, storage=None):
        self.name = name if name else camelcase_to_dash(self.__class__.__name__)
        self.prefix = prefix
        self.storage = storage

    def set_storage(self, storage):
        self.storage = storage

    def base_key_parts(self):
        return [self.prefix, self.name]

    def get_pk(self, item):
        return str(item.pk)

    def generate_key_for_pk(self, pk):

        key_parts = self.base_key_parts()
        key_parts += [pk]

        return build_url_path(key_parts)

    def serialize_item(self, item):
        raise NotImplementedError

    def deserialize_item(self, data):
        raise NotImplementedError

    async def add_item(self, item):
        key = self.generate_key_for_pk(self.get_pk(item))
        return await self.storage.create_key(key, data=self.serialize_item(item))

    async def remove_item(self, item):
        key = self.generate_key_for_pk(self.get_pk(item))
        return await self.storage.remove_key(key)

    async def get_item(self, pk):
        key = self.generate_key_for_pk(pk)
        resp = await self.storage.get_key(key)

        return self.deserialize_item(resp['data'])
