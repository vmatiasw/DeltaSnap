from __future__ import annotations
from typing import Any


class BaseData:
    def __init__(self, data: Any):
        self.data = data

    def __str__(self) -> str:
        return f"{self.data}"

    def __repr__(self) -> str:
        return f"{self.data}"

    def __eq__(self, other: Any) -> bool:
        return self.data == other

    def __bool__(self) -> bool:
        return bool(self.data)

    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index: int) -> Any:
        return self.data[index]

    def __setitem__(self, index: int, value: Any) -> None:
        self.data[index] = value

    def __contains__(self, item: Any) -> bool:
        return item in self.data

    def __iter__(self):
        return iter(self.data)

    def __delitem__(self, index: int) -> None:
        del self.data[index]
