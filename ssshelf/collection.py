"""
SSShelf Collections

A collections is an ordered list of items by an attribute

When you create a collection you must configure the pk attribute, and the order attribute.

The order attribute will determine where in the list the item falls.
The pk attribute is how you will look of the object.
"""


def get_attr_or_die(item, attr):
    value = getattr(item, attr, None)
    if value is None:
        raise AttributeException("The item is missing a value for the '%s' attribute" % (attr))

    return value


def parse_pk_from_key(key):
    last_key_part = key.split('/')[-1]

    key_prefix, primary_key = last_key_part.split('.', 1)

    return primary_key


class Collection(object):

    name = None
    item_class = None
    order_attr = None
    pk_attr = 'pk'
    key_prefix = 'collections'

    def key(self, suffix):
        return '%s/%s/%s' % (self.key_prefix, self.name, suffix)

    def get_order_attr_for_item(self, item):
        return get_attr_or_die(item, self.order_attr)

    def get_pk_attr_for_item(self, item):
        return get_attr_or_die(item, self.pk_attr)

    def get_storage_key_for_item(self, item):
        return '%s.%s' % (
            hash(self.get_order_attr_for_item(item)),
            self.get_pk_attr_for_item(),
        )

    async def add_item(self, item):
        storage_key = self.get_storage_key_for_item(item)
        with storage as cl:
            await cl.create_key(storage_key)

    async def remove_item(self, item):
        storage_key = self.get_storage_key_for_item(item)
        with storage as cl:
            await cl.remove_key(storage_key)

    async def get_page(start_at=None, end_at=None, max_items=200):
        with storage as cl:
            keys = await cl.get_keys(start_at=None, end_at=None, max_items=200)

        primary_keys = [parse_pk_from_key(x) for x in keys]

        self.item_class.get_items(primary_keys)

