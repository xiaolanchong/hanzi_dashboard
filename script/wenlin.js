
$( document ).ready(() => {
    $('input.showAll').change((ev) => {
        $('.hanzi, .meaning, .meaning>span').removeClass('hidden')
    })
    $('input.hideTranslation').change( (ev) => {
        $('.meaning, .meaning>span').addClass('hidden')
        $('.hanzi').removeClass('hidden')
    })
    $('input.hideWord').change((ev) => {
        $('.meaning, .meaning>span').removeClass('hidden')
        $('.hanzi').addClass('hidden')
    })
});
