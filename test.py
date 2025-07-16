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
import json
from string import ascii_uppercase
from app.parser import ProjectReader, ParseShedule
from app.ai import AIPrompter


TEMPLATE = 'C:/Users/Юрий Солдатов/PycharmProjects/learning_program/projects/template.yaml'

def start(path: str):
    # click.echo(create_division(DATA_PROG['start']))
    data_yaml = ProjectReader(path)
    # click.echo(create_division('Open Exel File'.upper(), '*'))
    shedule = ParseShedule(data_yaml.paths.shedule, name='План')
    shedule.search_code(data_yaml.program.code)
    data_yaml.import_data()
    return data_yaml, shedule

data_yaml, shedule = start(TEMPLATE)


# questions = data_yaml._data['questions']['9']
# for i, elem in enumerate(questions['discussions'], 1):
#     print(f'{i}. {elem}')

# test = data_yaml._data['test']['9']

# for i, item in enumerate(test["test_tasks"], 1):
#     print(i, item['question'])
#     answer_true = item['answer']
#     for answer in item['options']:
#         print(answer)
#     print('True answer:', answer_true)

# comparison = test.get("matching_task", None)

# if comparison:
#     print(comparison['task'])
#     text = '\n'.join((f'{letter}. {elem}' for elem, letter in zip(comparison['terms'], ascii_uppercase)))
#     numbers = list(range(1, len(comparison['definitions']) + 1))
#     random.shuffle(numbers)
#     answer_true = ', '.join([f'{letter}-{num}'
#                               for letter, num in zip(ascii_uppercase, numbers)])
#     answers = {}
#     for elem, i in zip(comparison['definitions'], numbers):
#         answers[i] = elem
#     text += '\n\n'
#     text += '\n'.join((f'{i}. {x}' for i, x in sorted(answers.items(), key=lambda a: a[0])))
#     print(text)
#     print('True answer', answer_true)

# sequence = test.get("sequence_task", None)
# if sequence:
#     print(sequence['task'])
#     numbers = list(range(1, len(sequence['steps']) + 1))
#     random.shuffle(numbers)
#     answers = {}
#     for elem, i in zip(sequence['steps'], numbers):
#         answers[i] = elem
#     text = '\n'.join((f'{i}. {x}' for i, x in sorted(answers.items(), key=lambda a: a[0])))
#     print(text)
#     answer_true = ', '.join(map(str, numbers))
#     print('True answer', answer_true)

# for i, elem in enumerate(questions['questions'], 1):
#     print(f'{i}. {elem}')