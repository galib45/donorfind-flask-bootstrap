var uploadButton = document.getElementById("upload");
var form = document.querySelector('form');

uploadButton.addEventListener('click', function(event) {
	event.preventDefault();
	var formdata = new FormData(form);
	fetch('/image/', {
		method: 'POST',
		body: formdata
	}).then(response => response.text())
	.then(text => console.log(text));
});