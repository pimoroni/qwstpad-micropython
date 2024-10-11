import sys

import mock
import pytest


@pytest.fixture(scope="function", autouse=False)
def machine():
    sys.modules["machine"] = mock.MagicMock()
    yield sys.modules["machine"]
    del sys.modules["machine"]


@pytest.fixture(scope="function", autouse=False)
def micropython():
    sys.modules["micropython"] = mock.MagicMock()
    sys.modules["micropython"].const = lambda x: x
    yield sys.modules["micropython"]
    del sys.modules["micropython"]

