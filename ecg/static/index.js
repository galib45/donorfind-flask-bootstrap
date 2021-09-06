tags = document.getElementById('tags');

previewImage = document.getElementById('preview');
fileInput = document.getElementById('image');
if (fileInput) {
	fileInput.onchange = function(event) {
		previewImage.src = URL.createObjectURL(this.files[0]);
		previewImage.style.display = 'block';
	}

	window.addEventListener('paste', (e) => {
	  	if (e.clipboardData.files.length > 0) {
	  		file = e.clipboardData.files[0];
	  		fileInput.files = e.clipboardData.files;
	  		document.getElementById('file-path').value = file.name;

	  		if (file.type.startsWith('image/')) {
	  			reader = new FileReader();
	  			reader.readAsDataURL(file);
	  			reader.onload = () => {
	  				previewImage.src = reader.result;
	  				previewImage.style.display = 'block';
	  			}
	  		}
	  	}
	});
}

function updateTags() {
	cbs = document.querySelectorAll('.filled-in:checked');
	tags.value = '';
	for (cb of cbs) {
		if (tags.value != '') {
			tags.value += ';';
		}
		tags.value += cb.nextElementSibling.innerHTML;
	}
}

function flipSwitch(code, pos) {
	return code.substr(0, pos) + '1' + code.substr(pos+1);
}

function genCode() {
	cbs = document.querySelectorAll('.filled-in');
	codeShow = document.getElementById('code');
	code = '00000000000000000000000000000';
	i = 0;
	for (cb of cbs) {
		if (cb.checked) {
			code = flipSwitch(code, i);
		}
		i++;
	}
	codeShow.value = parseInt(code, 2);
}

