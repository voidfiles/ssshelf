import json
from uuid import uuid4, UUID

import attr

from ssshelf.manager import Manager
from ssshelf.collections import Collection
from ssshelf.item import ItemManager
from ssshelf.storages.inmemory import InMemoryStorage
from ssshelf.utils import json_dump
from .dummy_storage import DummyStorage


def convert_uuid(input_):
    if isinstance(input_, UUID):
        return input_

    return UUID(input_)


@attr.s
class BookmarkModel(object):
    link = attr.ib()
    pk = attr.ib(default=attr.Factory(uuid4), convert=convert_uuid)


class BookmarkItemManager(ItemManager):
    def serialize_item(self, item):
        return bytes(json_dump(attr.asdict(item)), 'utf8')

    def deserialize_item(self, data):
        data = json.loads(data)
        return BookmarkModel(**data)

    def get_pk(self, item):
        return str(item.pk)


class BookmarkManager(Manager):
    item_manager = BookmarkItemManager()


class Dummy(Collection):

    def key(self, item):
        return [
            [item.link]
        ]

    async def add_item(self, item, storage):
        self.add_item_called = True
        self.add_item_called_with = item

    async def remove_item(self, item, storage):
        self.remove_item_called = True
        self.remove_item_called_with = item


class AllBookmarks(Collection):
    def key(self, item):
        return [
            [item.link]
        ]


def test_add_collection():
    bookmark_manager = BookmarkManager(DummyStorage())
    bookmark_manager.add_collection('all', Dummy())

    assert isinstance(bookmark_manager._collections['all'], Dummy)


def test_add_item(loop):
    bookmark_manager = BookmarkManager(DummyStorage())
    collection = Dummy()
    bookmark_manager.add_collection('all', collection)

    item = BookmarkModel(link="http://google.com")

    loop.run_until_complete(bookmark_manager.add_item(item))

    assert collection.add_item_called is True
    assert collection.add_item_called_with.link == item.link


def test_remove_item(loop):
    bookmark_manager = BookmarkManager(DummyStorage())
    collection = Dummy()
    bookmark_manager.add_collection('all', collection)

    item = BookmarkModel(link="http://google.com")

    loop.run_until_complete(bookmark_manager.remove_item(item))

    assert collection.remove_item_called is True
    assert collection.remove_item_called_with.link == item.link


def test_get_items_for_collection(loop):
    storage = InMemoryStorage()
    bookmark_manager = BookmarkManager(storage)
    bookmark_manager.add_collection('all', AllBookmarks())

    item1 = BookmarkModel(link="http://google.com")
    item2 = BookmarkModel(link="http://news.ycombinator.com")

    loop.run_until_complete(bookmark_manager.add_item(item1))
    loop.run_until_complete(bookmark_manager.add_item(item2))

    resp = loop.run_until_complete(bookmark_manager.get_items_for_collection('all'))

    assert len(resp['items']) == 2
