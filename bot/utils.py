import re

import inflect

inflector = inflect.engine()


def pascal_to_snake(text: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


def pluralize(text: str) -> str:
    is_singular = inflector.singular_noun(text) is False
    return inflector.plural_noun(text) if is_singular else text
