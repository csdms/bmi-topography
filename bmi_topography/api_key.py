import os
import warnings
from functools import partial
from pathlib import Path

from .errors import BadKeyError, MissingKeyError


class ApiKey:
    DEMO_API_KEY = "demoapikeyot2022"
    API_KEY_FILES = (".opentopography.txt", "~/.opentopography.txt")
    API_KEY_ENV_VAR = "OPENTOPOGRAPHY_API_KEY"

    def __init__(self, api_key, source="user"):
        if not isinstance(api_key, str) or len(api_key) == 0:
            raise BadKeyError("invalid API key")
        self._api_key = api_key
        self._source = source

    @classmethod
    def from_env(cls):
        try:
            api_key = os.environ[ApiKey.API_KEY_ENV_VAR]
        except KeyError:
            raise MissingKeyError(f"unable to find key ({ApiKey.API_KEY_ENV_VAR})")
        else:
            return cls(api_key, source="env")

    @classmethod
    def from_file(cls):
        if filepath := find_first_of(ApiKey.API_KEY_FILES):
            with open(filepath, "r") as fp:
                api_key = fp.read().strip()
        else:
            raise MissingKeyError(
                f"unable to find key ({', '.join(ApiKey.API_KEY_FILES)})"
            )
        return cls(api_key, source=f"file:{filepath}")

    @classmethod
    def from_demo(cls):
        return cls(ApiKey.use_demo_key(), source="demo")

    @classmethod
    def from_sources(cls, api_key=None):
        for from_source in [partial(cls, api_key), cls.from_env, cls.from_file]:
            try:
                return from_source()
            except (BadKeyError, MissingKeyError):
                pass
        return cls.from_demo()

    @property
    def api_key(self):
        return self._api_key

    @property
    def source(self):
        """Where the API key came from."""
        return self._source

    @staticmethod
    def use_demo_key():
        warnings.warn(
            "You are using a demo key to fetch data from OpenTopography, functionality "
            "will be limited. See https://bmi-topography.readthedocs.io/en/latest/#api-key "
            "for more information."
        )
        return ApiKey.DEMO_API_KEY

    def is_demo_key(self):
        return self._api_key == ApiKey.DEMO_API_KEY

    def __repr__(self):
        return f"ApiKey({self.api_key!r}, source={self.source!r})"

    def __str__(self):
        return self.api_key

    def __len__(self):
        return len(self.api_key)

    def __eq__(self, val):
        try:
            return self.api_key == val.api_key
        except AttributeError:
            return str(self) == val


def find_first_of(files):
    found = None
    for path in (Path(name) for name in files):
        if path.expanduser().is_file():
            found = path.expanduser()
            break
    return found
