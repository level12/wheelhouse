import logging

import click

from .config import Config
from wheelhouse import core

VERBOSE = False


@click.group()
@click.option('-v', '--verbose', is_flag=True)
def wheelhouse(verbose):
    global VERBOSE
    VERBOSE = verbose
    logging_level = logging.INFO if verbose else logging.WARN
    logging.basicConfig(level=logging_level)


@wheelhouse.command()
@click.argument('packages', nargs=-1)
def build(packages):
    config = Config(verbose=VERBOSE)
    if not packages:
        core.build_files(config)
    else:
        core.build_packages(config, packages)


@wheelhouse.command()
def config():
    config = Config(verbose=VERBOSE)

    click.echo('Config search paths searched:')
    for val in config.search_fpaths():
        click.echo('    {}'.format(val))

    click.echo('Config files used (higher precidence last):')
    for val in config.found_fpaths:
        click.echo('    {}'.format(val))

    click.echo('Config values:')
    if config.project_root_dpath is None:
        click.echo('    Error: no project wheelhouse.ini file found')
    else:
        click.echo('    project root = {}'.format(config.project_root_dpath))
        click.echo('    requirements root = {}'.format(config.requirements_dpath))
        click.echo('    wheelhouse root = {}'.format(config.wheelhouse_dpath))

        click.echo('    [wheelhouse]')
        click.echo('        requirement_files = {}'.format(config.requirement_files))
        click.echo('        pip_bins = {}'.format(config.pip_bins))


@wheelhouse.command()
def prune():
    config = Config(verbose=VERBOSE)
    will_remove = core.prune_list(config)
    for fpath in will_remove:
        print fpath.name
    response = click.confirm('Delete all the above wheels?')
    if response:
        for fpath in will_remove:
            fpath.unlink()
