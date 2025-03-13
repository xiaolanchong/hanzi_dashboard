
$( document ).ready(() => {
  const toggleHidden = (checkbox, className) => {
    if (checkbox.checked)
      $(`.${className}`).removeClass('hidden')
    else
      $(`.${className}`).addClass('hidden')
  }
  $('#showHanzi').change((ev) => toggleHidden(ev.target, 'hanzi_cell'))
  $('#showMeaning').change((ev) => toggleHidden(ev.target, 'meaning'))
  $('#showAssociation').change((ev) => toggleHidden(ev.target, 'association'))
  
  toggleHidden($('#showHanzi')[0], 'hanzi_cell')
  toggleHidden($('#showMeaning')[0], 'meaning')
  toggleHidden($('#showAssociation')[0], 'association')
});
