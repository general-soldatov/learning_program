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

import random
from string import ascii_uppercase
from app.parser import ProjectReader

TEMPLATE = 'C:/Users/Юрий Солдатов/PycharmProjects/learning_program/projects/template.yaml'

data_yaml = ProjectReader(TEMPLATE)
test = data_yaml._data['test']['Тема 9']

for i, item in enumerate(test["Тестовые задачи"], 1):
    print(i, item['Вопрос'])
    answer_true = None
    for j, answer in enumerate(item['Варианты ответов'], 1):
        print(f'{j}. {answer}')
        if answer == item['Правильный ответ']:
            answer_true = j
    print('True answer:', answer_true)

comparison = test.get("Задача на сопоставление", None)

if comparison:
    data = tuple(comparison.values())
    print(data[0])
    text = '\n'.join((f'{letter}. {elem}' for elem, letter in zip(data[1], ascii_uppercase)))
    numbers = list(range(1, len(data[2]) + 1))
    random.shuffle(numbers)
    answer_true = ', '.join([f'{letter}-{num}'
                              for letter, num in zip(ascii_uppercase, numbers)])
    answers = {}
    for elem, i in zip(data[2], numbers):
        answers[i] = elem
    text += '\n\n'
    text += '\n'.join((f'{i}. {x}' for i, x in sorted(answers.items(), key=lambda a: a[0])))
    print(text)
    print('True answer', answer_true)

sequence = test.get("Задача на последовательность", None)
if sequence:
    data = tuple(sequence.values())
    print(data[0])
    numbers = list(range(1, len(data[1]) + 1))
    random.shuffle(numbers)
    answers = {}
    for elem, i in zip(data[1], numbers):
        answers[i] = elem
    text = '\n'.join((f'{i}. {x}' for i, x in sorted(answers.items(), key=lambda a: a[0])))
    print(text)
    answer_true = ', '.join(map(str, numbers))
    print('True answer', answer_true)
