from datetime import datetime
import simpleflake
import json

from ssshelf.items import IManager
from ssshelf.collections import Collection
from ssshelf.utils import convert_datetime_to_str, json_dump
from ssshelf.managers import CManager
from ssshelf.storages.inmemory import InMemoryStorage


class Bookmark(IManager):
    def get_pk(self, item):
        return str(item['pk'])

    def serialize_item(self, item):
        return bytes(json_dump(item), 'utf8')

    def deserialize_item(self, data):
        return json.loads(data)


class AllBookmarks(Collection):
    def get_pk(self, item):
        return str(item['pk'])

    def key(self, item):
        return [
          [convert_datetime_to_str(item['created_at'])]
        ]


class BookmarkManager(CManager):
    item_manager = Bookmark()
    every = AllBookmarks()

async def demo():
    bookmark_manager = BookmarkManager(InMemoryStorage())

    bookmark = {
        'pk': simpleflake.simpleflake(),
        'link': 'http://google.com',
        'created_at': datetime.utcnow()
    }

    await bookmark_manager.add_item(bookmark)

    resp = await bookmark_manager.every.get_items()

    assert resp['items'][0]['link'] == 'http://google.com'


def test_readme(loop):
    loop.run_until_complete(demo())
