import click


def sync_options(func):
    """
    Add all of the sync options to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    options = [
        sync_source_option,
        sync_destination_option
    ]

    for option in reversed(options):
        func = option(func)

    return func


def sync_source_option(func):
    """
    Add the sync source option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--src', '-s',
        'sync_source',
        help='Local directory from which to sync.'
    )(func)


def sync_destination_option(func):
    """
    Add the sync destination option to the decorated command func.

    :param func: Click CLI command to decorate
    :return: decorated CLI command
    """
    return click.option(
        '--dest', '-d',
        'sync_destination',
        help='Remote directory to sync to.'
    )(func)
