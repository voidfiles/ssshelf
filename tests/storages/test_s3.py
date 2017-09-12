import json
import pytest
from ssshelf.storages.s3 import S3Storage


async def create_bucket(s3_client):
    await s3_client.create_bucket(Bucket='test_bucket')


async def read_body(resp):
    return await resp.get('Body').read()


@pytest.mark.moto
def test_my_model_save(s3_client, loop):
    loop.run_until_complete(create_bucket(s3_client))

    storage = S3Storage(bucket='test_bucket', s3_client=s3_client)
    document = {
        "x": "y"
    }

    document_str = bytes(json.dumps(document), 'utf8')
    loop.run_until_complete(storage.create_key('test', data=document_str))

    resp = loop.run_until_complete(storage.get_key('test'))

    body_data = loop.run_until_complete(read_body(resp))

    body_json = json.loads(body_data)

    assert document == body_json

@pytest.mark.moto
def test_multiple_keys(s3_client, loop):
    loop.run_until_complete(create_bucket(s3_client))

    storage = S3Storage(bucket='test_bucket', s3_client=s3_client)
    document = {
        "x": "y"
    }

    document_str = bytes(json.dumps(document), 'utf8')
    for i in range(0, 20):
        loop.run_until_complete(storage.create_key('bulk_test%03d' % (i), data=document_str))

    resp = loop.run_until_complete(storage.get_keys('bulk_test', max_keys=10))

    assert len(resp['keys']) == 10
    for i in range(0, 10):
        assert resp['keys'][i] == 'bulk_test%03d' % (i)

    assert 'continuation_token' in resp

    resp2 = loop.run_until_complete(
        storage.get_keys('bulk_test', max_keys=10,
                         continuation_token=resp['continuation_token'])
    )

    assert len(resp2['keys']) == 10
    for i in range(0, 9):
        assert resp2['keys'][i] == 'bulk_test%03d' % (i + 10)

    assert 'continuation_token' not in resp2
