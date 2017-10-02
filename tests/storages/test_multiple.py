import json
import pytest

from ssshelf.storages.inmemory import InMemoryStorage
from ssshelf.storages.s3 import S3Storage
from ssshelf.keys import IndexKey, PrefixKey


async def create_bucket(s3_client):
    await s3_client.create_bucket(Bucket='test_bucket')


@pytest.fixture
@pytest.mark.moto
def s3_storage(s3_client, loop):
    loop.run_until_complete(create_bucket(s3_client))
    return S3Storage(bucket='test_bucket', s3_client=s3_client)

@pytest.fixture
def in_memory_storage():
    return InMemoryStorage()


def test_multiple_keys(in_memory_storage, s3_storage, loop):

    for storage in (in_memory_storage, s3_storage):
        print(storage)
        document = {
            "x": "y"
        }

        document_str = bytes(json.dumps(document), 'utf8')
        keys = sorted([x for x in "abcdefghijklmnopqrst"], reverse=True)
        for i in keys:
            loop.run_until_complete(storage.create_key(IndexKey('bulk_test%s' % (i)), data=document_str))

        resp = loop.run_until_complete(storage.get_keys(PrefixKey(['bulk_test']), max_keys=10))

        reverse_keys = sorted(keys)
        assert len(resp['keys']) == 10
        for i, key in enumerate(reverse_keys[0:9]):
            assert resp['keys'][i] == IndexKey('bulk_test%s' % (key))

        assert 'after' in resp

        resp2 = loop.run_until_complete(
            storage.get_keys(PrefixKey(['bulk_test']), max_keys=10,
                             after=resp['after'])
        )

        assert len(resp2['keys']) == 10
        for i, key in enumerate(reverse_keys[10:]):
            assert resp2['keys'][i] == IndexKey('bulk_test%s' % (key))

        assert 'after' not in resp2

        keys_to_delete = [IndexKey('bulk_test%s' % (i)) for i in keys]

        loop.run_until_complete(storage.remove_keys(keys_to_delete))

        resp3 = loop.run_until_complete(
            storage.get_keys(PrefixKey(['bulk_test']), max_keys=10,
                             after=resp['after'])
        )
        assert len(resp3['keys']) == 0
