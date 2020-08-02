import re
import unittest

# in	b 	p 	m 	f 	d 	t 	n 	l 	g 	k 	h 	z 	c 	s 	zh 	ch 	sh 	r 	j 	q 	x	Ø
all_syllables_table = \
    """
a 	ba 	pa 	ma 	fa 	da 	ta 	na 	la 	ga 	ka 	ha 	za 	ca 	sa 	zha 	cha 	sha 	  	  	  	  	a
o 	bo 	po 	mo 	fo 	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	o
e 	  	  	me 	  	de 	te 	ne 	le 	ge 	ke 	he 	ze 	ce 	se 	zhe 	che 	she 	re 	  	  	  	e
ai 	bai 	pai 	mai 	  	dai 	tai 	nai 	lai 	gai 	kai 	hai 	zai 	cai 	sai 	zhai 	chai 	shai 	  	  	  	  	ai
ei 	bei 	pei 	mei 	fei 	dei 	tei 	nei 	lei 	gei 	kei 	hei 	zei 	  	  	zhei 	  	shei 	  	  	  	  	ei
ao 	bao 	pao 	mao 	  	dao 	tao 	nao 	lao 	gao 	kao 	hao 	zao 	cao 	sao 	zhao 	chao 	shao 	rao 	  	  	  	ao
ou 	  	pou 	mou 	fou 	dou 	tou 	nou 	lou 	gou 	kou 	hou 	zou 	cou 	sou 	zhou 	chou 	shou 	rou 	  	  	  	ou
an 	ban 	pan 	man 	fan 	dan 	tan 	nan 	lan 	gan 	kan 	han 	zan 	can 	san 	zhan 	chan 	shan 	ran 	  	  	  	an
ang 	bang 	pang 	mang 	fang 	dang 	tang 	nang 	lang 	gang 	kang 	hang 	zang 	cang 	sang 	zhang 	chang 	shang 	rang 	  	  	  	ang
en 	ben 	pen 	men 	fen 	den 	  	nen 	  	gen 	ken 	hen 	zen 	cen 	sen 	zhen 	chen 	shen 	ren 	  	  	  	en
eng 	beng 	peng 	meng 	feng 	deng 	teng 	neng 	leng 	geng 	keng 	heng 	zeng 	ceng 	seng 	zheng 	cheng 	sheng 	reng 	  	  	  	eng
ong 	  	  	  	  	dong 	tong 	nong 	long 	gong 	kong 	hong 	zong 	cong 	song 	zhong 	chong 	  	rong 	  	  	  	 
u 	bu 	pu 	mu 	fu 	du 	tu 	nu 	lu 	gu 	ku 	hu 	zu 	cu 	su 	zhu 	chu 	shu 	ru 	  	  	  	wu
ua 	  	  	  	  	  	  	  	  	gua 	kua 	hua 	  	  	  	zhua 	chua 	shua 	rua 	  	  	  	wa
uo 	  	  	  	  	duo 	tuo 	nuo 	luo 	guo 	kuo 	huo 	zuo 	cuo 	suo 	zhuo 	chuo 	shuo 	ruo 	  	  	  	wo
uai 	  	  	  	  	  	  	  	  	guai 	kuai 	huai 	  	  	  	zhuai 	chuai 	shuai 	  	  	  	  	wai
ui 	  	  	  	  	dui 	tui 	  	  	gui 	kui 	hui 	zui 	cui 	sui 	zhui 	chui 	shui 	rui 	  	  	  	wei
uan 	  	  	  	  	duan 	tuan 	nuan 	luan 	guan 	kuan 	huan 	zuan 	cuan 	suan 	zhuan 	chuan 	shuan 	ruan 	  	  	  	wan
uang 	  	  	  	  	  	  	  	  	guang 	kuang 	huang 	  	  	  	zhuang 	chuang 	shuang 	  	  	  	  	wang
un 	  	  	  	  	dun 	tun 	nun 	lun 	gun 	kun 	hun 	zun 	cun 	sun 	zhun 	chun 	shun 	run 	  	  	  	wen
ueng 	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	weng
i 	bi 	pi 	mi 	  	di 	ti 	ni 	li 	  	  	  	zi	ci	si	zhi	chi	shi	ri	ji 	qi 	xi 	yi
ia 	  	  	  	  	dia 	  	  	lia 	  	  	  	  	  	  	  	  	  	  	jia 	qia 	xia 	ya
ie 	bie 	pie 	mie 	  	die 	tie 	nie 	lie 	  	  	  	  	  	  	  	  	  	  	jie 	qie 	xie 	ye
iao 	biao 	piao 	miao 	  	diao 	tiao 	niao 	liao 	  	  	  	  	  	  	  	  	  	  	jiao 	qiao 	xiao 	yao
iu 	  	  	miu 	  	diu 	  	niu 	liu 	  	  	  	  	  	  	  	  	  	  	jiu 	qiu 	xiu 	you
ian 	bian 	pian 	mian 	  	dian 	tian 	nian 	lian 	  	  	  	  	  	  	  	  	  	  	jian 	qian 	xian 	yan
iang 	  	  	  	  	  	  	niang 	liang 	  	  	  	  	  	  	  	  	  	  	jiang 	qiang 	xiang 	yang
in 	bin 	pin 	min 	  	  	  	nin 	lin 	  	  	  	  	  	  	  	  	  	  	jin 	qin 	xin 	yin
ing 	bing 	ping 	ming 	  	ding 	ting 	ning 	ling 	  	  	  	  	  	  	  	  	  	  	jing 	qing 	xing 	ying
iong 	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	jiong 	qiong 	xiong 	yong
ü 	  	  	  	  	  	  	nü 	lü 	  	  	  	  	  	  	  	  	  	  	ju	qu	xu	yu
üe 	  	  	  	  	  	  	nüe 	lüe 	  	  	  	  	  	  	  	  	  	  	jue	que	xue	yue
üan 	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	juan	quan	xuan	yuan
ün 	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	  	jun	qun	xun	yun
"""


