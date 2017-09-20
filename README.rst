SSShelf
=======

.. image:: https://img.shields.io/pypi/v/ssshelf.svg
    :target: https://pypi.python.org/pypi/ssshelf

.. image:: https://travis-ci.org/voidfiles/ssshelf.svg?branch=master
    :target: https://travis-ci.org/voidfiles/ssshelf

.. image:: https://codeclimate.com/github/voidfiles/ssshelf/badges/gpa.svg
   :target: https://codeclimate.com/github/voidfiles/ssshelf
   :alt: Code Climate

.. image:: https://codeclimate.com/github/voidfiles/ssshelf/badges/coverage.svg
   :target: https://codeclimate.com/voidfiles/ssshelf/codeclimate/coverage
   :alt: Test Coverage


An S3 persistance manager. If you squint closely enough you could even call it a database.

Goals
-----

- Lots of examples
- Blob Storage as primary (S3, Ceph, Google Cloud Storage, etc.)

Concerns
--------

- Eventual Consistency
- Speed
- Constraints

Examples Using SSShelf
----------------------

- A URL Shortner ready for heroku https://github.com/voidfiles/ssshelf-url-shortener

Example
-------


.. code-block:: python

    import asyncio
    from datetime import datetime
    import simpleflake
    import json

    from ssshelf.items import IManager
    from ssshelf.collections import Collection
    from ssshelf.utils import convert_datetime_to_str, json_dump
    from ssshelf.managers import CManager
    from ssshelf.storages.s3 import S3Storage


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
            return convert_datetime_to_str(item['created_at'])


    class BookmarkManager(CManager):
        item_manager = Bookmark()
        every = AllBookmarks()

    async def demo():
        bookmark_manager = BookmarkManager(S3Storage())

        bookmark = {
            'pk': simpleflake.simpleflake(),
            'link': 'http://google.com',
            'created_at': datetime.utcnow()
        }

        await bookmark_manager.add_item(bookmark)

        items = await bookmark_manager.every.get_items()

        assert resp['items'][0]['link'] == 'http://google.com'

    loop = asyncio.get_event_loop()
    loop.run_until_complete(demo())



