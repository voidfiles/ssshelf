import pytest
from datetime import datetime
from ssshelf.utils import type_handler


def test_type_handler():
    dt = datetime(year=2010, month=12, day=2)
    blah = type_handler(dt)
    assert '2010-12-02' in blah


def test_type_handler_raise():
    with pytest.raises(TypeError):
        type_handler(12)