class PinyinSplitter:
    NEUTRAL_TONE = 5

    def __init__(self):
        self._all_syllables = dict()
        for row in all_syllables_table.split('\n'):
            for syl in row.split()[1:]:
                syl = syl.strip()
                for syl_toned, tone in PinyinSplitter.get_syllable_tones(syl):
                    self._all_syllables[syl_toned] = tone
        self.max_syllable_len = max(len(w) for w in self._all_syllables.keys())
        # print(self._all_syllables)

    @staticmethod
    def replace_with_tone(syllable: str, where: int):
        tones = {
            'a': 'āáǎàa',
            'e': 'ēéěèe',
            'i': 'īíǐìi',
            'o': 'ōóǒòo',
            'u': 'ūúǔùu',
            'ü': 'ǖǘǚǜü'
        }
        for index, ch in enumerate(tones[syllable[where]]):
            yield syllable[:where] + ch + syllable[where + 1:], index + 1

    # Rules to mark: http://pinyin.info/rules/where.html
    @staticmethod
    def get_syllable_tones(syllable: str):
        index = syllable.find('a')
        if index != -1:
            return PinyinSplitter.replace_with_tone(syllable, index)

        index = syllable.find('e')
        if index != -1:
            return PinyinSplitter.replace_with_tone(syllable, index)

        index = syllable.find('ou')
        if index != -1:
            return PinyinSplitter.replace_with_tone(syllable, index)

        m = re.search('([aeiouü])', syllable[::-1], re.IGNORECASE)
        assert m is not None
        where = len(syllable) - m.start(1) - 1
        return PinyinSplitter.replace_with_tone(syllable, where)

    def split(self, pinyin_phrase):
        def surrounded_by_brackets(phrase, st, e):
            return st >= 1 and e < len(phrase) and phrase[st - 1] == '[' and phrase[e] == ']'

        start = 0
        non_pinyin_tail = ''  # to merge non-pinyin chars into one group
        was_pinyin_before = False
        while start < len(pinyin_phrase):
            end = min(start + self.max_syllable_len, len(pinyin_phrase))
            for i in range(end, start, -1):
                tt = pinyin_phrase[start: i].lower()
                tone_number = self._all_syllables.get(tt)
                if tone_number is not None and \
                        (tone_number != PinyinSplitter.NEUTRAL_TONE or was_pinyin_before or
                         surrounded_by_brackets(pinyin_phrase, start, i)):
                    if len(non_pinyin_tail):
                        yield non_pinyin_tail, None
                        non_pinyin_tail = ''
                    yield pinyin_phrase[start: i], tone_number
                    start = i
                    was_pinyin_before = True
                    break
            else:
                non_pinyin_tail += pinyin_phrase[start: start + 1]
                start += 1
                was_pinyin_before = False
        if len(non_pinyin_tail):
            yield non_pinyin_tail, None


class PinyinSplitterTest(unittest.TestCase):
    def setUp(self):
        unittest.TestCase.maxDiff = None
        self.splitter = PinyinSplitter()

    def split(self, phrase):
        return list(self.splitter.split(phrase))

    def testOneSyllable(self):
        self.assertEqual(self.split('fū'), [('fū', 1)])
        self.assertEqual(self.split('上声 [shang]'), [('上声 [', None), ('shang', 5), (']', None)])
        self.assertEqual(self.split('[shang]'), [('[', None), ('shang', 5), (']', None)])
        self.assertEqual(self.split('shang]'), [('shang]', None)])
        self.assertEqual(self.split('[shang'), [('[shang', None)])
        self.assertEqual(self.split('shang'), [('shang', None)])
        self.assertEqual(self.split('(shang)'), [('(shang)', None)])

    def testMultipleSyllable(self):
        self.assertEqual(self.split('jiǎzhuāng'), [('jiǎ', 3), ('zhuāng', 1)])
        self.assertEqual(self.split('Yuànzi lǐ tíngzhe yí liàng chē.'),
                         [('Yuàn', 4), ('zi', 5), (' ', None), ('lǐ', 3), (' ', None), ('tíng', 2), ('zhe', 5),
                          (' ', None), ('yí', 2),
                          (' ', None), ('liàng', 4), (' ', None), ('chē', 1), ('.', None)])
        self.assertEqual(self.split('[liǎo]'), [('[', None), ('liǎo', 3), (']', None)])

    def testOddSymbls(self):
        self.assertEqual(self.split('fūz'), [('fū', 1), ('z', None)])

    def testPhrase(self):
        self.assertEqual(self.split('This word has lǐ tíngzhe zhe.'),
                         [('This word has ', None), ('lǐ', 3), (' ', None), ('tíng', 2), ('zhe', 5), (' zhe.', None)])


if __name__ == '__main__':
    unittest.main()
