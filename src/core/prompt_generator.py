import logging
import re
import os
from typing import Generator

from math import prod
from itertools import product


__all__ = ["SomethingGenerator", "PromptGenerator", "find_possible_topics_file_paths", "find_possible_sentiments_file_paths"]

is_whitespace = re.compile(r"\s+").match


def __find_possible_something_file_paths(names: set[str]) -> list[str]:
    # list of filenames to search for w/o extension
    pfp = []

    for root, dirs, files in os.walk(os.getcwd(), topdown=True):
        dirs[:] = list(filter(lambda d: not d.startswith((".", "__")), dirs))  # ignore hidden directories
        for file in files:
            if file.endswith(".py"):  # ignore python files (e.g. "topics.py")
                continue
            name, ext = os.path.splitext(os.path.basename(file))
            if ext.lower().endswith("txt") and name in names:
                pfp.append(os.path.join(root, file))
    return pfp


def find_possible_topics_file_paths () -> list[str]:
    return __find_possible_something_file_paths({"topics", "list", "subjects"})

def find_possible_sentiments_file_paths () -> list[str]:
    return __find_possible_something_file_paths({"sentiments", "feelings", "emotions"})

class SomethingGenerator:
    def __init__(self, filepath: str) -> None:
        self.logger = logging.getLogger("generator")
        self.__path = filepath
        self.__count: int = None

    def __iter__(self) -> Generator[str, None, None]:
        with open(self.__path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not is_whitespace(line):
                    yield line

    @property
    def count(self) -> int:
        if self.__count is None:
            self.__count = sum(1 for _ in self)
        return self.__count


class PromptGenerator:
    def __init__(self, *args: SomethingGenerator) -> None:
        self.logger = logging.getLogger("prompt_generator")
        self.__generators = args
        self.__count: int = None

    def __iter__(self) -> Generator[tuple[str, ...], None, None]:
        for p in product(*self.__generators):
            yield p

    @property
    def count(self) -> int:
        if self.__count is None:
            self.__count = prod(g.count for g in self.__generators)
        return self.__count
