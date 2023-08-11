
variants = {
    '敎': '教',
    '靑': '青',
    '內': '内',
    '每': '毎',
    '淸': '清',
    '綠': '緑',
    '溫': '温',
    '黃': '黄',
    '德': '徳',
    '歷': '歴',
    '說': '説',
    '歲': '歳',
    '黑': '黒',
    '錄': '録',
    '步': '歩',
    '狀': '状',
    '稅': '税',
    '硏': '研',
    '增': '増',
    '鄕': '郷',
    '虛': '虚',
    '戶': '戸',
    '擊': '撃',
    '緣': '縁',
    '脫': '脱',
    '槪': '概',
    '寬': '寛',
    '郞': '郎',
    '曆': '暦',
    '鍊': '錬',
    '賴': '頼',
    '尙': '尚',
    '緖': '緒',
    '悅': '悦',
    '卽': '即',
    '徵': '徴',
    '橫': '横',
    '渴': '渇',
    '繫': '繋',
    '俱': '倶',
    '旣': '既',
    '畓': '畔',
    '淚': '涙',
    '屢': '屡',
    '屛': '屏',
    '涉': '渉',
    '閱': '閲',
    '銳': '鋭',
    '娛': '娯',
    '玆': '滋',
    '毁': '毀',
   # '珏': '',
    '鉀': '甲',
   # '塏': '',
    '揭': '掲',
   # '璟': '',
   # '炅': '',
   # '儆': '',
   # '琯': '',
    '鷗': '鴎',
  #  '琪': '',
  #  '璣': '',
  #  '琦': '',
    '燾': '濤', #???
  #  '乭': '',
 #   '鄧': '',
    '萊': '莱',
  #  '樑': '',
    '沔': '',
    '汶': '',
    '珉': '',
    '玟': '',
    '旼': '',
    '磻': '',
    '龐': '',
    '裵': '',
    '昞': '',
    '昺': '',
    '倂': '併',
    '潽': '',
    '毖': '',
    '揷': '挿',
    '晳': '皙',
    '奭': '',
    '瑄': '',
    '璇': '',
    '璿': '',
    '卨': '',
    '巢': '巣',
    '珣': '',
    '湜': '',
    '倻': '',
    '姸': '',
    '燁': '',
    '芮': '',
    '濊': '',
    '吳': '呉',
    '鈺': '',
    '邕': '',
    '瑢': '',
    '鏞': '',
    '頊': '',
    '昱': '',
    '煜': '',
    '瑗': '',
    '庾': '',
    '鈗': '',
    '誾': '',
    '佾': '',
    '蔣': '',
    '獐': '',
    '楨': '',
    '珽': '',
    '曺': '',
    '琮': '',
    '埈': '',
    '晙': '',
    '璨': '',
    '瓚': '',
    '埰': '',
    '澈': '',
    '喆': '',
    '沆': '',
    '爀': '',
    '炫': '',
    '峴': '',
    '邢': '',
    '瀅': '',
    '澔': '',
    '祜': '',
    '嬅': '',
    '壎': '',
    '薰': '',
    '姬': '姫',
}


def get_yarxi_names():
    with open('yarxi_names.txt', encoding='utf8') as yarxi_file:
        for line in yarxi_file.readlines()[1:]:
            line = line.rstrip('\n')
            kanji, name, meaning = line.split('\t')
            yield kanji, name, meaning


def get_wenlin_hanzi():
    with open('../lists/wenlin_freq.txt', encoding='utf8') as hanzi_file:
        for line in hanzi_file.readlines()[2:]:
            line = line.rstrip('\n')
            if len(line.split('\t')) != 4:
                print(line)
            simple_hanzi, trad_hanzi, *rest = line.split('\t')
            yield simple_hanzi, trad_hanzi


hanzi_order = []
hanzi_dict = {}
for simple_hanzi, trad_hanzi in get_wenlin_hanzi():
    #if grade > 1:
        hanzi_order.append(simple_hanzi)
        hanzi_dict[simple_hanzi] = trad_hanzi

meanings = {}
for kanji, name, meaning in get_yarxi_names():
    meanings[kanji] = (name, meaning)

prev_hanzi = {}
#with open('../rest-hanja.txt', encoding='utf8') as file:
#    for line in file.readlines():
#        hanja = line[0]
#        prev_hanja[hanja] = line.rstrip('\r\n')

temp_prev_hanzi = None
for hanzi in hanzi_order[:]:
    trad_hanzi = hanzi_dict[hanzi]
    if hanzi not in meanings and \
       hanzi not in variants:
        pass
        #print(f'{hanzi} not in yarxi nor variant lists')
   # continue
    if hanzi in meanings:
        name, meaning = meanings[hanzi]
      #  print(hanzi, meanings[1])
    elif hanzi in variants and len(variants[hanzi]):
        name, meaning = meanings[variants[hanzi]]
      #  print(prev_hanzi[hanzi])
    else:
        name, meaning = '', ''
        for trad in trad_hanzi:
            if trad in meanings:
                name += meanings[trad][0]
                meaning += meanings[trad][0]
        if len(name) == 0:
            print(f'{hanzi} not matched')
            continue
    temp_prev_hanzi = hanzi
    print(f'{hanzi}\t{name}\t{meaning}')
