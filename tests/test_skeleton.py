# -*- coding: utf-8 -*-

import pytest
from subsonic_api_proxy.skeleton import fib

__author__ = "Patrick Ruckstuhl"
__copyright__ = "Patrick Ruckstuhl"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
