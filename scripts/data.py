import os
import requests


# posts = {
#     '220616': {
#         'name': 'we-in-game'
#     },
# }

pwd = os.getcwd()
posts_path = os.path.join(pwd, 'posts')

all_posts = {}
for i in os.listdir(posts_path):
    # 220531-hello-world
    date = i.split('-')[0]
    title = i[len(date) + 1:]
    if date in all_posts:
        title = min(title, all_posts[date]['name'], key=len)
    all_posts[date] = {
        'name': title
    }

tags_api = 'https://api.github.com/repos/KumaTea/blog/git/refs/tags'
r = requests.get(tags_api)
tags_json = r.json()
tags = [i['ref'].split('/')[-1] for i in tags_json]

posts = {}
for i in tags:
    if i in all_posts.keys():
        posts[i] = all_posts[i]
