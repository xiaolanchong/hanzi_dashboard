/* global $, it, expect */

const $ = require('jquery')
global.$ = global.jQuery = $
const utils = require('./utils.js')

it('create colored pinyin', () => {
  const output = utils.createColoredPinyin('xiāngjùn')
  expect(output).toEqual('<span class="tone1">xiāngjùn</span>')
})

it('create article link', () => {
  let output = utils.articleNumberToLink(20122)
  expect(output).toEqual('020100/020122.txt')

  output = utils.articleNumberToLink(1)
  expect(output).toEqual('000001/000001.txt')

  output = utils.articleNumberToLink(100)
  expect(output).toEqual('000100/000100.txt')

  output = utils.articleNumberToLink(20122, 5)
  expect(output).toEqual('20100/20122.txt')

  output = utils.articleNumberToLink(36987, 6, 'xlm')
  expect(output).toEqual('036900/036987.xlm')
})

it('create Wenlin character article', () => {
  const article =
  `1828 丛(F叢) [cóng] crowd; 丛书 cóngshū series of books; 丛林 jungle
丛[叢] ²cóng {C} b.f. ①crowd together 丛集 ¹cóngjí ②a crowd 人丛 réncóng* ③collection 丛书 ¹cóngshū ④clump; thicket; grove 丛林 cónglín ◆n. Surname
The full form 叢 is 丵 'bush' over 取 (qǔ) 'gather'.
"To 取 gather 丵 bushes. A bushy place, crowded; a collection, to collect" --Wieger.
The simple form 丛 is 从 cóng phonetic over 一 a line.`

  const expected =
  '<p><small>1828</small> 丛(F叢) [<span class="tone2">cóng</span>] crowd; 丛书 <span class="tone2">cóng</span><span class="tone1">shū</span> series of books; 丛林 jungle</p><p>丛[叢] ²<span class="tone2">cóng</span> {C} b.f. ①crowd together 丛集 ¹<span class="tone2">cóng</span><span class="tone2">jí</span> ②a crowd 人丛 <span class="tone2">rén</span><span class="tone2">cóng</span>* ③collection 丛书 ¹<span class="tone2">cóng</span><span class="tone1">shū</span> ④clump; thicket; grove 丛林 <span class=\"tone2\">cóng</span><span class=\"tone2\">lín</span> ◆n. Surname</p><p>The full form 叢 is 丵 \'bush\' over 取 (<span class=\"tone3\">qǔ</span>) \'gather\'.</p><p>"To 取 gather 丵 bushes. A bushy place, crowded; a collection, to collect" --Wieger.</p><p>The simple form 丛 is 从 <span class=\"tone2\">cóng</span> phonetic over 一 a line.</p><div><div></div><button>Показать слова</button><button>Закрыть</button></div>'
  const output = utils.createWenlinCharBoard('丛', article)
  expect(output.html()).toEqual(expected)
})

it('find pinyin', () => {
  let line = '---- 凸 [tū] convex; 凸透镜 tūtòujìng convex lens; 凹凸 āotū uneven'
  let res = utils.findPinyin(line)
  expect(res).toEqual([ "tū", "tūtòujìng", "āotū" ])

  line = '六 ¹liù* {A} num. six; 6 '
  res = utils.findPinyin(line)
  expect(res).toEqual([ 'liù' ])
})

it('split pinyin', () => {
  let res = utils.splitPinyin('tūtòujìng')
  expect(res).toEqual([ 0, 2, 5 ])
  
  res = utils.splitPinyin('āotū')
  expect(res).toEqual([ 0, 2 ])
})

it('highlight pinyin', () => {
  let line = '---- 凸 [tū] convex; 凸透镜 tūtòujìng convex lens; 凹凸 āotū uneven'
  let res = utils.highlightPinyin(line)
  expect(res).toEqual('---- 凸 [<span class="tone1">tū</span>] convex; 凸透镜 ' +
  '<span class="tone1">tū</span><span class="tone4">tòu</span><span class="tone4">jìng</span> convex lens; ' + 
  '凹凸 <span class="tone1">āo</span><span class="tone1">tū</span> uneven')
  
})

it('1-letter pinyin', () => {
  let line = '789  啊 [a] [ā] [á] ah--, ah?, ah..., ah!'
  let res = utils.highlightPinyin(line)
  expect(res).toEqual('789  啊 [a] [<span class="tone1">ā</span>] [<span class="tone2">á</span>]' + 
  ' ah--, ah?, ah..., ah!')
  
})



it('initial-final pinyin', () => {
  let line = '271 元 [yuán] primary; dollar'
  let res = utils.highlightPinyin(line)
  expect(res).toEqual('271 元 [<span class="tone2">yuán</span>] primary; dollar')
})