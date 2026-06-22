class DuplicateNodeError(RuntimeError):
    """Raised when duplicate nodes are found."""

    def __init__(self, message: str):
        """
        Error constructor.

        :param message: error message.
        """

        super().__init__(message)
