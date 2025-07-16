# import click

# @click.group()
# def cli():
#     pass

# @cli.command("comp")
# def comp():
#     print('comp')

# @cli.command("project")
# def project():
#     print('project')

# if __name__ == '__main__':
#     cli()

PROMPT_QUESTIONS = """
"messages": [
    {
      "role": "system",
      "text": "Ты преподаватель и автор методического пособия по дисциплине '{name}'. Ответ должен быть представлен в формате json, где ключи будут номера тем типа '1'."
    },
    {
      "role": "user",
      "text": "Напиши задания в рамках тем:
{themes}
Для каждой темы должно быть 5 вопросов для обсуждения в дискуссии и 5 вопросов для ответа на семинарах в формате: {"1": {"questions": ["Перечень вопросов", ...], "discussions": ["Перечень вопросов", ...]} ...}"
}
]
"""
PROMPT_TEST = '''
"messages": [
    {
      "role": "system",
      "text": "Ты преподаватель и автор методического пособия по дисциплине '{name}'. Ответ должен быть представлен в формате json, где ключи будут номера тем типа '1'."
    },
    {
      "role": "user",
      "text": "Напиши задания в рамках тем:
{themes}
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

import random
from string import ascii_uppercase
from app.parser import ProjectReader

TEMPLATE = 'C:/Users/Юрий Солдатов/PycharmProjects/learning_program/projects/template.yaml'

data_yaml = ProjectReader(TEMPLATE)

def themes_plan(themes: list, division: int):
    volume_last: list = []
    themes_ = [themes[:division], themes[division:]]
    volume_last.append({i+1: themes_[0][i] for i in range(division)})
    volume_last.append({i+1: themes_[1][i-division] for i in range(division, len(themes))})
    return volume_last

questions = data_yaml._data['questions']['9']
for i, elem in enumerate(questions['discussions'], 1):
    print(f'{i}. {elem}')

test = data_yaml._data['test']['9']

for i, item in enumerate(test["test_tasks"], 1):
    print(i, item['question'])
    answer_true = item['answer']
    for answer in item['options']:
        print(answer)
    print('True answer:', answer_true)

comparison = test.get("matching_task", None)

if comparison:
    print(comparison['task'])
    text = '\n'.join((f'{letter}. {elem}' for elem, letter in zip(comparison['terms'], ascii_uppercase)))
    numbers = list(range(1, len(comparison['definitions']) + 1))
    random.shuffle(numbers)
    answer_true = ', '.join([f'{letter}-{num}'
                              for letter, num in zip(ascii_uppercase, numbers)])
    answers = {}
    for elem, i in zip(comparison['definitions'], numbers):
        answers[i] = elem
    text += '\n\n'
    text += '\n'.join((f'{i}. {x}' for i, x in sorted(answers.items(), key=lambda a: a[0])))
    print(text)
    print('True answer', answer_true)

sequence = test.get("sequence_task", None)
if sequence:
    print(sequence['task'])
    numbers = list(range(1, len(sequence['steps']) + 1))
    random.shuffle(numbers)
    answers = {}
    for elem, i in zip(sequence['steps'], numbers):
        answers[i] = elem
    text = '\n'.join((f'{i}. {x}' for i, x in sorted(answers.items(), key=lambda a: a[0])))
    print(text)
    answer_true = ', '.join(map(str, numbers))
    print('True answer', answer_true)

for i, elem in enumerate(questions['questions'], 1):
    print(f'{i}. {elem}')