from dataclasses import dataclass
from typing import List, Dict

PROMPT = {
    "messages": [
        {
        "role": "system",
        "text": ""
        },
        {
        "role": "user",
        "text": ""
        }
    ]
}

ROLE = "Ты преподаватель и автор методического пособия по дисциплине '{name}'. Ответ должен быть представлен в формате json, где ключи будут номера тем типа '1'."
THEMES = "Напиши задания в рамках тем: {themes} \n"
QUESTION = "Для каждой темы должно быть 5 вопросов для обсуждения в дискуссии и 5 вопросов для ответа на семинарах в формате: {'1': {'questions': ['Перечень вопросов', ...], 'discussions': ['Перечень вопросов', ...]} ...}"
TEST = '''
Для каждой темы должно быть 5 тестовых задач с четырьмя вариантами ответов в формате: "test_tasks": [{
        "question": "Вопрос",
        "options": ["Буква. Вариант ответа", ... ],
        "answer": "Буква правильного ответа"
      }, ...], дополнительно для каждой темы нужна одна задача на сопоставление терминов в формате "matching_task": {
      "task": "Текст задачи",
      "terms": ["Термины", ... ],
      "definitions": ["Ответы в правильном порядке", ... "]
    } или выставление правильного порядка последовательности в формате "sequence_task": {
      "task": "Название.",
      "steps": ["Ответы в правильном порядке", ..."]
    } "
    }
  ]
'''


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