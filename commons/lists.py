from typing import Callable

from commons.optional import of, Optional, empty


def find_item(items: list[any], predicate: Callable) -> Optional:
    for item in items:
        if predicate(item):
            return of(item)
    return empty()
