// JavaScript Document
/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */
// @author: jmacura 2019

// Vypocet bodu u zavodniku
function calcPtsRunners(data, cats, teamMax) {
	// ulozeni skol
	let teams = [];
	data.forEach(function(x) {
		if (!teams.includes(x['Název oddílu'])) {
			teams.push(x['Název oddílu']);
		}
	});
	console.log(teams);
	// vypocet bodu zavodniku
	let teamScore = [];
	teams.forEach(function(t) {
		teamScore[t] = 0;
	});
	cats.forEach(function(cat) {
		let points = teamMax*2;
		data.forEach(function(x) {
			if (x['Krátký'] == cat) {
				if (teamScore[x['Název oddílu']] < 2) { //boduji jen prvni dva z druzstva
					x['body'] = points; //zapsani poctu bodu do objektu
					teamScore[x['Název oddílu']] += 1;
					points -= 1;
				} else {
					x['body'] = 0;
				}
			}
		});
	});
}

// Vypocet bodu u druzstev
function calcPtsTeams(data) {
	let hd3 = [];
	let hd5 = [];
	let hd79 = [];
	let hds = [];
	data.forEach(function(x) {
		console.log(x['body']);
		if (x['Krátký'] == "D3" || x['Krátký'] == "H3") {
	  	if (x['Název oddílu'] in hd3) {
	    	hd3[x['Název oddílu']] += x['body'];
			} else {
	    	hd3[x['Název oddílu']] = x['body'];
			}
		} else if (x['Krátký'] == "D5" || x['Krátký'] == "H5") {
			if (x['Název oddílu'] in hd5) {
	    	hd5[x['Název oddílu']] += x['body'];
			} else {
	      hd5[x['Název oddílu']] = x['body'];
			}
		} else if (x['Krátký'] == "D7" || x['Krátký'] == "H7" || x['Krátký'] == "D9" || x['Krátký'] == "H9") {
			if (x['Název oddílu'] in hd79) {
	    	hd79[x['Název oddílu']] += x['body'];
	    } else {
	      hd79[x['Název oddílu']] = x['body'];
			}
		} else if (x['Krátký'] == "DS" || x['Krátký'] == "HS") {
			if (x['Název oddílu'] in hds) {
	    	hds[x['Název oddílu']] += x['body'];
			} else {
				hds[x['Název oddílu']] = x['body'];
			}
		}
	});
	return [hd3, hd5, hd79, hds];
}

// vyhodit DISK zavodniky, kdyz uz nejsou potreba
function filterDISK(data) {
	clearData = data.filter(function(x) {
		return x['Klasifikace'] == '0';
	});
	return clearData
}

// Zjisteni nejobsazenejsi kategorie
function findMaxOccupiedCat(teamOccupancy) {
	let teamMax = 0;
	let maxCat = undefined;
	for (const x in teamOccupancy) {
		if (teamOccupancy[x].length > teamMax) {
			teamMax = teamOccupancy[x].length;
			maxCat = x;
		}
	}
	return [maxCat, teamMax];
}

// hlavni fce - zpracovani souboru
function handleFileSelect(evt) {
	let fr = null;
	let files = evt.target.files; // FileList object
	// files is a FileList of File objects. List some properties.
	let output = [];
	for (let i = 0, f; f = files[i]; i++) {
		output.push('<li><strong>', escape(f.name), '</strong> (', f.type || 'n/a', ') - ',
			f.size, ' bytů, poslední úprava: ',
			f.lastModified ? new Date(f.lastModified).toLocaleDateString() : 'n/a',
			'&emsp;</li>');
		showInfo("Načítám...");
		Papa.parse(f, {
			header: true,
			encoding: "Windows-1250",
			dynamicTyping: true,
			complete: function(input) {
				console.log(input);
				showInfo("Načteno " + input.data.length + " závodníků. Počítám...");
				let teamOccupancy = prepareData(input.data);
				[maxCat, teamMax] = findMaxOccupiedCat(teamOccupancy);
				data = filterDISK(input.data);
				calcPtsRunners(data, Object.keys(teamOccupancy), teamMax);
				let results = calcPtsTeams(data);
				console.log(results);
				showInfo("Načteno " + input.data.length + " závodníků. Spočteno.");
				//showInfo("Nejvíce škol je v kategorii " + maxCat + ": " + teamMax + " škol");
			}
		});
		document.getElementById('list').innerHTML = '<ul>' + output.join('') + '</ul>';
	}
}

function prepareData(data){
	// Ulozeni kategorii do pole
	cats = [];
	data.forEach(function(x) {
		if (x['Krátký'] && !cats.includes(x['Krátký'])) {
		  cats.push(x['Krátký']);
		}
	});
	// Kategorie vcetne jejich obsazeni
	teamOccupancy = [];
	cats.forEach(function(cat) {
		teamOccupancy[cat] = [];
	});
	data.forEach(function(x) {
		cat = x['Krátký'];
		team = x['Název oddílu'];
		if (cat && !teamOccupancy[cat].includes(team)) {
		 	teamOccupancy[cat].push(team);
		}
	});
	return teamOccupancy;
}

$(document).ready(function() {
	document.getElementById('files').addEventListener('change', handleFileSelect, false);
});

function showInfo(txt) {
	let infoBlock = document.getElementById("info-block");

	//console.log(attrs);
	let ls, t;
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
