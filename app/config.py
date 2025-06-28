from dataclasses import dataclass
from typing import List, Dict

@dataclass
class Paths:
    folder: str
    shedule: str
    work_program: str
    appraisal_funds: str
    metodical: str

@dataclass
class Program:
    code: str
    target: str
    tasks: List[str]
    place_of_learning: Dict[str, Dict[str, str]]
    competition: List[str]
    type_: str

@dataclass
class Themes:
    list_of: list
    semester_division: int

@dataclass
class Literatures:
    basic: List[str]
    optional: List[str]