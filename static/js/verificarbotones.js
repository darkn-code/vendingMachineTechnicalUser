var intervalID = setInterval(verificarBotones,1000);
var script = document.querySelector('script[src="../static/js/verificarbotones.js"]');
var precioPizza = JSON.parse(script.getAttribute('array'));
var precioPizzaFria = JSON.parse(script.getAttribute('arrayFrio'));
var total = document.getElementById("total");
total.textContent = "Total: 0 MXN";
var pizza = precioPizza.length -1;
var acc = 0; 
function verificarBotones()
{
    var data = $.get('/comprobarBotones');
    var tm = data.done
    (
        function(result)
        {
        console.log(result);
            for (var i = 0; i < pizza; i++) 
            {
                var input = document.getElementById("cantidad" + i.toString());
                var inputFrio = document.getElementById("cantidadFria" + i.toString());
                input.max = result[i] - inputFrio.value;
                inputFrio.max = result[i] - input.value;
                $(".baseDatos"+i.toString()).text("");
                $(".baseDatos"+i.toString()).text(result[i]);
            }

        }
    )
    //setTimeout("location.reload(true);",15000); 
  
}
function irPaginaP(){
    if (acc == 0){
        modalPizza.showModal();
    }
    else{
        modal.showModal();
    }
}
function cancelarPedido(){
    modalPizza.close()
    modal.close()
}
function irPaginaEfectivo(metodopago) {
    var cantidadPizzas = [];
    var cantidadFriaPizzas = [];
    var cantidaFriaPizzasStr = '';
    var cantidaPizzasStr = '';
    for (var i = 0; i < pizza; i++)
    {
        var input = document.getElementById("cantidad" + i.toString());
        var inputFrio = document.getElementById("cantidadFria" + i.toString());
        cantidadPizzas.push(input.value);
        cantidadFriaPizzas.push(inputFrio.value)
        if (pizza-1 == i){
            cantidaPizzasStr += input.value.toString();
            cantidaFriaPizzasStr += inputFrio.value.toString();
        }
        else{
            cantidaPizzasStr += input.value.toString() + ',';
            cantidaFriaPizzasStr += inputFrio.value.toString() + ',';
        }

    }
    console.log(cantidaPizzasStr);
    console.log(cantidaFriaPizzasStr);
    if (acc == 0){
        alert('No escogio ninguna pizza!')
    }
    else{
        $.get( "/enviarPeticion/"+ cantidaPizzasStr + '/'  + cantidaFriaPizzasStr + '/'  + acc );
        setTimeout(() => console.log("Esperando"), 500);
        window.location.href = "/mostarPagina/" + metodopago.toString();
    }
}

function incrementar(i){
    var input = document.getElementById("cantidad" + i.toString());
    if (input.value < input.max){
        acc +=  precioPizza[i];
        total.textContent = "Total: "+ acc + " MXN";
    }
    document.getElementById("cantidad" + i.toString()).stepUp();
}
function decrementar(i){
    var input = document.getElementById("cantidad" + i.toString());
    if (input.value > input.min){
        acc -= precioPizza[i];
        total.textContent = "Total: "+ acc + " MXN";
    }
    document.getElementById("cantidad" + i.toString()).stepDown();
}

function incrementarFrio(i){
    var input = document.getElementById("cantidadFria" + i.toString());
    if (input.value < input.max){
        acc +=  precioPizzaFria[i];
        total.textContent = "Total: "+ acc + " MXN";
    }
    document.getElementById("cantidadFria" + i.toString()).stepUp();
}
function decrementarFrio(i){
    var input = document.getElementById("cantidadFria" + i.toString());
    if (input.value > input.min){
        acc -= precioPizzaFria[i];
        total.textContent = "Total: "+ acc + " MXN";
    }
    document.getElementById("cantidadFria" + i.toString()).stepDown();
}