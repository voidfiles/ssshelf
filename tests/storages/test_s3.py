from botocore.exceptions import ClientError
import json
import pytest
from ssshelf.storages.s3 import S3Storage
from ssshelf.keys import IndexKey, PrefixKey

async def create_bucket(s3_client):
    await s3_client.create_bucket(Bucket='test_bucket')


@pytest.mark.moto
def test_my_model_save(s3_client, loop):
    loop.run_until_complete(create_bucket(s3_client))

    storage = S3Storage(bucket='test_bucket', s3_client=s3_client)
    document = {
        "x": "y"
    }

    document_str = bytes(json.dumps(document), 'utf8')
    loop.run_until_complete(storage.create_key(IndexKey('test'), data=document_str))

    resp = loop.run_until_complete(storage.get_key(IndexKey('test')))

    assert 'metadata' in resp
    body_json = json.loads(resp['data'])

    assert document == body_json

    loop.run_until_complete(storage.remove_key(IndexKey('test')))

    with pytest.raises(ClientError):
        loop.run_until_complete(storage.get_key(IndexKey('test')))


@pytest.mark.moto
def test_get_s3_client():
    storage = S3Storage(bucket='test_bucket')
    session = storage.get_s3_client()
    assert storage.s3_client
