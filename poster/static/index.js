var addButton = document.getElementById('add-para');
var paragraph = document.getElementById('paragraph');
var bold = document.getElementById('bold');
var color = document.getElementById('color');
var inputText = document.getElementById('input-text');
var text = document.getElementById('text');
var coreText = '';
addButton.addEventListener('click', function() {
	coreText = '<font color="' + color.value + '">' + paragraph.value.replace(/\n/g, '<br>') + '</font>';
	inputText.innerHTML += '<p>';
	if(bold.checked == true) {
		inputText.innerHTML += '<b>' + coreText + '</b>';
		text.value += 't';
	} else {
		inputText.innerHTML += coreText;
		text.value += 'f';
	}
	text.value += color.value + paragraph.value + '<--endblock-->';
	//console.log(text.value);
	paragraph.value = '';
	M.textareaAutoResize(paragraph);
	color.value = '#000000';
	bold.checked = false;
});