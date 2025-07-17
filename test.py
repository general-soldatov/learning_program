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


import json
from app.parser import ProjectReader, ParseShedule
from app.ai import AIPrompter, AITester


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







# for i, elem in enumerate(questions['questions'], 1):
#     print(f'{i}. {elem}')

ai = AITester(data_yaml)
test = ai.build()
print(test, sep='\n')