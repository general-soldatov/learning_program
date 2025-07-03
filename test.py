import click

@click.group()
def cli():
    pass

@cli.command("comp")
def comp():
    print('comp')

@cli.command("project")
def project():
    print('project')

if __name__ == '__main__':
    cli()
