

class DummyStorage(object):

    def __init__(self, *args, **kwargs):
        self.create_key_call_count = 0
        self.get_key_call_count = 0
        self.get_keys_call_count = 0
        self.remove_key_call_count = 0
        self.remove_keys_call_count = 0

    async def create_key(self, *args, **kwargs):
        self.create_key_call_count += 1
        self.create_key_called_with = {
            'args': args,
            'kwargs': kwargs
        }

    async def remove_key(self, *args, **kwargs):
        self.remove_key_call_count += 1

    async def remove_keys(self, *args, **kwargs):
        self.remove_keys_call_count += 1

    def _set_get_key(self, data=None, metadata=None):
        self._next_data = data
        self._next_metadata = metadata

    async def get_key(self, storage_key):
        self.get_key_call_count += 1
        return {
            'data': self._next_data,
            'metadata': self._next_metadata,
        }

    def _set_get_keys(self, keys):
        self._next_keys = keys

    async def get_keys(self, prefix, max_keys=200, continuation_token=None):
        self.get_keys_call_count += 1
        return self._next_keys
