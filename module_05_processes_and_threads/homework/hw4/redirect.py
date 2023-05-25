import sys
import traceback
from types import TracebackType
from typing import Type, IO, Optional, Literal


class Redirect:
    """Context manager to redirect stdout
    and stderr to specified IO objects."""

    def __init__(self, stdout: IO = None, stderr: IO = None) -> None:
        """
        Constructor of the Redirect context manager.
        :param stdout: IO object for stdout
        :param stderr: IO object for stderr
        """
        self.stdout = stdout
        self.stderr = stderr
        self.original_stdout = sys.stdout
        self.original_stderr = sys.stderr

    def __enter__(self):
        """The function redirects threads if they are specified."""

        if self.stdout is not None:
            sys.stdout = self.stdout
        if self.stderr is not None:
            sys.stderr = self.stderr

    def __exit__(
            self,
            exc_type: Optional[Type[BaseException]],
            exc_val: Optional[BaseException],
            exc_tb: Optional[TracebackType]
    ) -> Literal[True]:
        """If error was raised the function shows traceback in current stderr.
        Then current threads switch in original ones
        (if threads were switched)."""

        if exc_type is not None:
            sys.stderr.write(traceback.format_exc())

        if self.stdout is not None:
            sys.stdout = self.original_stdout
        if self.stderr is not None:
            sys.stderr = self.original_stderr

        return True


# print('Hello stdout')
# stdout_file = open('stdout.txt', 'w')
# stderr_file = open('stderr.txt', 'w')
#
# with Redirect(stdout=stdout_file, stderr=stderr_file):
#     print('Hello stdout.txt')
#     raise Exception('Hello stderr.txt')
#
# print('Hello stdout again')
# raise Exception('Hello stderr')
