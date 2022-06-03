class BmiTopographyError(Exception):

    """Base exception for all bmi_topography errors."""

    pass


class MissingKeyError(BmiTopographyError):

    """Raise if an API key cannot be found."""

    pass


class BadKeyError(BmiTopographyError):

    """Raise for an invalid key."""

    pass


class BadApiKeySource(BmiTopographyError):

    """Raise for an invalid API key source."""

    pass
