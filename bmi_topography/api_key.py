import os
import warnings
from functools import partial
from pathlib import Path

from .errors import BadApiKeySource, BadKeyError, MissingKeyError


class ApiKey:

    """Store an API key to use when fetching topography data from OpenTopography.

    Parameters
    ----------
    api_key : str
        An API key as a (non-empty) string.
    source : str, optional
        A string that indicates where the key came from. Possible
        values are: *user*, *env*, *file*, and *demo*.

    Raises
    ------
    BadKeyError
        The provided API key is invalid.
    MissingKeyError
        A key could not be found in the usual places.
    BadApiKeySource
        An invalid source was provided.

    Examples
    --------
    >>> from bmi_topography.api_key import ApiKey
    >>> api_key = ApiKey("foobar")
    >>> api_key
    ApiKey('foobar', source='user')
    """

    DEMO_API_KEY = "demoapikeyot2022"
    API_KEY_FILES = (".opentopography.txt", "~/.opentopography.txt")
    API_KEY_ENV_VAR = "OPENTOPOGRAPHY_API_KEY"

    def __init__(self, api_key, source="user"):
        if not isinstance(api_key, str) or len(api_key) == 0:
            raise BadKeyError("invalid API key")
        self._api_key = api_key
        self._source = ApiKey._validate_source(source)

        if self.is_demo_key():
            warnings.warn(
                "You are using a demo key to fetch data from OpenTopography, functionality "
                "will be limited. See https://bmi-topography.readthedocs.io/en/latest/#api-key "
                "for more information."
            )

    @staticmethod
    def _validate_source(source):
        valid_sources = ["user", "env", "file", "demo"]
        if isinstance(source, str) and source.split(":")[0] in valid_sources:
            return source
        else:
            raise BadApiKeySource(
                f"{source}: Invalid source (not one of {', '.join(valid_sources)}"
            )

    @classmethod
    def from_env(cls):
        """Get the key from and environment variables."""
        try:
            api_key = os.environ[ApiKey.API_KEY_ENV_VAR]
        except KeyError:
            raise MissingKeyError(f"unable to find key ({ApiKey.API_KEY_ENV_VAR})")
        else:
            return cls(api_key, source="env")

    @classmethod
    def from_file(cls):
        """Read the key from a file."""
        if filepath := _find_first_of(ApiKey.API_KEY_FILES):
            with open(filepath, "r") as fp:
                api_key = fp.read().strip()
        else:
            raise MissingKeyError(
                f"unable to find key ({', '.join(ApiKey.API_KEY_FILES)})"
            )
        return cls(api_key, source=f"file:{filepath}")

    @classmethod
    def from_sources(cls, api_key=None):
        """Get a key from the first of a series of sources.

        Look for a key from the following sources, returning the first found:
        (1) provided by a user through the *api_key* keyword,
        (2) provided by an environment variable,
        (3) provided in a text file, and
        (4) use a demo key
        """
        for from_source in [partial(cls, api_key), cls.from_env, cls.from_file]:
            try:
                return from_source()
            except (BadKeyError, MissingKeyError):
                pass
        return cls(ApiKey.DEMO_API_KEY, source="demo")

    @property
    def api_key(self):
        """The API key."""
        return self._api_key

    @property
    def source(self):
        """Where the API key came from."""
        return self._source

    def is_demo_key(self):
        """Check if the key is a demo key."""
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


def _find_first_of(files):
    """Find the first existing file from a list of files."""
    found = None
    for path in (Path(name) for name in files):
        if path.expanduser().is_file():
            found = path.expanduser()
            break
    return found
