import click
from typing import Tuple
from app.abstract import create_division
from app.parser import  ProjectReader, ParseShedule
from app.word_template import WorkPlan, AppraisalFunds, Metodical

@click.group()
def cli():
    pass

DATA_PROG = {
    'start': 'start program'.upper(),
    'end': 'end program'.upper()
}

def start(path: str) -> Tuple[ProjectReader, ParseShedule]:
    click.echo(create_division(DATA_PROG['start']))
    data_yaml = ProjectReader(path)
    click.echo(create_division('Open Exel File'.upper(), '*'))
    shedule = ParseShedule(data_yaml.paths.shedule, name='План')
    shedule.search_code(data_yaml.program.code)
    data_yaml.import_data()
    return data_yaml, shedule

@cli.command("preview")
@click.option("--path", prompt="Path", default='projects/databases.yaml')
def prewiew(path):
    _, shedule = start(path)
    shedule.search_competition()
    click.echo(create_division("Selected competition:".upper(), '*'))
    for key, value in shedule.abstract_of_competition.items():
        click.echo(key)
        click.echo(create_division(division='-'))
        click.echo(value['text'])
    click.echo(create_division(DATA_PROG['end']))

@cli.command("project")
@click.option("--path", prompt="Path", default='projects/databases.yaml')
def project(path):
    data_yaml, shedule = start(path)
    if click.confirm(f"Do you really want to create a project {path}"):
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
    click.echo(create_division(DATA_PROG['end']))


if __name__ == '__main__':
    cli()