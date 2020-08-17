# Script to create hanzi dashboard - page with all characters to click and get a definition

import jinja2
import os
import re
from pinyin_splitter import PinyinSplitter


# no Unicode extension
re_cjk = re.compile(r'([\u4E00-\u9FFF]+)')


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
    #print(len(data))
    html = hsk_tmpl.render(records=data)
    with open('index.html', mode='w', encoding='utf8') as file:
        file.write(html)


def generate_taiwan_list(env):
    taiwan_tmpl = env.get_template('taiwan.template.html')
    data = list(read_taiwan_list())
    #print(len(data))
    html = taiwan_tmpl.render(records=data)
    with open('taiwan.html', mode='w', encoding='utf8') as file:
        file.write(html)


def read_wenlin_list():
    with open(os.path.join('lists', 'wenlin_freq.txt'), encoding='utf8') as f:
        for line in f.readlines()[2:]:
            hanzi, traditional, pinyin, meaning = line.split('\t')
            pinyin_arr = ((syl, get_tone_number(syl)) for syl in pinyin.split())
            index = meaning.find('*)')
            # remove *) extra readings
            reduced_meaning = meaning[:index] if index != -1 else meaning
            colored_meaning = surround_pinyin(reduced_meaning)
            colored_meaning = surround_hanzi(colored_meaning)
            yield hanzi, traditional, pinyin_arr, colored_meaning


def surround_hanzi(meaning):
    def replace(m):
        return f'<span class="hanzi hanzi_sample">{m.group(1)}</span>'
    return re_cjk.sub(replace, meaning)


splitter = PinyinSplitter()


def surround_pinyin(meaning):
    def iter(part, tone):
        if tone is not None:
            return f'<span class="tone{tone}">{part}</span>'
        else:
            return part
    return ''.join(iter(part, tone) for part, tone in splitter.split(meaning))


def get_tone_number(pinyin):
    tones = [
        'āēīōūǖĀĒĪŌŪǕ',
        'áéíóúǘÁÉÍÓÚǗ',
        'ǎěǐǒǔǚǍĚǏǑǓǙ',
        'àèìòùǜÀÈÌÒÙǛ',
    ]
    for index, tone_row in enumerate(tones):
        for tone_letter in tone_row:
            if tone_letter in pinyin:
                return index + 1
    return 0


def generate_wenlin_list(env):
    wenlin_tmpl = env.get_template('wenlin.template.html')
    data = read_wenlin_list()
    html = wenlin_tmpl.render(records=data)
    with open('wenlin.html', mode='w', encoding='utf8') as file:
        file.write(html)


glob_env = jinja2.Environment(
    loader=jinja2.PackageLoader('create_dashboard', package_path='template'),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)

generate_hsk_list(glob_env)
generate_taiwan_list(glob_env)
generate_wenlin_list(glob_env)
