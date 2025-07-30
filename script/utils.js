/* global $ */

'use strict'

const CHAR_NOT_FOUND = 'Иероглиф не найден на сайте'

function getHaziBoardId(hanzi) {
  return 'hanzi' + hanzi.charCodeAt(0)
}

function removeHanziBoard(hanzi) {
  let hanjaBoardElem = $(`#${getHaziBoardId(hanzi)}`)
  if (hanjaBoardElem.length) {
    hanjaBoardElem.remove()
    return
  }
}

function onHanziClick (self) {
  const insertElem = (whereClicked, whatInsert) => {
	$(self).after(whatInsert)
  }
  addDictionaryWidget(self, insertElem)
}

function onHanziMemClick (self) {
  const insertElem = (whereClicked, whatInsert) => {
	  $(self).parent().next().append(whatInsert)
  }
  addDictionaryWidget(self, insertElem)
}

function addDictionaryWidget (whatClicked, howToAdd) {
  const hanzi = $(whatClicked).text()
  const hanziBoardId = getHaziBoardId(hanzi)
  let hanjaBoardElem = $(`#${hanziBoardId}`)
  if (hanjaBoardElem.length) {
    hanjaBoardElem.remove()
    return
  }
  hanjaBoardElem = $(`<div id="${hanziBoardId}">Загрузка...</div>`)
  howToAdd(whatClicked, hanjaBoardElem)
  if ($('#cedict').prop('checked')) {
    getCedictArticle(hanzi, hanjaBoardElem)
  } else if ($('#bkrs').prop('checked')) {
    getBkrsArticle(hanzi, hanjaBoardElem)
  } else if ($('#wenlin').prop('checked')) {
    getWenlinCharArticle(hanzi, hanjaBoardElem)
  } else {
    getWenlinCharArticle(hanzi, hanjaBoardElem)
  }
}

function getCedictArticle (hanzi, parentElem) {
  const hanziIndex = hanzi.charCodeAt(0)
  const hanjaUrl = 'cedict/' + articleNumberToLink(hanziIndex)
  $.get({
    url: hanjaUrl,
    dataType: 'text'
  }
  ).done((data) => {
    parentElem.text('')
    const table = createHanziBoard(hanzi, data)
    parentElem.append(table)
  }
  ).fail(() => {
    parentElem.text(CHAR_NOT_FOUND)
  }
  )
}

function getBkrsArticle (hanzi, parentElem) {
  const hanziIndex = hanzi.charCodeAt(0)
  const hanjaUrl = 'bkrs/' + articleNumberToLink(hanziIndex, 6, 'xdfx')
  $.get({
    url: hanjaUrl,
    dataType: 'text'
  }
  ).done((data) => {
    parentElem.text('')
    const board = createBkrsBoard(data)
    parentElem.append(board)
  }
  ).fail(() => {
    parentElem.text(CHAR_NOT_FOUND)
  }
  )
}

function createBkrsBoard (xmlData) {
  const replaceFunc = (match, p1, p2, offset, string) => {
    const xdfxToHtml = {
      i: ['i', ''],
      b: ['strong', ''],
      c: ['span', ''],
      k: ['div', ''],
      ex: ['div', 'example']
    }
    const [tag, cssClass] = xdfxToHtml[p2] || ['span', '']
    return p1 ? `</${tag}>` : `<${tag} class="${cssClass}">`
  }
  const htmlData = xmlData.replace(/<(\/)?([a-z]+)>/ig, replaceFunc)

  const board = $('<div />')
  $(board).html(htmlData)
  return board
}

function getWenlinCharArticle (hanzi, parentElem) {
  const hanziIndex = hanzi.charCodeAt(0)
  const fileName = articleNumberToLink(hanziIndex, 6, 'txt')
  const hanziUrl = 'wenlin/wenlin_char/' + fileName
  $.get({
    url: hanziUrl,
    dataType: 'text'
  }
  ).done((data) => {
    parentElem.text('')
    const board = createWenlinCharBoard(hanzi, data)
    parentElem.append(board)
  }
  ).fail(() => {
    parentElem.text(CHAR_NOT_FOUND)
  }
  )
}

