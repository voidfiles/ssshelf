# from .proxy import StorageProxy
#
#
# class ReadKeysCacheRedis(StorageProxy):
#     def __init__(self, storage, redis):
#         super(ReadKeysCacheInMemory, self).__init__(storage)
#         self.redis = redis
#
#     async def create_key(self, storage_key, data=None):
#         data = await self.storage.create_key(storage_key, data)
#         self.t[storage_key.get_url_path()] = ''
#
#         return data
#
#     async def remove_key(self, storage_key):
#         await self.storage.remove_key(storage_key)
#         if storage_key.get_url_path() in self.t:
#             del self.t[storage_key.get_url_path()]
#
#     async def remove_keys(self, storage_keys):
#         await self.storage.remove_keys(storage_keys)
#         for x in storage_keys:
#             self._cache.remove(x.get_url_path())
#
#     async def get_keys(self, prefix, max_keys=200, after=None):
#         resp = None
#         if not after:
#             after = prefix.as_url_path()
#
#         keys = self.t.iterkeys(after)[:max_keys]
#
#         if len(keys) <= max_keys:
#             more = max_keys - len(keys)
#             start_token = keys[-1]
#             resp = self.storage.get_keys(prefix, more, start_token)
#             keys += resp['keys']
#             after = resp.get('after')
#
#         if after:
#             kwargs['after'] = after
#
#         resp = await retry_client(
#             self.get_s3_client().list_objects_v2,
#             **kwargs,
#         )
#
#         response_keys = [x['Key'] for x in resp.get('Contents', [])]
#
#         resp_data = {
#             'keys': response_keys,
#         }
#
#         after = resp.get('after')
#         if after:
#             resp_data['after'] = after
#
#         return resp_data
