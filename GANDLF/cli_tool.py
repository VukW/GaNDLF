import click
from GANDLF.entrypoints.anonymizer import new_way as anonymizer_command


@click.group()
def gandlf():
    """GANDLF command-line tool."""
    pass


gandlf.add_command(anonymizer_command, 'anonymizer')

if __name__ == '__main__':
    gandlf()
