"""
Collection Managers
-------------------

Collection managers brings together the item manager,
collections and storages.

"""
import six
from .utils import RAISE_NOT_IMPLEMENTED
from .collections import Collection


class CManagerMetaclass(type):
    """
    This metaclass sets a dictionary named `_declared_collections` on the class.
    Any instances of `Collection` included as attributes on either the class
    or on any of its superclasses will be include in the
    `_declared_collections` dictionary.
    """

    @classmethod
    def _get_declared_collections(cls, bases, attrs):
        fields = []
        for collection_name, obj in list(attrs.items()):
            if isinstance(obj, Collection):
                fields += [(collection_name, attrs.get(collection_name))]

        # If this class is subclassing another Serializer, add that Serializer's
        # fields.  Note that we loop over the bases in *reverse*. This is necessary
        # in order to maintain the correct order of fields.
        for base in reversed(bases):
            if hasattr(base, '_declared_collections'):
                fields = [
                    (collection_name, obj) for collection_name, obj
                    in base._declared_collections.items()
                    if collection_name not in attrs
                ] + fields

        return dict(fields)

    def __new__(cls, name, bases, attrs):
        attrs['_declared_collections'] = cls._get_declared_collections(bases, attrs)
        return super(CManagerMetaclass, cls).__new__(cls, name, bases, attrs)


@six.add_metaclass(CManagerMetaclass)
class CManager(object):
    item_manager = RAISE_NOT_IMPLEMENTED

    def __init__(self, storage):
        self.storage = storage

        for collection in self._declared_collections.values():
            collection.set_storage(self.storage)
            self.item_manager.set_storage(self.storage)
            collection.set_item_manager(self.item_manager)

    async def add_item(self, item):
        await self.item_manager.add_item(item)
        awaitable_resps = {}
        for name, collection in self._declared_collections.items():
            awaitable_resps[name] = collection.add_item(item)

        resps = {}
        for name, resp in awaitable_resps.items():
            resps[name] = await resp

        return resps

    async def remove_item(self, item):
        awaitable_resps = {}
        for name, collection in self._declared_collections.items():
            awaitable_resps[name] = collection.remove_item(item)

        resps = {}
        for name, resp in awaitable_resps.items():
            resps[name] = await resp

        await self.item_manager.remove_item(item)

        return resps
