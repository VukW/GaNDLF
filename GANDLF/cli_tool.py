import logging

import click

from GANDLF.entrypoints import append_copyright_to_help
from GANDLF.entrypoints.anonymizer import new_way as anonymizer_command
from GANDLF.entrypoints.run import new_way as run_command
from GANDLF.entrypoints.constructCSV import new_way as construct_csv_command
from GANDLF.entrypoints.collectStats import new_way as collect_stats_command
from GANDLF.entrypoints.patchMiner import new_way as path_miner_command
from GANDLF.entrypoints.preprocess import new_way as preprocess_command
from GANDLF.entrypoints.verifyInstall import new_way as verify_install_command
from GANDLF.entrypoints.configGenerator import new_way as config_generator_command
from GANDLF.entrypoints.recoverConfig import new_way as recover_config_command
from GANDLF.entrypoints.deploy import new_way as deploy_command
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
gandlf.add_command(collect_stats_command, 'collect-stats')
gandlf.add_command(path_miner_command, 'path-miner')
gandlf.add_command(preprocess_command, 'preprocess')
gandlf.add_command(verify_install_command, 'verify-install')
gandlf.add_command(config_generator_command, 'config-generator')
gandlf.add_command(recover_config_command, 'recover-config')
gandlf.add_command(deploy_command, 'deploy')

if __name__ == '__main__':
    gandlf()
