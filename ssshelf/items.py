from .utils import camelcase_to_dash, build_url_path


class IManager(object):
    prefix = 'items'

    @property
    def name(self):
        return camelcase_to_dash(self.__class__.__name__)

    def base_key_parts(self):
        return [self.prefix, self.name]

    def get_pk(self, item):
        return str(item.pk)

    def generate_key_for_pk(self, pk):

        key_parts = self.base_key_parts()
        key_parts += [pk]

        return build_url_path(key_parts)

    def serialize_item(self, item):
        raise NotImplementedError

    def deserialize_item(self, data):
        raise NotImplementedError

    async def add_item(self, item, storage):
        key = self.generate_key_for_pk(self.get_pk(item))
        return await storage.create_key(key, data=self.serialize_item(item))

    async def remove_item(self, item, storage):
        key = self.generate_key_for_pk(self.get_pk(item))
        return await storage.remove_key(key)

    async def get_item(self, pk, storage):
        key = self.generate_key_for_pk(pk)
        resp = await storage.get_key(key)

        return self.deserialize_item(resp['data'])
