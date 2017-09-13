import asyncio
import aiobotocore
from retrying import retry


@retry(stop_max_attempt_number=2)
def retry_client(method, *args, **kwargs):
    return method(*args, **kwargs)


class S3Storage(object):

    def __init__(self, bucket, aws_client_kwargs=None, s3_client=None):
        self.aws_client_kwargs = aws_client_kwargs if aws_client_kwargs else {
            'region_name': 'us-east-1',
        }
        self.bucket = bucket
        self.s3_client = s3_client

    def get_s3_client(self):
        if self.s3_client:
            return self.s3_client

        session = aiobotocore.get_session(loop=loop)
        self.s3_client = session.create_client('s3', **self.aws_client_kwargs)

        return self.s3_client

    async def create_key(self, storage_key, data=None):
        data = data if data else bytes()

        await retry_client(
            self.get_s3_client().put_object,
            Bucket=self.bucket,
            Key=storage_key,
            Body=data
        )

    async def remove_key(self, storage_key):

        await retry_client(
            self.get_s3_client().delete_object,
            Bucket=self.bucket,
            Key=storage_key,
        )

    async def remove_keys(self, storage_keys):

        await retry_client(
            self.get_s3_client().delete_objects,
            Bucket=self.bucket,
            Delete={
                "Objects": [{'Key': x} for x in storage_keys],
                "Quiet": True,
            },
        )

    async def get_key(self, storage_key):
        resp = await retry_client(
            self.get_s3_client().get_object,
            Bucket=self.bucket,
            Key=storage_key,
        )

        return {
            'data': await resp.get('Body').read(),
            'metadata': resp.get('Metadata', {}),
        }

    async def get_keys(self, prefix, max_keys=200, continuation_token=None):

        resp = None

        kwargs = {
            "Bucket": self.bucket,
            "MaxKeys": max_keys,
            "Prefix": prefix,
        }

        if continuation_token:
            kwargs['ContinuationToken'] = continuation_token

        resp = await retry_client(
            self.get_s3_client().list_objects_v2,
            **kwargs,
        )

        response_keys = [x['Key'] for x in resp.get('Contents', [])]

        resp_data = {
            'keys': response_keys,
        }

        continuation_token = resp.get('NextContinuationToken')
        if continuation_token:
            resp_data['continuation_token'] = continuation_token

        return resp_data
