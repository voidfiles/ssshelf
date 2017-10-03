try:
    from lsm import LSM
except ImportError:  # pragma: no cover
    raise ImportError("To use the LSM storage engine you must install lsm-db")  # pragma: no cover

from ssshelf.keys import IndexKey

def format_storage_key(storage_key):
    path = storage_key.as_url_path()
    return bytes(path, 'utf8')

class LSMStorage(object):

    def __init__(self, db_path=None):
        self.t = LSM(db_path)

    async def create_key(self, storage_key, data=None):
        data = data if data else bytes()

        self.t[format_storage_key(storage_key)] = data

        return data

    async def remove_key(self, storage_key):
        del self.t[format_storage_key(storage_key)]

    async def remove_keys(self, storage_keys):
        for key in storage_keys:
            del self.t[format_storage_key(key)]

    async def get_key(self, storage_key):
        try:
            value = self.t.fetch(format_storage_key(storage_key))
        except KeyError:
            return {
                'data': None,
                'metadata': None
            }

        return {
            'data': value,
            'metadata': {},
        }

    async def get_keys(self, prefix, max_keys=200, after=None):

        start_at = after if after else prefix.as_url_path()

        keys = []
        found_token = False

        start_at = bytes(start_at, 'utf8')
        broke_early = False
        for x, val in self.t[start_at:]:
            if len(keys) == max_keys:
                broke_early = True
                break

            if not x.startswith(format_storage_key(prefix)):
                break

            keys.append(IndexKey.from_url_path(x.decode('utf8')))

        after = None
        if broke_early and x.startswith(format_storage_key(prefix)):
            after = x.decode('utf8')

        ret = {
            'keys': keys,
        }

        if after:
            ret['after'] = after

        return ret
