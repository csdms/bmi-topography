import os
from unittest import mock

import pytest

from bmi_topography.api_key import ApiKey, _find_first_of
from bmi_topography.errors import BadApiKeySource, BadKeyError, MissingKeyError


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
        with pytest.raises(MissingKeyError):
            ApiKey.from_env()


@pytest.mark.parametrize("bad_key", [None, 0, 1, ""])
def test_bad_user_key(bad_key):
    with pytest.raises(BadKeyError):
        ApiKey(bad_key)


@pytest.mark.parametrize("bad_source", [None, 0, 1, "", "not-a-source"])
def test_bad_source(bad_source):
    with pytest.raises(BadApiKeySource):
        ApiKey("foobar", source=bad_source)


@mock.patch.dict(os.environ, {"OPENTOPOGRAPHY_API_KEY": "foo"})
def test_find_user_api_key_env(tmpdir):
    """The API key is an environment variable"""
    with tmpdir.as_cwd():
        with open(".opentopography.txt", "w") as fp:
            fp.write("bar")
        key = ApiKey.from_sources()
    assert key == "foo"
    assert key.source == "env"
    assert key == ApiKey("foo", source="env")


@mock.patch.dict(os.environ, {"OPENTOPOGRAPHY_API_KEY": "foo"})
def test_find_user_api_key_from_file(tmpdir):
    """The API key is in a file"""
    env = copy_environ(exclude="OPENTOPOGRAPHY_API_KEY")
    with tmpdir.as_cwd():
        with open(".opentopography.txt", "w") as fp:
            fp.write("bar")

        with mock.patch.dict(os.environ, env, clear=True):
            key = ApiKey.from_sources()
            assert key == "bar"
            assert key.source.startswith("file:")
            assert key.source.endswith(".opentopography.txt")


@mock.patch.dict(os.environ, {"OPENTOPOGRAPHY_API_KEY": "foo"})
def test_find_user_api_key_from_user(tmpdir):
    """The API key is in a file"""
    env = copy_environ(exclude="OPENTOPOGRAPHY_API_KEY")
    with tmpdir.as_cwd():
        with mock.patch.dict(os.environ, env, clear=True):
            key = ApiKey.from_sources(api_key="foobar")
            assert key == "foobar"
            assert key.source.startswith("user")


def test_find_user_api_key_from_missing_file(tmpdir):
    """The API key is in a file"""
    env = copy_environ(exclude="OPENTOPOGRAPHY_API_KEY")
    with tmpdir.as_cwd():
        with mock.patch.dict(os.environ, env, clear=True):
            with pytest.raises(MissingKeyError):
                ApiKey.from_file()


def test_default_to_demo_key(tmpdir):
    """If a key can't be found, use the demo key"""
    env = copy_environ(exclude="OPENTOPOGRAPHY_API_KEY")
    with tmpdir.as_cwd():
        with mock.patch.dict(os.environ, env, clear=True):
            key = ApiKey.from_sources()
            assert key.is_demo_key()
            assert key.source == "demo"


def test_read_first_missing(tmpdir):
    with tmpdir.as_cwd():
        assert _find_first_of(["foo.txt"]) is None
        assert _find_first_of([]) is None


def test_read_first_file(tmpdir):
    with tmpdir.as_cwd():
        with open("foo.txt", "w") as fp:
            fp.write("foo")
        with open("bar.txt", "w") as fp:
            fp.write("bar")

        assert _find_first_of(["foo.txt", "bar.txt"]).name == "foo.txt"
        assert _find_first_of(["bar.txt", "foo.txt"]).name == "bar.txt"


def test_use_demo_key_is_a_string():
    key = ApiKey(ApiKey.DEMO_API_KEY, source="demo")
    assert len(key) > 0
    assert key.source == "demo"
    assert key.is_demo_key()


def test_use_demo_key_issues_warning():
    with pytest.warns(UserWarning):
        ApiKey(ApiKey.DEMO_API_KEY)


def test_api_key_repr():
    key = ApiKey("foobar")
    assert eval(repr(key)) == key
