function irPagina(number) {
    $.get( "/enviarPeticion/" + number);
    window.location.href = "/mostarPagina";
}
