var uploadButton = document.getElementById("upload");
var form = document.querySelector('form');
var container = document.querySelector('.container');
inputImage = document.createElement('img');
container.appendChild(inputImage);

uploadButton.addEventListener('click', function(event) {
	event.preventDefault();
	var formdata = new FormData(form);
	fetch('/image/', {
		method: 'POST',
		body: formdata
	}).then(response => response.text())
	.then((text) => {
		filepath = '/file/image/uploads/' + text;
		inputImage.src = filepath;
	});
});