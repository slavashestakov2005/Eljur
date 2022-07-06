let query_send = 0, query_get = 0, query_error = 0, errors = [], classes_need_parse = 0, server = 'https://slavashestakov2005.pythonanywhere.com/';


function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

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


function parseStudent(href, step = 0) {
	if (step === 10){
		errors.push(href);
		return;
	}
	++query_send;
	$.ajax({
		url: href + "?mode=print",
		dataType: "html"
	}).done(function (msg) {
		let div = toHtml(msg);
		if (div.getElementsByClassName("page-empty").length){
			++query_get;
			return;
		}
		let title = div.getElementsByClassName("page-title")[0].textContent.split(' ');
		let tables = div.getElementsByClassName("ej-accordion");
		let data = dataForSend();
		data['cls'] = title[1];
		data['fio'] = title[title.length - 3] + " " + title[title.length - 2] + " " + title[title.length - 1];
		for (let table of tables) {
			let name = table.children[0].children[0].children[0].innerHTML;
			let info = table.children[1].children[0].children[0].children[1].innerHTML;
			data[toCode(name, href)] = info;
		}

		$.ajax({
			url: server + "parse",
			type: 'POST',
			data: data,
			dataType: "json"
		}).done(function (msg) {
			++query_get;
		});
	}).error(function (msg) {
		++query_get;
		++query_error;
		parseStudent(href, step + 1);
	});
}

function parseClass(href){
	++query_send;
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
		++query_get;
	});
}

function parseClassDelay(href){
	++classes_need_parse;
	if (query_send - query_get < 5){
		parseClass(href);
		--classes_need_parse;
	}
	else sleep(1000).then(() => { parseClassDelay(href); --classes_need_parse; });
}

function parseClassList(){
	++query_send;
	$.ajax({
		url: "https://univers.eljur.ru/journal-portfolio-action",
		dataType: "html"
	}).done(function (msg) {
		let a = toHtml(msg).getElementsByClassName("choose_classes_single")[0].getElementsByTagName("a");
		for (let element of a) {
			parseClassDelay(element.href);
		}
		++query_get;
	}).error(function (msg) {
		++query_get;
		alert("Нужно зайти в журнал");
	});
}


window.onload = function() {
	let footer = document.getElementById("footer");
	if (!footer) return;
	let button = document.createElement("input");
	button.setAttribute("type", "button");
	button.setAttribute("value", "Печать портфолио");
	button.setAttribute("name", "print-portfolio");
	let p = document.createElement("p");
	p.setAttribute("id", "tag_p_for_info_from_eljur_extension");
	button.onclick = function(){
		$.ajax({
			url: server + "start",
			type: 'POST',
			dataType: "json"
		}).done(function (msg) {
			parseClassList();
		});

		let timerId = setInterval(function() {
			let text = "Отправлено: " + query_send + "<br>" +
				"Получено: " + query_get + "<br>" +
				"Из них повторных: " + query_error + "<br>" +
				"Осталось классов: " + classes_need_parse;
			if (errors.length) text += '<br>Ошибки:<br>' + errors;
			document.getElementById('tag_p_for_info_from_eljur_extension').innerHTML = text;
			if (query_send - query_get === 0 && classes_need_parse === 0){
				clearInterval(timerId);

				let request = new XMLHttpRequest(), fileName = "log.xlsx";
				request.open('POST', server + "end", true);
				request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
				request.responseType = 'blob';

				request.onload = function(e) {
					if (this.status === 200) {
						let blob = this.response;
						if(window.navigator.msSaveOrOpenBlob) {
							window.navigator.msSaveBlob(blob, fileName);
						}
						else{
							let downloadLink = window.document.createElement('a');
							let contentTypeHeader = request.getResponseHeader("Content-Type");
							downloadLink.href = window.URL.createObjectURL(new Blob([blob], { type: contentTypeHeader }));
							downloadLink.download = fileName;
							document.body.appendChild(downloadLink);
							downloadLink.click();
							document.body.removeChild(downloadLink);
						}
					}
				};
				request.send();
			}
		}, 1000);

	};
	footer.children[0].appendChild(button);
	footer.children[0].appendChild(p);
};
