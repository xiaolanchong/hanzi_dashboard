/* global $ */

function onHanjaClick (self) {
  const hanzi = $(self).text()
  const hanjaBoardId = 'hanzi' + hanzi.charCodeAt(0)
  let hanjaBoardElem = $(`#${hanjaBoardId}`)
  if (hanjaBoardElem.length) {
    hanjaBoardElem.remove()
    return
  }
  hanjaBoardElem = $(`<div id="${hanjaBoardId}">Загрузка...</div>`)
  $(self).after(hanjaBoardElem)
  if($( "#cedict" ).prop( "checked")) {
    getCedictArticle(hanzi, hanjaBoardElem)
  }
  else if ($( "#bkrs" ).prop( "checked")) {
    getBkrsArticle(hanzi, hanjaBoardElem)
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
      parentElem.text('Иероглиф не найден на сайте')
    }
  )
}

function getBkrsArticle (hanzi, parentElem) {
  const hanziIndex = hanzi.charCodeAt(0)
  const hanjaUrl = 'bkrs/' + articleNumberToLink(hanziIndex, strLen=6, ext='xdfx')
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
      parentElem.text('Иероглиф не найден на сайте')
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
      ex: ['div', 'example'],
    }
    const [tag, cssClass] = xdfxToHtml[p2] ?? ['span','']
    return p1 ? `</${tag}>` : `<${tag} class="${cssClass}">`
  }
  htmlData = xmlData.replace(/<(\/)?([a-z]+)>/ig, replaceFunc)
  
  const board =$(`<div />`)
  $(board).html(htmlData)
  return board
}

function createHanziBoard (hanzi, textData) {
  const records = textData.split('\n')
  const table = $(`<table class="hanzi-board">` + 
                    `<caption>Слова ${hanzi}</caption>` + 
                    `<tr><th>Традиционные</th><th>Упрощенные</th><th>Пиньинь</th><th>Значение</th></tr>` + 
                  `</table>`)
  for (const record of records) {
    if (record.length == 0)
       continue;
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
  syllables = pinyin.split(' ').map( (syllable) => {
    const getTone = (syl) => {
      for(let vowel of 'āēīōūǖĀĒĪŌŪǕ') {
        if (syllable.indexOf(vowel) != -1) {
          return 1
        }
      }
      for(let vowel of 'áéíóúǘÁÉÍÓÚǗ') {
        if (syllable.indexOf(vowel) != -1) {
          return 2
        }
      }
      for(let vowel of 'ǎěǐǒǔǚǍĚǏǑǓǙ') {
        if (syllable.indexOf(vowel) != -1) {
          return 3
        }
      }
      for(let vowel of 'àèìòùǜÀÈÌÒÙǛ') {
        if (syllable.indexOf(vowel) != -1) {
          return 4
        }
      }
      return 5
    }
    tone = 'tone' + getTone(syllable)
    return `<span class="${tone}">${syllable}</span>`
  });
  return syllables.join(' ')
}


function articleNumberToLink (number, strLen=6, ext='txt') {
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