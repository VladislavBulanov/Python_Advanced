from typing import Collection, Type, Optional
from types import TracebackType


class BlockErrors:
    """The context manager for blocking specified errors."""

    def __init__(self, error_types: Collection) -> None:
        """
        The class' constructor.
        :param error_types: specified errors
        """

        self.error_types = error_types

    def __enter__(self) -> None:
        pass

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> Optional[bool]:
        """
        The function blocks error if this error is one of specified.
        :param exc_type: type of exception
        :param exc_val: value of exception
        :param exc_tb: traceback of exception
        """

        if exc_type is not None and issubclass(exc_type, tuple(self.error_types)):
            return True
