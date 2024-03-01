import logging

import click

from GANDLF.entrypoints import append_copyright_to_help
from GANDLF.entrypoints.anonymizer import new_way as anonymizer_command
from GANDLF.entrypoints.run import new_way as run_command
from GANDLF.entrypoints.constructCSV import new_way as construct_csv_command
from GANDLF import version


def setup_logging(loglevel):
    logging.basicConfig(level=loglevel.upper())


@click.group()
@click.version_option(version, '--version', '-v', message='GANDLF Version: %(version)s')
@click.option('--loglevel', default='INFO', help='Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)')
@click.pass_context  # Pass the context to subcommands
@append_copyright_to_help
def gandlf(ctx, loglevel):
    """GANDLF command-line tool.
    """
    ctx.ensure_object(dict)
    ctx.obj['LOGLEVEL'] = loglevel
    setup_logging(loglevel)


gandlf.add_command(anonymizer_command, 'anonymizer')
gandlf.add_command(run_command, 'run')
gandlf.add_command(construct_csv_command, 'construct-csv')

if __name__ == '__main__':
    gandlf()
