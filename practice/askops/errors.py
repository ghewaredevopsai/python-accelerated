"""The AskOps exception hierarchy.

One base class, so a caller can catch everything AskOps raises with a single `except AskOpsError`
and still let genuine bugs (TypeError, AttributeError...) crash loudly.

TODO(mission 2): add
  * RunbookNotFound - raised when a runbook id does not exist. Keep the id on the exception
    as `.runbook_id`, and make str(exc) mention it.
  * DataError       - raised when a data file is missing or is not valid JSON. The message
    must include the file path, or the person on call cannot fix it.
"""


class AskOpsError(Exception):
    """Base class for every error AskOps raises on purpose."""
