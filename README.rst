SSShelf
=======

An S3 persistance manager. If you squint closely enough you could even call it a database.

Goals
-----

- High test coverage
- Lots of examples
- Treat s3 like a database

Concerns
--------

- Eventual Consistency
- Speed
- Constraints

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