function getWenlinWordArticle (hanzi, parentElem) {
  const hanziIndex = hanzi.charCodeAt(0)
  const fileName = articleNumberToLink(hanziIndex, 6, 'txt')
  const hanziUrl = 'wenlin/wenlin_word/' + fileName
  $.get({
    url: hanziUrl,
    dataType: 'text'
  }
  ).done((data) => {
    parentElem.text('')
     const board = createWenlinWordBoard(hanzi, data)
    parentElem.append(board)
  }
  ).fail(() => {
    parentElem.text(CHAR_NOT_FOUND)
  }
  )
}

function createWenlinWordBoard (hanzi, textData) {
  const records = textData.split('\n')
  const table = $('<table class="hanzi-board">' +
                    `<caption>Слова ${hanzi}</caption>` +
                    '<tr><th>Упрощенные</th><th>Традиционные</th><th>Пиньинь</th><th>Значение</th></tr>' +
                  '</table>')
  const reLine = /(.+?)(?:\[(.+?)\])?\s+(.+?)\s(.+)/ //  雇佣兵[-傭-] gùyōngbīng {E} n. mercenary
  for (const record of records) {
    if (record.length === 0) { continue }
    let [, simplified, traditional, pinyin, meaning] = record.match(reLine)
    if (traditional === undefined)
      traditional = ''
    meaning = highlightPinyin(meaning)  // A meaning can contain examples
    const pinyinColored = highlightPinyin(pinyin)
    const row = $(`<tr><td class="hanzi-simp">${simplified}</td><td class="hanzi-trad">${traditional}` +
                  `<td class="">${pinyinColored}</td><td>${meaning}</td></tr>`)
    table.append(row)
  }
  return table
}

function createWenlinCharBoard (hanzi, textData) {
  const records = textData.split('\n')
  const article = $('<article />')
  for (let index = 0; index < records.length; ++index) {
    let line = records[index]
    if (index === 0) { // 1828 丛(F叢) [cóng] crowd; 丛书 cóngshū series of books; 丛林 jungle
      const reHeader = /^(\w+)\s(.+)/i
      line = line.replace(reHeader, '<small>$1</small> $2')
    }
    line = highlightPinyin(line)
    const row = $(`<p>${line}</p>`)
    article.append(row)
  }

  const wordBoard = $('<div />')
  const buttonShowWord = $('<button>Показать слова</button>')
  buttonShowWord.click(()=>{
    buttonShowWord.prop('disabled', true);
    getWenlinWordArticle(hanzi, wordBoard)
  })
  const buttonHide = $('<button>Закрыть</button>').click(()=>{
    removeHanziBoard(hanzi)
  })
  const container = $('<div />')
  
  container.append(wordBoard).append(buttonShowWord).append(buttonHide)
  article.append(container)
  return article
}

function createHanziBoard (hanzi, textData) {
  const records = textData.split('\n')
  const table = $('<table class="hanzi-board">' +
                    `<caption>Слова ${hanzi}</caption>` +
                    '<tr><th>Традиционные</th><th>Упрощенные</th><th>Пиньинь</th><th>Значение</th></tr>' +
                  '</table>')
  for (const record of records) {
    if (record.length === 0) { continue }
    let [traditional, simplified, pinyin, meaning] = record.split('\t')
    const pinyinColored = createColoredPinyin(pinyin)
    meaning = meaning.replaceAll('/', '; ')
    const row = $(`<tr><td class="hanzi-trad">${traditional}</td><td class="hanzi-simp">${simplified}` +
                  `<td class="">${pinyinColored}</td><td>${meaning}</td></tr>`)
    table.append(row)
  }
  return table
}

function _getPinyinRegex () {
  return new RegExp('([a-z]*[üāēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜ][a-zāēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜ]*)', 'ig')
}

function findPinyin (line) {
  const re = _getPinyinRegex()
  return line.match(re)
}

const isNode = () =>
  typeof process === 'object' &&
  typeof process.versions === 'object' &&
  typeof process.versions.node !== 'undefined';
 
