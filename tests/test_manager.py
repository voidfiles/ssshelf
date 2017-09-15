import json
from uuid import uuid4, UUID

import attr

from ssshelf.managers import CManager
from ssshelf.collections import Collection
from ssshelf.items import IManager
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


class BookmarkItemManager(IManager):
    def serialize_item(self, item):
        return bytes(json_dump(attr.asdict(item)), 'utf8')

    def deserialize_item(self, data):
        data = json.loads(data)
        return BookmarkModel(**data)

    def get_pk(self, item):
        return str(item.pk)


class Dummy(Collection):

    def key(self, item):
        return [
            [item.link]
        ]

    async def add_item(self, item):
        self.add_item_called = True
        self.add_item_called_with = item

    async def remove_item(self, item):
        self.remove_item_called = True
        self.remove_item_called_with = item


class AllBookmarks(Collection):
    def key(self, item):
        return [
            [item.link]
        ]


class BookmarkManagerDummy(CManager):
    item_manager = BookmarkItemManager()

    all = Dummy()


class BookmarkManagerAll(CManager):
    item_manager = BookmarkItemManager()

    all = AllBookmarks()


def test_add_collection():
    bookmark_manager = BookmarkManagerDummy(DummyStorage())

    assert isinstance(bookmark_manager.all, Dummy)


def test_add_item(loop):
    bookmark_manager = BookmarkManagerDummy(DummyStorage())

    item = BookmarkModel(link="http://google.com")

    loop.run_until_complete(bookmark_manager.add_item(item))

    assert bookmark_manager.all.add_item_called is True
    assert bookmark_manager.all.add_item_called_with.link == item.link


def test_remove_item(loop):
    bookmark_manager = BookmarkManagerDummy(DummyStorage())

    item = BookmarkModel(link="http://google.com")

    loop.run_until_complete(bookmark_manager.remove_item(item))

    assert bookmark_manager.all.remove_item_called is True
    assert bookmark_manager.all.remove_item_called_with.link == item.link


def test_get_items_for_collection(loop):
    storage = InMemoryStorage()
    bookmark_manager = BookmarkManagerAll(storage)

    item1 = BookmarkModel(link="http://google.com")
    item2 = BookmarkModel(link="http://news.ycombinator.com")

    loop.run_until_complete(bookmark_manager.add_item(item1))
    loop.run_until_complete(bookmark_manager.add_item(item2))

    resp = loop.run_until_complete(bookmark_manager.all.get_items())

    assert len(resp['items']) == 2
