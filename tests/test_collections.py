import datetime
import json
from uuid import uuid4, UUID

import attr
import pytest

from ssshelf.collections import Collection
from ssshelf.items import IManager
from .dummy_storage import DummyStorage
from ssshelf.utils import json_dump

@attr.s
class BookmarkModel(object):
    link = attr.ib()
    tags = attr.ib(default=attr.Factory(list))
    created_at = attr.ib(default=attr.Factory(datetime.datetime.utcnow))
    pk = attr.ib(default=attr.Factory(uuid4))


class BookmarkImanager(IManager):
    def serialize_item(self, item):
        return bytes(json_dump(attr.asdict(item)), 'utf8')

    def deserialize_item(self, data):
        return BookmarkModel(**json.loads(data))

    async def get_item(*args, **kwargs):
        return BookmarkModel(link='http://google.com')


class Dummy(Collection):
    pass


class AllBookmarks(Collection):
    def key(self, item):
        return [
            [item.created_at.strftime("%Y-%m-%dT%H:%M:%SZ")]
        ]


def test_not_impl():
    with pytest.raises(NotImplementedError):
        Dummy.key({})


def test_name():
    ab = AllBookmarks()

    assert ab.name == 'all-bookmarks'

    assert ab.base_key_parts() == ['collections', 'all-bookmarks']


def test_pk():
    ab = AllBookmarks()
    bookmark = BookmarkModel(link='http://google.com')

    assert ab.get_pk(bookmark) == str(bookmark.pk)
    assert ab.parse_pk_from_key('asdf/asdfsdd/23/ab') == 'ab'


def test_generate_keys():
    ab = AllBookmarks()
    bookmark = BookmarkModel(
        link='http://google.com',
        created_at=datetime.datetime(2017, 10, 10),
        pk=UUID("1eeaf5ed-11a1-4f72-8c1f-9c53b9584e34")
    )
    assert list(ab.generate_keys_for_item(bookmark)) == [
        "collections/all-bookmarks/2017-10-10T00%3A00%3A00Z/1eeaf5ed-11a1-4f72-8c1f-9c53b9584e34"
    ]


def test_add_item(loop):
    ds = DummyStorage()
    ab = AllBookmarks()
    ab.set_storage(ds)
    bookmark = BookmarkModel(
        link='http://google.com',
        created_at=datetime.datetime(2017, 10, 10),
        pk=UUID("1eeaf5ed-11a1-4f72-8c1f-9c53b9584e34")
    )
    loop.run_until_complete(ab.add_item(bookmark))
    assert ds.create_key_call_count == 1


def test_remove_item(loop):
    ds = DummyStorage()
    ab = AllBookmarks()
    ab.set_storage(ds)
    bookmark = BookmarkModel(
        link='http://google.com',
        created_at=datetime.datetime(2017, 10, 10),
        pk=UUID("1eeaf5ed-11a1-4f72-8c1f-9c53b9584e34")
    )
    loop.run_until_complete(ab.remove_item(bookmark))
    assert ds.remove_key_call_count == 1


def test_get_keys(loop):
    ds = DummyStorage()
    ab = AllBookmarks()
    im = BookmarkImanager()
    im.set_storage(ds)
    ab.set_storage(ds)
    ab.set_item_manager(im)
    ds._set_get_keys({
        'keys': ["blah/19"]
    })

    resp = loop.run_until_complete(ab.get_keys())
    assert ds.get_keys_call_count == 1
    assert resp['keys'] == ['19']


def test_get_items(loop):
    ds = DummyStorage()
    ab = AllBookmarks()
    im = BookmarkImanager()
    im.set_storage(ds)
    ab.set_storage(ds)

    ab.set_item_manager(im)

    ds._set_get_keys({
        'keys': ["blah/19"]
    })

    ds._set_get_key({})

    resp = loop.run_until_complete(ab.get_items())
    assert resp['items'][0].link == 'http://google.com'
