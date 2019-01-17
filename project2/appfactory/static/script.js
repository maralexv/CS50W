
// document.addEventListener('DOMContentLoaded', function () {
// 	document.querySelector('#submit').onclick = function user() {
// 		const username = document.querySelector('#username').value;
// 		load_page("channels");
// 		document.querySelector(".startpage").style.display = 'none';
// 		return username;
// 	}
// });







function load_page(page) {
	const request = new XMLHttpRequest();
	request.open('GET', `/${page}`);
	return false;
}