import os
import re
import random
import string
import logging
import requests
import subprocess
import urllib.request
from data import posts


logging.basicConfig(level=logging.INFO)

temp_path = os.path.join('/tmp', 'posts')
pwd = os.getcwd()
repo = 'KumaTea/blog'
media_file = 'media.zip'


def get_media(post_id):
    temp_media_path = os.path.join(temp_path, post_id, media_file)
    os.makedirs(os.path.dirname(temp_media_path), exist_ok=True)
    with open(temp_media_path, 'wb') as f:
        r = requests.get(f'https://github.com/{repo}/releases/download/{post_id}/{media_file}')
        f.write(r.content)
    return logging.info(f'[media]\tpost {post_id} downloaded')


def unzip_media(post_id):
    temp_media_path = os.path.join(temp_path, post_id, media_file)
    post_name = '{post_id}-{title}'.format(post_id=post_id, title=posts[post_id]['name'])
    post_path = os.path.join(pwd, 'posts', post_name)
    os.makedirs(post_path, exist_ok=True)
    subprocess.run(['unzip', temp_media_path, '-d', post_path])
    return logging.info(f'[media]\tpost {post_id} unzipped')


def gen_uuid(length=4):
    # https://stackoverflow.com/a/56398787/10714490
    alphabet = string.ascii_lowercase + string.digits
    return ''.join(random.choices(alphabet, k=length))


def get_content_type(url):
    with urllib.request.urlopen(url) as response:
        return response.headers['content-type']


def get_external_media(post_id):
    used_uuid = []
    post_name = '{post_id}-{title}'.format(post_id=post_id, title=posts[post_id]['name'])
    post_file = os.path.join(pwd, 'posts', post_name, 'index.md')
    media_path = os.path.join(pwd, 'posts', post_name, 'img')
    os.makedirs(os.path.dirname(media_path), exist_ok=True)

    # media in markdown: ![description](link)
    media_regex = r'!\[.*\]\((.*)\)'
    media_md = []
    with open(post_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines:
        if re.search(media_regex, line):
            media_md.append(re.search(media_regex, line).group(1))

    # check if media is external
    url_regex = r'(https?):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])'
    edited = False
    for media in media_md:
        if re.search(url_regex, media):
            edited = True
            # download media
            media_name = gen_uuid()
            while media_name in used_uuid:
                media_name = gen_uuid()
            used_uuid.append(media_name)

            media_url = media
            media_type = get_content_type(media_url)
            media_ext = media_type.split('/')[1]
            if media_ext == 'jpeg':
                media_ext = 'jpg'

            media_filename = f'{media_name}.{media_ext}'
            with open(os.path.join(media_path, media_filename), 'wb') as f:
                r = requests.get(media_url)
                f.write(r.content)

            # replace media url
            for i, line in enumerate(lines):
                if media in line:
                    lines[i] = line.replace(media, f'img/{media_filename}')
            logging.info(f'[media]\texternal {media} downloaded')

    if edited:
        with open(post_file, 'w', encoding='utf-8') as f:
            f.writelines(lines)
        return logging.info(f'[media]\tpost {post_id} media replaced')
    else:
        return None


if __name__ == '__main__':
    logging.info('[media]\tcreating temp directory')
    os.makedirs(temp_path, exist_ok=True)
    for pid in posts:
        get_media(pid)
        unzip_media(pid)
        get_external_media(pid)

    subprocess.run(['rm', '-rvf', temp_path])
    logging.info('[media]\tdone')
