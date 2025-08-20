# Script to create hanzi dashboard - page with all characters to click and get a definition
import dataclasses
import typing

import jinja2
import csv
import os
import re
from pathlib import Path
from pinyin_splitter import PinyinSplitter


# no Unicode extension
re_cjk = re.compile(r'([\u4E00-\u9FFF]+)')
boards_dir = 'boards'


def read_hsk_list():
    with open(Path('..') / 'lists' / 'hsk_list.txt', encoding='utf8') as f:
        for line in f.readlines()[1:]:
            hanja, _, _, _, _, level, _, _ = line.split('\t')
            yield hanja, level


def read_char_list(file_name):  #
    with open(Path('..') / 'lists' / file_name, encoding='utf8') as f:
        return (ch for ch in f.read())


def generate_hsk_list(env):
    hsk_tmpl = env.get_template('hsk.template.html')
    data = list(read_hsk_list())
    #print(len(data))
    html = hsk_tmpl.render(records=data)
    with open(Path('..') / boards_dir / 'hsk.html', mode='w', encoding='utf8') as file:
        file.write(html)


def generate_list(env, char_file: str, template_list: str, output_file: str):
    taiwan_tmpl = env.get_template(template_list) #'taiwan.template.html')
    data = list(read_char_list(char_file))
    #print(len(data))
    html = taiwan_tmpl.render(records=data)
    with open(Path('..') / boards_dir / output_file, mode='w', encoding='utf8') as file:
        file.write(html)


def generate_taiwan_list(env):
    generate_list(env, 'taiwan_list.txt', 'taiwan.template.html', 'taiwan.html')


def generate_china_list(env):
    generate_list(env, '1_3500chars.txt', 'china_main.template.html', 'china_main.html')
    generate_list(env, '2_3000chars.txt', 'china_rest.template.html', 'china_rest.html')
    generate_list(env, '3_names.txt', 'china_name.template.html', 'china_name.html')


def generate_zhonghuayuwen_list(env):
    generate_list(env, 'zhonghuayuwen-ancient.txt', 'zhonghuayuwen-ancient.template.html',
                  'zhonghuayuwen-ancient.html')


def read_wenlin_list():
    with open(Path('..') / 'lists' / 'wenlin_freq.txt', encoding='utf8') as f:
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
    with open(Path('..') / boards_dir / 'wenlin.html', mode='w', encoding='utf8') as file:
        file.write(html)


def generate_yarxi_list(env):
    yarxi_tmpl = env.get_template('yarxi_mode.template.html')

    def read_list():
        with open(Path('..') / 'lists' / 'yarxi_mode.txt', encoding='utf8') as f:
            for line in f.readlines():
                hanzi, pinyin, meaning = line.split('\t')
                tone_num = get_tone_number(pinyin)
                yield hanzi, pinyin, tone_num, meaning
    html = yarxi_tmpl.render(records=list(read_list()))
    with open(Path('..') / boards_dir / 'yarxi_mode.html', mode='w', encoding='utf8') as file:
        file.write(html)


@dataclasses.dataclass
class MaoRecord:
    number: int
    pinyin: [typing.Tuple[str, int]]
    hanzi: str
    meaning: str
    assoc: [typing.Tuple[bool, str]]


def split_on_all_caps(text: str) -> list[str]:
    """
    Splits text into substrings separated by ALL-CAPS words.
    Keeps the ALL-CAPS words as separate list elements.
    """
    # Regex: match words that are fully uppercase (A-Z only)
    tokens = re.split(r'(\b[А-Я]+\b)', text)

    # Clean up spaces and empties
    return [t.strip() for t in tokens if t.strip()]


def is_meaning_in_association(parts, idx):
    #  This is not a meaning
    if idx == 0 and len(parts[idx]) == 1:
        return False
    # Prefix. T is not a meaning
    if len(parts[idx]) == 1 and idx > 0:
        assert parts
        kkk = parts[idx-1].rstrip()
        if kkk and kkk[-1] in ('.', '!', '?') and len(kkk):
            return False
        return True
    return parts[idx][-1].isupper()


def generate_wenlin_mao_list(env):
    mao_tmpl = env.get_template('wenlin_mao.template.html')
    pages = [   (1,  499),  (500,  999),
             (1000, 1499), (1500, 1999),
             (2000, 2499), (2500, 2999),
             (3000, 3499), (3500, None)]

    NEUTRAL_TONE = 5

    def read_lists():
        with open(Path('..') / 'lists' / 'wenlin + mao system.csv', 'r', newline='', encoding='utf8') as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            for idx, (start, end) in enumerate(pages):
                end = end + 1 if end else len(rows)
                records = []
                for row in rows[start:end]:
                    number, pinyin_joined, hanzi, _, meaning, _, _, _, _, _, _, association, *_ = row
                    number = int(number)
                    if len(pinyin_joined) == 0:
                        print(row)
                    pinyin = [(pinyin, int(pinyin[-1]) if len(pinyin) and pinyin[-1].isdigit() else NEUTRAL_TONE)
                              for pinyin in pinyin_joined.split(' ')]
                    meaning = meaning.replace('\n', ' ')
                    association = association.replace('\n', ' ')
                    parts = split_on_all_caps(association)
                    association = [(is_meaning_in_association(parts, str_idx), part)
                                   for str_idx, part in enumerate(parts)]
                    #print(number, pinyin, hanzi, meaning, association)
                    records.append(MaoRecord(number=number, pinyin=pinyin, hanzi=hanzi,
                                             meaning=meaning, assoc=association))
                   # if int(number) > 10:
                    #    return
                yield records

    pages = [l for l in read_lists()]
    for idx, record_list in enumerate(pages):
        #print(len(record_list))
        html = mao_tmpl.render(entities=record_list, current_page=idx, page_total=len(pages))
        with open(Path('..') / boards_dir / f'wenlin_mao-{idx+1}.html', mode='w', encoding='utf8') as file:
            file.write(html)
            #return


glob_env = jinja2.Environment(
    loader=jinja2.PackageLoader('create_dashboards', package_path=str(Path('..') / 'template')),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)

generate_hsk_list(glob_env)
generate_taiwan_list(glob_env)
generate_china_list(glob_env)
generate_wenlin_list(glob_env)
generate_zhonghuayuwen_list(glob_env)
generate_yarxi_list(glob_env)
generate_wenlin_mao_list(glob_env)
