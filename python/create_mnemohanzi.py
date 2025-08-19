import re
import dataclasses
import enum
import itertools
import typing as t
import jinja2
from pathlib import Path

re_key = '\bКЛЮЧ\b'
boards_dir = 'boards'

re_line = re.compile(r"""
^
(?:
(?P<key>\d+)|  # key
(?P<prime>I)|  # group 1
(?P<second>II)  # group 2
)?
(?:
(?P<hanzi>[\u4E00-\u9FFF]) |
(?P<rare>[\u3400-\u4DBF]) |
(?P<radical>[\u2E80-\u2FDF]) |
(?P<ext>[\U00020000-\U0002A6DF]) |
(?P<beibei>贝贝)
)
\s
(?:
(?P<pinyin>[a-züāēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜń]+)
(?:,
  (?P<pinyin2>[a-züāēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜń]+)
)?
(?:,
  (?P<pinyin3>[a-züāēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜń]+)
)?
\s
)?
(?P<text>.+?)
$
""", re.VERBOSE)


class Type(enum.Enum):
    KEY = 'K'
    PRIME = 'I'
    SECOND = 'II'
    UNDEFINED = ''


type_to_str = {
    Type.KEY: 'K',
    Type.PRIME: 'I',
    Type.SECOND: 'II',
    Type.UNDEFINED: '',
}


@dataclasses.dataclass
class Entity:
    hanzi: str  # or radical
    type: Type
    key_id: int = None
    meaning: str = None
    pinyin: list[str] = None
    assoc: t.Optional[str] = None
    etym: t.Optional[str] = None


@dataclasses.dataclass
class JinjaEntity:
    hanzi: str
    key_id: t.Optional[int]
    meaning: str
    pinyin: list[str]
    tone_numbers: list[int]
    assoc: t.Optional[str]
    etym: t.Optional[str]
    is_prime: bool = False,
    is_second: bool = False


def get_tone_number(pinyin):
    tones = [
        'āēīōūǖĀĒĪŌŪǕ',
        'áéíóúǘÁÉÍÓÚǗń',
        'ǎěǐǒǔǚǍĚǏǑǓǙ',
        'àèìòùǜÀÈÌÒÙǛ',
    ]
    for index, tone_row in enumerate(tones):
        for tone_letter in tone_row:
            if tone_letter in pinyin:
                return index + 1
    return 0


def to_jinja_entity(entity: Entity):
    return JinjaEntity(hanzi=entity.hanzi,
                       key_id=entity.key_id if entity.type == Type.KEY else None,
                       meaning=entity.meaning,
                       assoc=entity.assoc,
                       etym=entity.etym,
                       pinyin=entity.pinyin,
                       tone_numbers=[get_tone_number(pinyin) for pinyin in entity.pinyin],
                       is_prime=entity.type == Type.PRIME,
                       is_second=entity.type == Type.SECOND)


def load_dictionary():
    entities = []
    with open('mnemo_hanzi_dict.txt', encoding='utf8') as f:
        for lineno, line in enumerate(f.readlines()):
            line = line.rstrip('\n')
            m = re_line.match(line)
            if m is None:
                print('Not in pattern:', line)
               # break
            groups = m.groupdict()
            key, prime, second = groups['key'], groups['prime'], groups['second']
            hanzi = groups['hanzi'] or groups['rare']
            ext_rad = groups['radical'] or groups['ext'] or groups['beibei']
            text = groups['text']

            meaning, etym, assoc = None, None, None
            parts = text.split('АСЦ')
            if 'ЭТМЛ' in text and 'ЭТМЛ.:' not in text:
                print(text)
                assert False
            if len(parts) == 1:
                parts = parts[0].split('ЭТМЛ.:')
                if len(parts) == 2:
                    meaning, etym = parts[0], parts[1]
                else:
                    meaning = parts[0]
            elif len(parts) == 2:
                if 'ЭТМЛ.' in parts[0]:
                    meaning, etym = parts[0].split('ЭТМЛ.:')
                    assoc = parts[1]
                elif 'ЭТМЛ.' in parts[1]:
                    meaning = parts[0]
                    assoc, etym = parts[1].split('ЭТМЛ.:')
                else:
                    meaning, assoc = parts
            else:
                assert 'ЭТМЛ' not in text
                meaning, assoc = parts[0], '; '.join(parts[1:])
            assert len(meaning)
            typ = Type.UNDEFINED
            if key is not None:
                typ = Type.KEY
            elif groups['prime']:
                typ = Type.PRIME
            elif groups['second']:
                typ = Type.SECOND
            pinyin = []
            for name in ['pinyin', 'pinyin2', 'pinyin3']:
                if groups[name] is not None:
                    pinyin.append(groups[name])
            #if len(pinyin) > 1:
            #    print(hanzi)
            ent = Entity(hanzi=hanzi or ext_rad, type=typ,
                         key_id=int(key) if key else None,
                         meaning=meaning.strip() if meaning else None,
                         assoc=assoc.strip() if assoc else None,
                         etym=etym.strip() if etym else None,
                         pinyin=pinyin
                         )
            entities.append(ent)
    return entities


def dump_dictionary(entities: list[Entity]):
    for ent in entities:
        print(f'{type_to_str[ent.type] if ent.type != Type.KEY else ent.key_id}'
              f'{ent.hanzi} {(",".join(ent.pinyin) + " ") if pinyin else ""}{ent.meaning}'
              f'{" ЭТМЛ.: " + ent.etym if ent.etym else ""}'
              f'{" АСЦ " + ent.assoc if ent.assoc else ""}'
              )


def dump_hanzi(entities: list[Entity]):
    for ent in entities:
        print(ent.hanzi)


def generate_html(entities: list[Entity]):
    def find_by_key(key_id):
        for index, entity in enumerate(entities):
            if entity.key_id and entity.key_id == key_id:
                return index
        else:
            return None

    def pairwise(iterable):  # TODO: replace in 3.10 by itertools
        # pairwise('ABCDEFG') → AB BC CD DE EF FG

        iterator = iter(iterable)
        a = next(iterator, None)

        for b in iterator:
            yield a, b
            a = b

    env = jinja2.Environment(
        loader=jinja2.PackageLoader('create_mnemohanzi', package_path=str(Path('..') / 'template')),
        autoescape=jinja2.select_autoescape(['html', 'xml'])
    )
    file_index = 0
    mnemohanzi_tmpl = env.get_template('mnemohanzi.template.html')

    # 0, 900, 1800, 2700, 3600, 4400
    current_entity_number = 0
    break_keys = [0, find_by_key(20), find_by_key(36), find_by_key(127), find_by_key(202), len(entities)]
    for start, end in pairwise(break_keys):
        html = mnemohanzi_tmpl.render(entities=[to_jinja_entity(entity) for entity in entities[start:end]],
                                      page_total=len(break_keys)-1, current_page=file_index,
                                      start_entity_number=current_entity_number)
        file_index += 1
        current_entity_number += end - start
        with open(Path('..') / boards_dir / f'mnemohanzi-{file_index}.html', mode='w', encoding='utf8') as file:
            file.write(html)
        #break


def run():
    entities = load_dictionary()
    #dump_dictionary(entities)
    #dump_hanzi(entities)
    generate_html(entities)


run()
