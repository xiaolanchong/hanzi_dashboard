# Creates dictionary articles per character: text files with
#  (word/char in traditional, word/char in simplified, pinyin, definition) records
# Source: CC-CEDICT dictionary, https://www.mdbg.net/chinese/dictionary?page=cedict

import re
from collections import defaultdict
import os

pinyin_tone_marks = {
    'a': 'āáǎà', 'e': 'ēéěè', 'i': 'īíǐì',
    'o': 'ōóǒò', 'u': 'ūúǔù', 'ü': 'ǖǘǚǜ',
    'A': 'ĀÁǍÀ', 'E': 'ĒÉĚÈ', 'I': 'ĪÍǏÌ',
    'O': 'ŌÓǑÒ', 'U': 'ŪÚǓÙ', 'Ü': 'ǕǗǙǛ'
}

re_bracket = re.compile("\[.+?]")


def convert_pinyin_callback(m):
    tone = int(m.group(3)) % 5
    r = m.group(1).replace('v', 'ü').replace('V', 'Ü')
    # for multiple vowels, use first one if it is a/e/o, otherwise use second one
    pos = 0
    if len(r) > 1 and not r[0] in 'aeoAEO':
        pos=1
    if tone != 0:
        r = r[0:pos] + pinyin_tone_marks[r[pos]][tone-1]+r[pos+1:]
    return r+m.group(2)


def convert_pinyin(s):
    return re.sub(r'([aeiouüvÜ]{1,3})(n?g?r?)([012345])', convert_pinyin_callback, s, flags=re.IGNORECASE)


# Converts '三公经费[san1 gong1 jing1 fei4]' to '三公经费[sān gōng jīng fèi]'
def replace_pinyin_in_brackets(meaning):
    find_from = 0
    new_meaning = ''
    while True:
        m = re_bracket.search(meaning, find_from)
        if m is not None:
            new_meaning += meaning[find_from:m.start(0)]
            brackets = meaning[m.start(0): m.end(0)].replace('u:', 'ü').replace('U:', 'Ü')
            new_meaning += convert_pinyin(brackets)
            find_from = m.end(0)
        else:
            break
    return meaning if find_from == 0 else new_meaning + meaning[find_from:]


def read_cedict_data():
    re_line = re.compile(r'^(\S+) (\S+) \[(.+)\] /(.+?)/$')
    with open(os.path.join('dictionary', 'cedict_ts.u8'), encoding='utf8') as f:
        for line in f.readlines():
            if line[0] in '#%':
                continue
            m = re_line.match(line)
            if m is None:
                print(f'{line} not matched against regex')
                continue
            traditional, simplified, pronunciation, meaning = m.groups()
            pronunciation = pronunciation.replace('u:', 'ü').replace('U:', 'Ü')
            pronunciation = convert_pinyin(pronunciation)
            meaning = replace_pinyin_in_brackets(meaning)
            yield traditional, simplified, pronunciation, meaning


def is_cjk(symbol):
    return 0x4E00 <= ord(symbol)  # + extensions


def create_char_dict(data):
    hanzi_words = defaultdict(list)
    hanzi_words_per_char = set()
    for traditional, simplified, pronunciation, definition in data:
        assert len(traditional) == len(simplified)
        for ch in traditional + simplified:
            if not is_cjk(ch):
                continue
            full_tuple = (ch, traditional, simplified, pronunciation, definition)
            if full_tuple not in hanzi_words_per_char:
                hanzi_words_per_char.add(full_tuple)
                hanzi_words[ch].append((traditional, simplified, pronunciation, definition))

    # move character definition (len == 1 at the beginning)
    for k in hanzi_words.keys():
        records = hanzi_words[k]
        for index, record in enumerate(records):
            traditional, _, _, _ = record
            if len(traditional) == 1:
                copy_to = next((i for i in range(index) if len(records[i][0]) > 1), None)
                if copy_to is not None:
                    records[copy_to], records[index] = records[index], records[copy_to]
    return hanzi_words


# Creates article files: 000001/000001.txt, ..., 00900/00900.txt, ...
def write_hanzi(hanzi_words):
    root_dir = 'cedict'
    if not os.path.exists(root_dir):
        os.mkdir(root_dir)
    for hanzi, recs in list(hanzi_words.items())[:]:
       # print(f'{t}\t{s}\t{p}\t{d}')
        hanzi_num = ord(hanzi[0])
        dir_num = (hanzi_num // 100) * 100 if hanzi_num >= 100 else 1
        dir_name = f'{dir_num:06}'
        print(dir_name)
        if not os.path.exists(os.path.join(root_dir, dir_name)):
            os.mkdir(os.path.join(root_dir, dir_name))
        with open(os.path.join(root_dir, dir_name, f'{hanzi_num:06}.txt'), mode='w', encoding='utf8') as f:
            for rec in recs:
                text = '\t'.join(rec)
                f.write(text)
                f.write('\n')


def generate_cedict():
    data = list(read_cedict_data())
    hanzi_words = create_char_dict(data)
    write_hanzi(hanzi_words)


def generate_wenlin_list():
    pass


def test_pinyin_in_meaning():
    assert replace_pinyin_in_brackets(' city 瀋陽市|沈阳市[Shen3 yang2 shi4] li') == ' city 瀋陽市|沈阳市[Shěn yáng shì] li'
    assert replace_pinyin_in_brackets(' city 瀋陽市|沈阳市[Shen3 yang2 shi4] li [Shen3  shi4]') == \
        ' city 瀋陽市|沈阳市[Shěn yáng shì] li [Shěn  shì]'
    assert replace_pinyin_in_brackets(' city 瀋陽市|沈阳市[Shen3 lu:2 shi4] li [Shen3  shi4]') == \
        ' city 瀋陽市|沈阳市[Shěn lǘ shì] li [Shěn  shì]'


test_pinyin_in_meaning()
generate_cedict()
generate_wenlin_list()



