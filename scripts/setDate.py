import os
import logging
import subprocess
from datetime import datetime, timezone, timedelta

# timezone is UTC+8


logging.basicConfig(level=logging.INFO)

pwd = os.getcwd()
posts_path = os.path.join(pwd, 'posts')
# about_page_path = 'content/pages/about/index.md'
about_page_path = os.path.join(pwd, 'content', 'pages', 'about', 'index.md')
git_date_fmt = '%a %b %d %H:%M:%S %Y %z'
preferred_date_fmt = '%Y-%m-%d %H:%M:%S'
metadata_date_fmt = '%Y-%m-%d %H:%M:%S%z'


def set_about_info():
    """
    最后文章 LAST_POST_DATE
    最后更新 COMMIT_DATE
    构建日期 BUILD_DATE
    """
    # git log -1 --format=%cd posts
    # Sun Jun 4 02:42:49 2023 +0800
    git_command = subprocess.check_output(
        ['git', 'log', '-1', '--format=%cd', posts_path])
    git_last_post_date = git_command.decode('utf-8')[:-1]  # ends with \n
    last_post_date = datetime.strptime(
        git_last_post_date, git_date_fmt)
    last_post_date = last_post_date.astimezone(timezone(timedelta(hours=8)))
    last_post_date_str = last_post_date.strftime(preferred_date_fmt)

    git_command = subprocess.check_output(
        ['git', 'log', '-1', '--format=%cd']).decode('utf-8')
    git_commit_date = git_command[:-1]
    commit_date = datetime.strptime(
        git_commit_date, git_date_fmt)
    commit_date = commit_date.astimezone(timezone(timedelta(hours=8)))
    commit_date_str = commit_date.strftime(preferred_date_fmt)

    # build_date = datetime.now()
    # convert to UTC+8
    build_date = datetime.now(timezone(timedelta(hours=8)))
    build_date_str = build_date.strftime(preferred_date_fmt)

    with open(about_page_path, 'r', encoding='utf-8') as f:
        about_page = f.read()
    about_page = about_page.replace('LAST_POST_DATE', last_post_date_str)
    about_page = about_page.replace('COMMIT_DATE', commit_date_str)
    about_page = about_page.replace('BUILD_DATE', build_date_str)
    with open(about_page_path, 'w', encoding='utf-8') as f:
        f.write(about_page)

    return logging.info('[date]\tset about info')


def set_post_modified_date(post_path):
    post_date_str = post_path.split('-')[0]
    post_date = datetime.strptime(post_date_str, '%y%m%d').astimezone(timezone(timedelta(hours=8)))

    post_text_path = os.path.join(posts_path, post_path, 'index.md')
    git_command = subprocess.check_output(
        ['git', 'log', '-1', '--format=%cd', post_text_path])
    git_commit_date = git_command.decode('utf-8')[:-1]
    commit_date = datetime.strptime(
        git_commit_date, git_date_fmt).astimezone(timezone(timedelta(hours=8)))

    if post_date.day != commit_date.day or post_date.month != commit_date.month or post_date.year != commit_date.year:
        logging.info(f'[date]\t{post_path} modified date changed')
        # 2023-06-03T15:00:00+0800
        post_date_str = commit_date.strftime(metadata_date_fmt)

        with open(post_text_path, 'r', encoding='utf-8') as f:
            post_text = f.read()
        # insert `lastmod` next to the `date` line
        date_info_line = ''
        for line in post_text.split('\n'):
            if line.startswith('date:'):
                date_info_line = line
                break
        if not date_info_line:
            raise RuntimeError(f'[date]\t{post_path} date info not found')
        post_text = post_text.replace(date_info_line, date_info_line + f'\nlastmod: "{post_date_str}"')
        with open(post_text_path, 'w', encoding='utf-8') as f:
            f.write(post_text)
    else:
        return None


def set_posts_modified_date():
    posts_list = os.listdir(posts_path)
    for post_path in posts_list:
        set_post_modified_date(post_path)
    return logging.info('[date]\tset posts modified date')


if __name__ == '__main__':
    set_about_info()
    set_posts_modified_date()
