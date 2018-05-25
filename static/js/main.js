function sendReq(url) {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
			data = this.responseText;
			location.href = location.origin+data;
		}
	};
	xhttp.open("GET", "goto?url="+url, true);
	xhttp.send();
}

function go(){
	sendReq(uri.value)
}

function reverse(s){
    return s.split("").reverse().join("");
}

function getUrlParameter(url, key){
	var url = new URL(url);
	var val = url.searchParams.get(key);
	return val;
}