# Script to create hanzi dashboard - page with all characters to click and get a definition

import jinja2
import os


def read_hsk_list():
    with open(os.path.join('lists', 'hsk_list.txt'), encoding='utf8') as f:
        for line in f.readlines()[1:]:
            hanja, _, _, _, _, level, _, _ = line.split('\t')
            yield hanja, level


def read_taiwan_list():
    with open(os.path.join('lists', 'taiwan_list.txt'), encoding='utf8') as f:
        return (ch for ch in f.read())


def generate_hsk_list(env):
    hsk_tmpl = env.get_template('hsk.template.html')
    data = list(read_hsk_list())
    print(len(data))
    html = hsk_tmpl.render(records=data)
    with open('index.html', mode='w', encoding='utf8') as file:
        file.write(html)


def generate_taiwan_list(env):
    taiwan_tmpl = env.get_template('taiwan.template.html')
    data = list(read_taiwan_list())
    print(len(data))
    html = taiwan_tmpl.render(records=data)
    with open('taiwan.html', mode='w', encoding='utf8') as file:
        file.write(html)


glob_env = jinja2.Environment(
    loader=jinja2.PackageLoader('create_dashboard', package_path='template'),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)

if True:
    generate_hsk_list(glob_env)
if True:
    generate_taiwan_list(glob_env)




