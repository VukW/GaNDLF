import click
from functools import update_wrapper
from GANDLF.cli import copyrightMessage


def append_copyright_to_help(command_func):
    def new_command_func(*args, **kwargs):
        # used to append copyright message to command help
        command_func.__doc__ += "\n\n" + copyrightMessage

        return command_func(*args, **kwargs)

    return update_wrapper(new_command_func, command_func)


class ParamNamesFilter:
    """Given a list of param aliases, returns either all or all-except-last depending on old_way_flag"""
    def __init__(self, old_way_flag: bool):
        self.old_way_flag = old_way_flag

    def __call__(self, *params: str) -> tuple[str]:
        """
        Args:
            params (tuple[str]): List of aliases for the param. The latest one is assumed to be an camelCase old-way
             name. It would be returned only if `old_way_flag` is True
        """
        if self.old_way_flag:
            return params
        else:
            return params[:-1]
