from typing import Collection, Type, Literal
from types import TracebackType


class BlockErrors:
    def __init__(self, error_types: Collection) -> None:
        self.error_types = error_types

    def __enter__(self) -> None:
        pass

    def __exit__(
            self,
            exc_type: Type[BaseException] | None,
            exc_val: BaseException | None,
            exc_tb: TracebackType | None
    ) -> Literal[True] | None:
        if exc_type is not None and exc_type not in self.error_types:
            return False  # Прокидываем исключение выше
        return True  # Игнорируем исключение