if (isNode()) {
  const pinyinSeparate = require('./pinyin-separate.min.js')
}

function splitPinyin (word) {
	//console.log(pinyinSeparate)
  return pinyinSeparate(word)
}
	
function splitPinyinOld (word) {
  const finals = 'aeiouüāēīōūǖáéíóúǘǎěǐǒǔǚàèìòùǜ'
  const initials = 'b|p|m|f|d|t|n|l|g|k|h|z|c|s|zh|ch|sh|r|j|q|x'
  const complete_finals = 'w|y'
  const reSyl = new RegExp(`((?:${initials}|${complete_finals})[${finals}]+?)`, 'gi')
  const res = []
  let myArray = null
  while ((myArray = reSyl.exec(word)) !== null) {
    if(myArray.index !== 0 && res.length === 0)
      res.push(0)
    res.push(myArray.index)
  }
  if (res.length == 0)
    res.push(0)
  return res
}

function highlightPinyin (line) {
  const replacer = (match, p1, offset, string) => {
	const syllables = []  
	  /*
    const offsets = splitPinyin(match)
    
    for(let i = 0; i < offsets.length; ++i) {
      if(i + 1 == offsets.length) {
        const syl = match.substring(offsets[i], match.length)
        syllables.push(createColoredPinyin(syl))
      } else {
        const syl = match.substring(offsets[i], offsets[i+1])
        syllables.push(createColoredPinyin(syl))
      }
    }*/
	const res = splitPinyin(match)
	//console.log(match, res)
	for (let syl of res) {
	  syllables.push(createColoredPinyin(syl))
	}
    return syllables.join('')
  }
  const re = _getPinyinRegex()
  return line.replace(re, replacer)
}

function createColoredPinyin (pinyin) {
  const syllables = pinyin.split(' ').map((syllable) => {
    const getTone = (syl) => {
      for (const vowel of 'āēīōūǖĀĒĪŌŪǕ') {
        if (syllable.indexOf(vowel) !== -1) {
          return 1
        }
      }
      for (const vowel of 'áéíóúǘÁÉÍÓÚǗ') {
        if (syllable.indexOf(vowel) !== -1) {
          return 2
        }
      }
      for (const vowel of 'ǎěǐǒǔǚǍĚǏǑǓǙ') {
        if (syllable.indexOf(vowel) !== -1) {
          return 3
        }
      }
      for (const vowel of 'àèìòùǜÀÈÌÒÙǛ') {
        if (syllable.indexOf(vowel) !== -1) {
          return 4
        }
      }
      return 5
    }
    const tone = 'tone' + getTone(syllable)
    return `<span class="${tone}">${syllable}</span>`
  })
  return syllables.join(' ')
}

function articleNumberToLink (number, strLen = 6, ext = 'txt') {
  const articlesPerDir = 100
  let dirNumber = Math.floor(number / articlesPerDir)
  dirNumber = (dirNumber === 0) ? 1 : dirNumber *= articlesPerDir
  // 000001/000001.txt, ..., 00900/00900.txt, ...
  return padByZero(dirNumber, strLen) + '/' + padByZero(number, strLen) + '.' + ext
}

function padByZero (num, size) {
  let s = num.toString()
  while (s.length < size) { s = '0' + s }
  return s
}

const init = () => {
  $('.kanji_widget').on('click', function (event, ui) {
    onHanziClick(this)
  })
}

const initMHz = () => {
  $('.mhz_widget').on('click', function (event, ui) {
    onHanziMemClick(this)
  })
}

window.addEventListener('load', init, false)
window.addEventListener('load', initMHz, false)

if (typeof module !== 'undefined') {
  module.exports.createColoredPinyin = createColoredPinyin
  module.exports.articleNumberToLink = articleNumberToLink
  module.exports.createWenlinWordBoard = createWenlinWordBoard
  module.exports.createWenlinCharBoard = createWenlinCharBoard
  module.exports.findPinyin = findPinyin
  module.exports.splitPinyin = splitPinyin
  module.exports.highlightPinyin = highlightPinyin
}
