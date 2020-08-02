
$( document ).ready(() => {
    $('input.showAll').change((ev) => {
        $('.hanzi, .meaning, .meaning>span, .pinyin>span').removeClass('hidden')
    })
    $('input.hideMeaning').change( (ev) => {
        $('.meaning, .meaning>span, .pinyin>span').addClass('hidden')
        $('.hanzi').removeClass('hidden')
    })
    $('input.hideHanzi').change((ev) => {
        $('.meaning').removeClass('hidden')
        $('.hanzi, .meaning>span, .pinyin>span').addClass('hidden')
    })
});
