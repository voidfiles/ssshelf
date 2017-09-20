import pygtrie


class InMemoryStorage(object):

    def __init__(self):
        self.t = pygtrie.CharTrie()

    async def create_key(self, storage_key, data=None):
        data = data if data else bytes()

        self.t[storage_key] = data

        return data

    async def remove_key(self, storage_key):
        del self.t[storage_key]

    async def remove_keys(self, storage_keys):

        for key in storage_keys:
            del self.t[key]

    async def get_key(self, storage_key):

        return {
            'data': self.t.get(storage_key),
            'metadata': {},
        }

    def _build_keys(self, key_iterator, max_keys, continuation_token):
        keys = []
        found_token = False

        for x in key_iterator:
            if continuation_token and found_token is False:
                if x != continuation_token:
                    continue

                found_token = True

            keys.append(x)

            if len(keys) == max_keys:
                break

        return keys

    async def get_keys(self, prefix, max_keys=200, continuation_token=None):

        key_iterator = self.t.iterkeys(prefix)

        try:
            keys = self._build_keys(key_iterator, max_keys, continuation_token)
        except KeyError:
            return {
                'keys': []
            }

        try:
            continuation_token = next(key_iterator)
        except StopIteration:
            continuation_token = None

        ret = {
            'keys': keys,
        }

        if continuation_token:
            ret['continuation_token'] = continuation_token

        return ret
