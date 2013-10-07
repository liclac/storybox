function setDistractions(state) {
	$('.distraction').toggleClass('distraction-hidden', !state)
}
function hideDistractionsIfEventTargetIsNotEmpty(e) {
	setDistractions($(e.target).val().length == 0)
}

function wrapSelection(element, wrap, replmap) {
	var selectedText = $(element).selection()
	if(selectedText.startsWith(wrap) && selectedText.endsWith(wrap))
	{
		var replacement = null
		for(var key in replmap)
		{
			if(selectedText.startsWith(key) && selectedText.endsWith(key))
			{
				replacement = replmap[key] + selectedText.substring(key.length, selectedText.length - key.length) + replmap[key]
				break
			}
		}
		if(replacement == null)
			replacement = selectedText.substring(wrap.length, selectedText.length - wrap.length)
		$(element).selection('replace', { text: replacement })
	}
	else
	{
		$(element).selection('replace', { text: wrap + selectedText + wrap })
	}
	
	if(selectedText.length == 0)
	{
		var pos = $(element).selection('getPos')
		$(element).selection('setPos', {start: pos.start + 1, end: pos.start + 1})
	}
}
