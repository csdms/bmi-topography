import os
from unittest import mock

import pytest

from bmi_topography.topography import find_user_api_key, read_first_of, use_demo_key


def copy_environ(exclude=None):
    if exclude is None:
        exclude = {}
    elif isinstance(exclude, str):
        exclude = {exclude}

    return {key: value for key, value in os.environ.items() if key not in exclude}


def test_find_user_api_key_not_found():
    """The API key is not given anywhere"""
    env = copy_environ(exclude="OPENTOPOGRAPHY_API_KEY")
    with mock.patch.dict(os.environ, env, clear=True):
        assert find_user_api_key() == ""


@mock.patch.dict(os.environ, {"OPENTOPOGRAPHY_API_KEY": "foo"})
def test_find_user_api_key_env(tmpdir):
    """The API key is an environment variable"""
    with tmpdir.as_cwd():
        with open(".opentopography.txt", "w") as fp:
            fp.write("bar")
    assert find_user_api_key() == "foo"


@mock.patch.dict(os.environ, {"OPENTOPOGRAPHY_API_KEY": "foo"})
def test_find_user_api_key_from_file(tmpdir):
    """The API key is in a file"""
    env = copy_environ(exclude="OPENTOPOGRAPHY_API_KEY")
    with tmpdir.as_cwd():
        with open(".opentopography.txt", "w") as fp:
            fp.write("bar")

        with mock.patch.dict(os.environ, env, clear=True):
            assert find_user_api_key() == "bar"


def test_read_first_missing(tmpdir):
    with tmpdir.as_cwd():
        assert read_first_of(["foo.txt"]) == ""
        assert read_first_of([]) == ""


def test_read_first_file(tmpdir):
    with tmpdir.as_cwd():
        with open("foo.txt", "w") as fp:
            fp.write("foo")
        with open("bar.txt", "w") as fp:
            fp.write("bar")

        assert read_first_of(["foo.txt", "bar.txt"]) == "foo"
        assert read_first_of(["bar.txt", "foo.txt"]) == "bar"


def test_use_demo_key_is_a_string():
    demo_key = use_demo_key()
    assert isinstance(demo_key, str)
    assert len(demo_key) > 0


def test_use_demo_key_issues_warning():
    with pytest.warns(UserWarning):
        use_demo_key()
