import datetime
import mock
import json
from uuid import uuid4, UUID

import attr
import iso8601
import pytest


from ssshelf.item import ItemManager
from ssshelf.utils import json_dump
from .dummy_storage import DummyStorage

class Dummy(ItemManager):
    pass


def coerce_datetime(input_):
    if isinstance(input_, datetime.datetime):
        return input_

    return iso8601.parse_date(input_)


def convert_uuid(input_):
    if isinstance(input_, UUID):
        return input_

    return UUID(input_)


@attr.s
class BookmarkModel(object):
    link = attr.ib()
    tags = attr.ib(default=attr.Factory(list))
    created_at = attr.ib(default=attr.Factory(datetime.datetime.utcnow), convert=coerce_datetime)
    pk = attr.ib(default=attr.Factory(uuid4), convert=convert_uuid)


class Bookmark(ItemManager):
    def serialize_item(self, item):
        return bytes(json_dump(attr.asdict(item)), 'utf8')

    def deserialize_item(self, data):
        data = json.loads(data)
        return BookmarkModel(**data)

    def get_pk(self, item):
        return str(item.pk)


def test_not_implmented():
    d = Dummy()

    with pytest.raises(NotImplementedError):
        d.serialize_item({})

    with pytest.raises(NotImplementedError):
        d.deserialize_item({})


def test_key_parts():
    d = Dummy()
    assert d.name == 'dummy'

    assert d.base_key_parts() == ['items', 'dummy']


def test_serializer_deserializer():
    bookmark_manager = Bookmark()
    bookmark = BookmarkModel(link='http://google.com')
    serialized_bookmark = bookmark_manager.serialize_item(bookmark)
    assert 'http://google.com' in str(serialized_bookmark)
    bookmark_2 = bookmark_manager.deserialize_item(serialized_bookmark)
    print(serialized_bookmark)
    assert bookmark_2.link == bookmark.link
    assert bookmark_2.created_at.year == bookmark.created_at.year
    assert bookmark_2.pk == bookmark.pk


def test_generate_key_for_item():
    bookmark_manager = Bookmark()
    bookmark = BookmarkModel(link='http://google.com')
    expected_key = 'items/bookmark/%s' % (str(bookmark.pk))
    assert bookmark_manager.generate_key_for_item(bookmark) == expected_key


def test_add_item(loop):
    ds = DummyStorage()
    bookmark_manager = Bookmark()
    bookmark = BookmarkModel(link='http://google.com')
    loop.run_until_complete(bookmark_manager.add_item(bookmark, storage=ds))
    assert ds.create_key_call_count == 1
    assert ds.create_key_called_with['kwargs']['data'] == bookmark_manager.serialize_item(bookmark)


def test_remove_item(loop):
    ds = DummyStorage()
    bookmark_manager = Bookmark()
    bookmark = BookmarkModel(link='http://google.com')
    loop.run_until_complete(bookmark_manager.remove_item(bookmark, storage=ds))
    assert ds.remove_key_call_count == 1
