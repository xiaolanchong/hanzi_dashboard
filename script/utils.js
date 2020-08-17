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

function onHanjaClick (self) {
  const hanzi = $(self).text()
  const hanziBoardId = getHaziBoardId(hanzi)
  let hanjaBoardElem = $(`#${hanziBoardId}`)
  if (hanjaBoardElem.length) {
    hanjaBoardElem.remove()
    return
  }
  hanjaBoardElem = $(`<div id="${hanziBoardId}">Загрузка...</div>`)
  $(self).after(hanjaBoardElem)
  if ($('#cedict').prop('checked')) {
    getCedictArticle(hanzi, hanjaBoardElem)
  } else if ($('#bkrs').prop('checked')) {
    getBkrsArticle(hanzi, hanjaBoardElem)
  } else if ($('#wenlin').prop('checked')) {
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
  // const hanziUrl = 'wenlin/wenlin_word/' + fileName
  const hanziUrl = 'wenlin/wenlin_char/' + fileName
  $.get({
    url: hanziUrl,
    dataType: 'text'
  }
  ).done((data) => {
    parentElem.text('')
    // const board = createWenlinWordBoard(hanzi, data)
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
    //const board = createWenlinCharBoard(hanzi, data)
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
    if (traditional === undefined) { traditional = '' }
    const pinyinColored = createColoredPinyin(pinyin)
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
    const row = $(`<p>${line}</p>`)
    article.append(row)
  }

  const wordBoard = $('<div />')
  const buttonShowWord = $('<button>Показать слова</button>')
  buttonShowWord.click(()=>{
    //removeHanziBoard(hanzi)
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
    onHanjaClick(this)
  })
}

window.addEventListener('load', init, false)

if (typeof module !== 'undefined') {
  module.exports.createColoredPinyin = createColoredPinyin
  module.exports.articleNumberToLink = articleNumberToLink
  module.exports.createWenlinWordBoard = createWenlinWordBoard
  module.exports.createWenlinCharBoard = createWenlinCharBoard
}
