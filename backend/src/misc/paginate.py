from typing import Any, List
# import pytest
from math import ceil


class Paginador:
    def __init__(self, data: List[Any], offset: int = 1, limit: int = 0):
        self.data = data
        self._offset = offset
        self.limit = limit

    @property
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, offset):
        if not (0 < offset < self.get_number_of_pages()):
            raise ValueError("Offset deve ser valido!")

        self._offset = offset

    @property
    def limit(self):
        return self._limit

    @limit.setter
    def limit(self, limit):
        if limit < 0:
            raise ValueError("Limite deve ser valido!")
        self._limit = limit

    def get_number_of_pages(self) -> int:
        if self.limit == 0:
            return len(self.data)

        if len(self.data) < self.limit:
            return 1

        return ceil(len(self.data) / self.limit)

    def paginate(self) -> List[Any]:
        if self.limit == 0:
            return self.data[:]

        start = self.limit * (self.offset - 1)
        end = self.limit + start

        return self.data[start:end]

    def get_response(self):
        return {
            'limit': self.limit,
            'offset': self.offset,
            'length': self.get_number_of_pages(),
            'payload': self.paginate()
        }
