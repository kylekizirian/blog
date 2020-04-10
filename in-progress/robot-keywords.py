#!/usr/bin/python
import inspect
import re
from collections import namedtuple

import robot
from robot.api import deco


class Arithmetic:

    def __init__(self):
        pass

    @deco.keyword("Add ${first} and ${second}")
    def add(self, first: float, second: float) -> float:
        return float(first) + float(second)

    @deco.keyword("Subtract ${first} from ${second}")
    def subtract(self, first: float, second: float) -> float:
        return float(second) - float(first)

    @deco.keyword("Multiply ${first} and ${second}")
    def multiply(self, first: float, second: float) -> float:
        return float(first) * float(second)

Keyword = namedtuple("Keyword", ["name", "function"])

def get_keywords(obj):
    """Given an object, return all robot keywords associated with it

    Keywords have a `robot_name` attribute associated with them.
    """
    obj_methods = [i[1] for i in inspect.getmembers(obj, predicate=inspect.ismethod)]
    keywords = [
        Keyword(getattr(obj_method, 'robot_name'), obj_method)
        for obj_method in obj_methods
        if hasattr(obj_method, 'robot_name')
    ]
    return keywords


if __name__ == "__main__":

    obj = Arithmetic()
    keywords = get_keywords(obj)
    keywords_with_regex = []

    add_example = "Add 1 and 2"

    for keyword in keywords:
        foo = re.sub("\$\{.+?\}", "(.*)", keyword.name)
        foo = "^" + foo + "$"
        keywords_with_regex.append(Keyword(foo, keyword.function))

    # does add_example match any of these regexes?
    matching_keywords = [keyword for keyword in keywords_with_regex if re.fullmatch(keyword.name, add_example)]

    if len(matching_keywords) != 1:
        raise Exception

    kw = matching_keywords[0]

    groups = re.fullmatch(kw.name, add_example)
    breakpoint()
    print(kw.function(*groups.groups()))

