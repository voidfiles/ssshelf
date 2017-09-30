import pygtrie

from ssshelf.keys import IndexKey

class InMemoryStorage(object):

    def __init__(self):
        self.t = pygtrie.CharTrie()
        self.t.enable_sorting()

    async def create_key(self, storage_key, data=None):
        data = data if data else bytes()

        self.t[storage_key.as_url_path()] = data

        return data

    async def remove_key(self, storage_key):
        del self.t[storage_key.as_url_path()]

    async def remove_keys(self, storage_keys):
        for key in storage_keys:
            del self.t[key.as_url_path()]

    async def get_key(self, storage_key):
        return {
            'data': self.t.get(storage_key.as_url_path()),
            'metadata': {},
        }

    def _build_keys(self, key_iterator, max_keys, after):
        keys = []
        found_token = False

        for x in key_iterator:
            if after and found_token is False:
                if x != after:
                    continue

                found_token = True

                continue

            keys.append(IndexKey.from_url_path(x))

            if len(keys) == max_keys:
                break

        return keys

    async def get_keys(self, prefix, max_keys=200, after=None):
        key_iterator = self.t.iterkeys(prefix.as_url_path())

        try:
            keys = self._build_keys(key_iterator, max_keys, after)
        except KeyError:
            return {
                'keys': []
            }

        try:
            next(key_iterator)
            after = keys[-1].as_url_path()
        except StopIteration:
            after = None

        ret = {
            'keys': keys,
        }

        if after:
            ret['after'] = after

        return ret
