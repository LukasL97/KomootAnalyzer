from typing import TypeVar, List

T = TypeVar('T')


def flatten(lists: List[List[T]]) -> List[T]:
    return [item for l in lists for item in l]
