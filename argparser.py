import os

from argparse import ArgumentParser


def create_argparser() -> ArgumentParser:
    logging_disabled = os.getenv('LOGGING_DISABLED', 'False').lower() == 'true'
    delay = os.getenv('DELAY', 0)
    path = os.getenv('PHOTOS_PATH', 'photos')

    parser = ArgumentParser()

    parser.add_argument(
        '-ld',
        default=logging_disabled,
        type=bool,
        dest='logging_disabled',
        help='Disable logging',
    )
    parser.add_argument(
        '-d',
        default=delay,
        type=int,
        dest='delay',
        help='Archive chunk response delay',
    )
    parser.add_argument(
        '-p',
        default=path,
        type=str,
        dest='path',
        help='Path to photos root folder',
    )

    return parser
