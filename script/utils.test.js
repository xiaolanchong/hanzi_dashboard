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
  '<p><small>1828</small> 丛(F叢) [cóng] crowd; 丛书 cóngshū series of books; 丛林 jungle</p><p>丛[叢] ²cóng {C} b.f. ①crowd together 丛集 ¹cóngjí ②a crowd 人丛 réncóng* ③collection 丛书 ¹cóngshū ④clump; thicket; grove 丛林 cónglín ◆n. Surname</p><p>The full form 叢 is 丵 \'bush\' over 取 (qǔ) \'gather\'.</p><p>"To 取 gather 丵 bushes. A bushy place, crowded; a collection, to collect" --Wieger.</p><p>The simple form 丛 is 从 cóng phonetic over 一 a line.</p>'
  const output = utils.createWenlinCharBoard('丛', article)
  expect(output.html()).toEqual(expected)
})
