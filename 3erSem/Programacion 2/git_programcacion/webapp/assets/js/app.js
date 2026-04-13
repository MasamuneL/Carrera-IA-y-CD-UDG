
// ================================================================ //

window.onload = () => {
	htmx.on("htmx:responseError", function(event) {
		alert(`Error ${event.detail.xhr.response}`)
	});
	htmx.on("htmx:sendError", function(event) {
		alert(`Error de red: no se puede conectar con el servidor.`)
	});
	htmx.on("htmx:timeout", function(event) {
		alert(`Error: se agotó el tiempo de espera para la respuesta del servidor.`)
	});
};

// ================================================================ //
