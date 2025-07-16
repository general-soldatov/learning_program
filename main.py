import click
import shutil
from typing import Tuple
from app.abstract import create_division
from app.ai import AIPrompter
from app.parser import  ProjectReader, ParseShedule
from app.word_template import WorkPlan, AppraisalFunds, Metodical

@click.group()
def cli():
    pass

DATA_PROG = {
    'start': 'start program'.upper(),
    'end': 'end program'.upper()
}

TEMPLATE = 'C:/Users/Юрий Солдатов/PycharmProjects/learning_program/projects/template.yaml'

def start(path: str) -> Tuple[ProjectReader, ParseShedule]:
    click.echo(create_division(DATA_PROG['start']))
    data_yaml = ProjectReader(path)
    click.echo(create_division('Open Exel File'.upper(), '*'))
    shedule = ParseShedule(data_yaml.paths.shedule, name='План')
    shedule.search_code(data_yaml.program.code)
    data_yaml.import_data()
    return data_yaml, shedule

@cli.command("create", help="Copy template of project to locale directory")
@click.option("--path", prompt="Path", default='')
@click.option("--name", prompt="Name", default='project')
def copy_template(path, name):
    click.echo(create_division(DATA_PROG['start']))
    click.echo(create_division('Create project'.upper(), '*'))
    project_name = f"{path}{'/' if path != '' else ''}{name}.yaml"
    # data_yaml = ProjectReader(TEMPLATE)
    if click.confirm(f"Do you really want to create a project {project_name}"):
        # data_yaml.recording(project_name)
        shutil.copy(TEMPLATE, project_name)
    else:
        click.echo("Aborted!")
    click.echo('\n' + create_division(DATA_PROG['end']))

@cli.command("preview", help="Preview the project")
@click.option("--path", prompt="Path", default=TEMPLATE)
def preview(path):
    data_yaml, shedule = start(path)
    shedule.search_competition()
    shedule.search_semester()
    semesters = ', '.join(map(str, shedule.data_course.keys()))
    click.echo(create_division("Data of discipline:".upper(), '*'))
    click.echo(f'Discipline: "{shedule.name}"\nSemesters: {semesters}')
    click.echo('Selected competition:')
    for key, value in shedule.abstract_of_competition.items():
        click.echo(create_division(key, division='>'))
        click.echo(value['text'])
    ai = AIPrompter(data_yaml, shedule)
    click.echo('\n' + create_division('EXPORT PROMPTS TO LLM', '>'))
    ai.export_prompt()
    click.echo('\n' + create_division(DATA_PROG['end']))

@cli.command("project", help="Build the project")
@click.option("--path", prompt="Path", default=TEMPLATE)
def project(path):
    data_yaml, shedule = start(path)
    if click.confirm(f"Do you really want to complile the project {path}"):
        click.echo("Create document: Work Plan")
        wp = WorkPlan(data_yaml.program, path_doc=data_yaml.paths.work_program, path=data_yaml.paths.folder)
        wp.add_with_project(data_yaml.themes, data_yaml.literatures, data_yaml.program, shedule)
        click.echo(wp.create_document())
        click.echo("Create document: Appraisal Funds")
        af = AppraisalFunds(data_yaml.program, path_doc=data_yaml.paths.appraisal_funds, path=data_yaml.paths.folder)
        af.add_with_project(data_yaml.program, shedule)
        click.echo(af.create_document())
        click.echo("Create document: Metodical")
        mw = Metodical(data_yaml.program, path_doc=data_yaml.paths.metodical, path=data_yaml.paths.folder)
        mw.add_with_project(data_yaml.themes, data_yaml.literatures, data_yaml.program, shedule)
        click.echo(mw.create_document())
    else:
        click.echo("Aborted!")
    click.echo('\n' + create_division(DATA_PROG['end']))


if __name__ == '__main__':
    cli()