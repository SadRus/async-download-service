import asyncio
import os
import logging
from functools import partial

import aiofiles
from aiohttp import web
from dotenv import load_dotenv

from argparser import create_argparser

ARCHIVE_FILENAME = 'archive.zip'
CHUNK_SIZE = 300 * 1024  # bytes

_logger = logging.getLogger()


async def archive(request: web.Request, delay: int, path: str) -> web.StreamResponse:
    response = web.StreamResponse()
    response.headers.update({
        'Content-Type': 'application/zip',
        'Content-Disposition': f'attachment; filename={ARCHIVE_FILENAME}',
    })

    folder_name = request.match_info.get('archive_hash', 'unknown_hash')
    folder_path = os.path.join(os.getcwd(), path, folder_name)
    if not os.path.exists(folder_path):
        return web.HTTPNotFound(text='Архив не существует или был удален')

    command_args = ('-r', '-', '.')

    process = await asyncio.create_subprocess_exec(
        'zip',
        *command_args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=folder_path,
    )

    await response.prepare(request)
    try:
        while not process.stdout.at_eof():
            message = await process.stdout.read(n=CHUNK_SIZE)
            await response.write(message)
            _logger.info('Sending archive chunk...')
            await asyncio.sleep(delay)

    except ConnectionResetError as err:
        _logger.warning(f'Download was interrupted: {err}')

    except BaseException as err:
        _logger.error(err)

    finally:
        if process.returncode is None:
            process.terminate()
        else:
            process.kill()
            await process.communicate()

    return response


async def handle_index_page(request: web.Request) -> web.Response:
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    load_dotenv()

    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s: %(message)s',
    )

    parser = create_argparser()
    parsed_args = parser.parse_args()

    _logger.disabled = parsed_args.logging_disabled

    archive = partial(archive, delay=parsed_args.delay, path=parsed_args.path)

    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archive),
    ])
    web.run_app(app)
