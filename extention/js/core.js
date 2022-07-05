function toHtml(data){
	let div = document.createElement('div');
	div.innerHTML = data;
	return div;
}

function dataForSend(){
	let data = {};
	for (let name of ['educational', 'olympiads', 'contest', 'research', 'elective', 'additional_education_out', 'additional_education_in',
		'sport', 'other_olympiads', 'events_in', 'events_out', 'sport_out', 'creativity_out', 'cls', 'fio']) data[name] = '';
	return data;
}

function toCode(name, href) {
	switch (name) {
		case 'Результаты учебной деятельности': return 'educational';
		case 'Олимпиады': return 'olympiads';
		case 'Конкурсы': return 'contest';
		case 'Исследовательская работа': return 'research';
		case 'Элективные курсы': return 'elective';
		case 'Дополнительное образование (вне ОУ)': return 'additional_education_out';
		case 'Дополнительное образование (в ОУ)': return 'additional_education_in';
		case 'Спортивные достижения': return 'sport';
		case 'Прочие олимпиады': return 'other_olympiads';
		case 'Мероприятия (в ОУ)' : return 'events_in';
		case 'Мероприятия (вне ОУ)': return 'events_out';
		case 'Спорт (вне ОУ)': return 'sport_out';
		case 'Творчество (вне ОУ)': return 'creativity_out';
		default: alert("Что-то не изветное: " + name + "\n(" + href + ")");
	}
}


function parseStudent(href) {
	$.ajax({
		url: href + "?mode=print",
		dataType: "html"
	}).done(function (msg) {
		let div = toHtml(msg);
		let title = div.getElementsByClassName("page-title")[0].textContent.split(' ');
		let tables = div.getElementsByClassName("ej-accordion");
		let data = dataForSend();
		data['cls'] = title[1];
		data['fio'] = title[title.length - 3] + " " + title[title.length - 2] + " " + title[title.length - 1];
		for (let table of tables){
			let name = table.children[0].children[0].children[0].innerHTML;
			let info = table.children[1].children[0].children[0];
			info = info.children[1];
			let key = toCode(name, href);
			data[key] = info.innerHTML;
		}

		$.ajax({
			url: "http://localhost:8080/parse",
			type: 'POST',
			data: data,
			dataType: "json"
		}).done(function (msg) {});
	});
}

function parseClass(href){
	console.log(href);
	$.ajax({
		url: href,
		dataType: "html"
	}).done(function (msg) {
		let table = toHtml(msg).getElementsByClassName("ej-table ej-table--colored-lines ej-table--header-columns")[0];
		for(let row of table.rows){
			for(let newHref of row.getElementsByTagName("a")){
				parseStudent(newHref);
			}
		}
	});
}


window.onload = function() {
	let footer = document.getElementById("footer");
	if (!footer) return;
	let button = document.createElement("input");
	button.setAttribute("type", "button");
	button.setAttribute("value", "Печать портфолио");
	button.setAttribute("name", "print-portfolio");
	button.onclick = function(){
		let xhr = new XMLHttpRequest();
		xhr.open('GET', "https://univers.eljur.ru/journal-portfolio-action", true);
		xhr.onload = function () {
			let a = toHtml(xhr.response).getElementsByClassName("choose_classes_single")[0].getElementsByTagName("a");
			let hrefs = [];
			for (let element of a) hrefs.push(element.href);
			console.log(0);
			parseClass(hrefs[0]);
			console.log(1);
			parseClass(hrefs[1]);
			console.log(2);
			parseClass(hrefs[2]);
			console.log(3);
			parseClass(hrefs[3]);
			console.log(4);
			parseClass(hrefs[4]);
			console.log(5);
			parseClass(hrefs[5]);
			console.log(6);
			parseClass(hrefs[6]);
			console.log(7);
			parseClass(hrefs[7]);
			console.log(8);
			parseClass(hrefs[8]);
		};
		xhr.send(null);
	};
	footer.children[0].appendChild(button);
};
