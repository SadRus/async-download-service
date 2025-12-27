import asyncio
import os

import aiofiles
from aiohttp import web

BUFFER_SIZE = 300  # bytes


async def archive(request):
    response = web.StreamResponse()
    response.headers.update({
        'Content-Type': 'application/zip',
        'Content-Disposition': 'attachment; filename="archive.zip"',
    })

    folder_name = request.match_info.get('archive_hash', 'unknown_hash')
    folder_path = os.path.join(os.getcwd(), 'test_photos', folder_name)
    if not os.path.exists(folder_path):
        return web.HTTPNotFound(text="Архив не существует или был удален")

    command_args = ['-r', '-', '.']

    archive_process = await asyncio.create_subprocess_exec(
        'zip',
        *command_args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=folder_path,
    )

    await response.prepare(request)
    while not archive_process.stdout.at_eof():
        message = await archive_process.stdout.read(n=BUFFER_SIZE*1024)
        await response.write(message)

    return response


async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


if __name__ == '__main__':
    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archive),
    ])
    web.run_app(app)
