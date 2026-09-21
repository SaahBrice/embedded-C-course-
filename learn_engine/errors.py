class LearnError(Exception):
    """Base class for expected game errors."""


class CatalogError(LearnError):
    """The curriculum catalog is malformed."""


class ProgressError(LearnError):
    """Saved learner progress is malformed or cannot be persisted."""


class AttemptError(LearnError):
    """An attempt operation is invalid or unsafe."""


class RunnerError(LearnError):
    """A mission checker cannot be configured or executed."""
