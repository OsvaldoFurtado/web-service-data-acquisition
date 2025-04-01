"""

Project: A template for Data Acquisition projects

"""
from dataclasses import dataclass
from typing import TypeAlias


@dataclass
class XYPair:
    x: str
    y: str


@dataclass
class SomeOtherStructure:
    x: list[str]
    y: list[str]


RawData: TypeAlias = XYPair | SomeOtherStructure