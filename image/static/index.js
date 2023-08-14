var uploadButton = document.getElementById("upload");
var form = document.querySelector('form');
var container = document.querySelector('.container');
var image = document.querySelector('#image');
var progressbar = document.querySelector('#progress_bar');
var progress = document.querySelector('#progress');
var percentage = document.querySelector('#percentage');
var description = document.querySelector('#description');

image.addEventListener('load', () => {
	percentage.innerHTML = '';
	progressbar.style.display = 'none';
	width = image.naturalWidth;
	height = image.naturalHeight;
	var url = image.src || image.href;
    if (url && url.length > 0) {
        var perf = performance.getEntriesByName(url)[0];
        imageSize = Math.round(perf.transferSize / 1024); //or encodedBodySize, decodedBodySize
        description.innerHTML += width.toString() + 'x' + height.toString();
        description.innerHTML += ', ' + imageSize.toString() + 'kB';
    }
});

uploadButton.addEventListener('click', function(event) {
	event.preventDefault();
	image.style.display = 'none';
	description.innerHTML = '';
	progress.classList.remove("indeterminate");
	progress.classList.add("determinate");

	var formdata = new FormData(form);
	// fetch('/image/', {
	// 	method: 'POST',
	// 	body: formdata
	// }).then(response => response.text())
	// .then((text) => {
	// 	filepath = '/file/image/uploads/' + text;
	// 	image.src = filepath;
	// });
	var xhr = new XMLHttpRequest();
	xhr.upload.onprogress = function(event) {
	    let percent = Math.round(100 * event.loaded / event.total);
	    percentage.innerHTML = 'Uploading ... ' + percent.toString() + '%';
	    progress.style.width = percent.toString() + '%';
	    if (progressbar.style.display == 'none') progressbar.style.display = 'block';
	    if (percent == 100) {
	    	percentage.innerHTML = 'Upload Done. Now Processing ...';
	    	progress.classList.remove("determinate");
	    	progress.classList.add("indeterminate");
	    }
	};
	xhr.onreadystatechange = function() {
	    if (xhr.readyState == XMLHttpRequest.DONE) {
	        filepath = '/file/image/uploads/' + xhr.responseText;
	        image.src = filepath;
	        image.style.display = 'block';
	    	progress.style.width = '0';
	    	percentage.innerHTML = 'Processing Done. Now Loading Image ...';
	    }
	}
	xhr.open('POST', '/image/');
	xhr.send(formdata);
});