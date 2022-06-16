import os
import logging
import requests
import subprocess
from data import posts


logging.basicConfig(level=logging.INFO)

temp_path = os.path.join('/tmp', 'posts')
pwd = os.getcwd()
repo = 'KumaTea/blog'
media_file = 'media.zip'


def get_media(post_id):
    media_path = os.path.join(temp_path, post_id, media_file)
    os.makedirs(os.path.dirname(media_path), exist_ok=True)
    with open(media_path, 'wb') as f:
        r = requests.get(f'https://github.com/{repo}/releases/download/{post_id}/{media_file}')
        f.write(r.content)
    return logging.info(f'post {post_id} downloaded')


def unzip_media(post_id):
    media_path = os.path.join(temp_path, post_id, media_file)
    destination = os.path.join(
        pwd,
        'posts',
        '{post_id}-{title}'.format(
            post_id=post_id,
            title=posts[post_id]['name']
        )
    )
    os.makedirs(destination, exist_ok=True)
    subprocess.run(['unzip', media_path, '-d', destination])
    return logging.info(f'post {post_id} unzipped')


if __name__ == '__main__':
    logging.info('creating temp directory')
    os.makedirs(temp_path, exist_ok=True)
    for pid in posts:
        get_media(pid)
        unzip_media(pid)

    subprocess.run(['rm', '-rvf', temp_path])
    logging.info('done')
