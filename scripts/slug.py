import os
import logging


logging.basicConfig(level=logging.INFO)

pwd = os.getcwd()
posts_path = os.path.join(pwd, 'posts')


def add_slug(name):
    slug_line = 'slug: {}\n'.format(name.lower().replace(' ', '-'))
    with open(os.path.join(posts_path, name, 'index.md'), 'r', encoding='utf-8') as f:
        lines = f.readlines()
    lines.insert(2, slug_line)  # after title
    with open(os.path.join(posts_path, name, 'index.md'), 'w', encoding='utf-8') as f:
        f.writelines(lines)
    return logging.info(f'{name} slug added')


if __name__ == '__main__':
    for i in os.listdir(posts_path):
        add_slug(i)
