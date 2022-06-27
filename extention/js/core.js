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

			$.ajax({
				url: xhr.responseURL + "?mode=print",
				dataType: "html"
			}).done(function (msg) {
				let div = document.createElement('div');
				div.innerHTML = msg;
				let tables = div.getElementsByClassName('portfolio_table');
				let data = [];
				for (let table of tables) data.push(table.children[0].children[1].innerHTML);

				$.ajax({
					url: "http://localhost:8080/parse",
					type: 'POST',
					data: {'educational': data[0], 'olympiads': data[1], 'research': data[2], 'events': data[3]},
					dataType: "json"
				}).done(function (msg) {
					console.log('Answer for');
					console.log(msg);
				});

			});

		};
		xhr.send(null);
	};
	footer.children[0].appendChild(button);
};
