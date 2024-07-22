let sentencesArray;
let counter = 0;

jQuery.ajax({
	url: './json/data.json',
	dataType: 'json',
	success: function(data) {
		sentencesArray = data.sentences;
	},
	error: function() {
		console.error('Nie wczytano danych');
	}
});

function check() {
	let option = document.querySelector('input[name="options"]:checked').value;
	
	if (option == "opt1") {
		document.querySelector(".checkmark1").style.setProperty('--display', 'flex');
		document.querySelector(".checkmark2").style.setProperty('--display', 'none');
		document.querySelector(".checkmark3").style.setProperty('--display', 'none');
	} else if (option == "opt2") {
		document.querySelector(".checkmark1").style.setProperty('--display', 'none');
		document.querySelector(".checkmark2").style.setProperty('--display', 'flex');
		document.querySelector(".checkmark3").style.setProperty('--display', 'none');
	} else if (option == "opt3") {
		document.querySelector(".checkmark1").style.setProperty('--display', 'none');
		document.querySelector(".checkmark2").style.setProperty('--display', 'none');
		document.querySelector(".checkmark3").style.setProperty('--display', 'flex');
	}
}

function repleace() {
	let option = document.querySelector('input[name="options"]:checked').value;
	let lenght = sentencesArray.length;
	
	if (option == "opt1") {
		document.getElementById("text-container").innerHTML = sentencesArray[0];
		counter = 0;
	} else if (option == "opt2") {
		document.getElementById("text-container").innerHTML = sentencesArray[1];
		counter = 0;
	} else if (option == "opt3") {
		var rand = Math.floor((Math.random() * (lenght - 2)) + 2);
		document.getElementById("text-container").innerHTML = sentencesArray[rand];
		counter = 1;
	} else {
		console.error('Nie wybrano żadnej opcji');
	}
}

function paste() {
	var option = document.querySelector('input[name="options"]:checked').value;
	let existing = document.getElementById("text-container").innerText.split('\n\n');
	let lenght = sentencesArray.length;
	
	if (option == "opt1" && checkAvaliabilityAlert(existing, sentencesArray[0])) {
		addParagraph(existing, sentencesArray[0]);
	} else if (option == "opt2" && checkAvaliabilityAlert(existing, sentencesArray[1])) {
		addParagraph(existing, sentencesArray[1]);
	} else if (option == "opt3" && counter < (lenght - 2)) {
		do {
			let rand = Math.floor((Math.random() * (lenght - 2)) + 2);
			if (checkAvaliability(existing, sentencesArray[rand])) {
				addParagraph(existing, sentencesArray[rand]);
				counter++;
				break;
			}
		} while (1);
	} else if (option == "opt3" && counter == (lenght - 2)) {
		alert("Ten element już jest doklejony!");
	} else {
		console.error('Nie wybrano żadnej opcji');
	}
}

function reset() {
	location.reload(true);
}

function personal() {
	document.getElementById("header-title-id").innerHTML = 'Zadanie <b>rekrutacyjne</b><br/>Mateusz Ścisłowski';
}

function checkAvaliabilityAlert(array, item) {
	if (array.includes(item)) {
		alert("Ten element już jest doklejony!");
		return false;
	} else {
		return true;
	}
}

function checkAvaliability(array, item) {
	if (array.includes(item)) {
		return false;
	} else {
		return true;
	}
}

function addParagraph(array, item) {
	array.push(item);
	sorting(array);
	document.getElementById("text-container").innerText = array.join('\n\n');
}

function sorting(array) {
	array.sort(function (a, b) {
		return a.toLowerCase().localeCompare(b.toLowerCase());
	});
}