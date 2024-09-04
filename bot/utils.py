import re
from typing import TypeVar

import inflect

inflector = inflect.engine()


def pascal_to_snake(text: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


def pluralize(text: str) -> str:
    plural_form = inflector.plural_noun(text)
    return text if plural_form.endswith("ss") else plural_form


K = TypeVar("K")
V = TypeVar("V")


def get_key_by_value(dict_: dict[K, V], target_value: V) -> K | None:
    return next((key for key, value in dict_.items() if value == target_value), None)
