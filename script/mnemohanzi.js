
$( document ).ready(() => {
  const toggleHidden = (checkbox, checkBoxId, className, firstTime) => {
    let needChecked = checkbox.checked
    const fullName = 'mnemo_hanzi_' + className
    if (firstTime) {
       const isOn = localStorage.getItem(fullName)
       if (isOn !== null) {
          needChecked = (isOn === 'true')
		  if (needChecked)
			$(`#${checkBoxId}`).attr('checked', 'checked');
		  else
			$(`#${checkBoxId}`).removeAttr('checked')
       }
    } else {
       localStorage.setItem(fullName, needChecked)
    }

    if (needChecked)
      $(`.${className}`).removeClass('hidden')
    else
      $(`.${className}`).addClass('hidden')
  }
  
  const items = [
	['showHanzi', 'hanzi_cell'],
	['showMeaning', 'meaning'],
	['showAssociation', 'association'],
  ]
  for(const [checkboxId, className] of items) {
	  $(`#${checkboxId}`).change((ev) => toggleHidden(ev.target, checkboxId, className, false))
	  toggleHidden($(`#${checkboxId}`)[0], checkboxId, className, true)
  }
});
