// JavaScript Document
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
// @author: jmacura 2016

// global variables
//var dataBlob = null;

function handleFileSelect(evt) {
	var fr = null;
	var files = evt.target.files; // FileList object
	// files is a FileList of File objects. List some properties.
	var output = [];
	for (var i = 0, f; f = files[i]; i++) {
		output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
			f.size, ' bytů, poslední úprava: ',
			f.lastModified ? new Date(f.lastModified).toLocaleDateString() : 'n/a',
			'&emsp;</li>');
		showInfo("Načítání...");
		console.log(f);
		var results = Papa.parse(f, {
			header: true,
			encoding: "ISO-8859-2",
			dynamicTyping: true,
			complete: function(results) {
				console.log(results);
				showInfo("Načteno.");
			}
		});
	document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
}

//	console.log(dataString);
}

$(document).ready(function() {
	document.getElementById('files').addEventListener('change', handleFileSelect, false);
});

function showInfo(txt) {
	var infoBlock = document.getElementById("info-block");

	//console.log(attrs);
	var ls, t;
	//1st line
	ls = document.createElement("P");
	//r = document.createElement("TR");
	//d = document.createElement("TD");
	t = document.createTextNode(txt);
	ls.appendChild(t); //r.appendChild(d);
	//d = document.createElement("TD");
	//t = document.createTextNode(attrs[0]);
	while(infoBlock.hasChildNodes()) {
		infoBlock.removeChild(infoBlock.firstChild);
	}
	infoBlock.appendChild(ls);
}
