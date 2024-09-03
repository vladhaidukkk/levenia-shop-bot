import re
from typing import TypeVar

import inflect

inflector = inflect.engine()


def pascal_to_snake(text: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


def pluralize(text: str) -> str:
    is_singular = inflector.singular_noun(text) is False
    return inflector.plural_noun(text) if is_singular else text


K = TypeVar("K")
V = TypeVar("V")


def get_key_by_value(dict_: dict[K, V], target_value: V) -> K | None:
    return next((key for key, value in dict_.items() if value == target_value), None)
