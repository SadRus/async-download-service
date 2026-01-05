from argparse import ArgumentParser


def create_argparser() -> ArgumentParser:
    parser = ArgumentParser()
    parser.add_argument(
        '-dl',
        '--disable-logging',
        action='store_true',
        dest='logging_disabled',
        help='Disable logging',
    )
    parser.add_argument(
        '-d',
        '--response-delay',
        default=0,
        type=int,
        dest='delay',
        help='Archive chunk response delay',
    )
    parser.add_argument(
        '-p',
        '--path',
        default='photos',
        type=str,
        dest='path',
        help='Path to photos root folder',
    )
    return parser
