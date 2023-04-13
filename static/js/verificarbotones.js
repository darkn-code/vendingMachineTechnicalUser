var intervalID = setInterval(verificarBotones,5000);
var script = document.querySelector('script[src="../static/js/verificarbotones.js"]');
var precioPizza = JSON.parse(script.getAttribute('array'));
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
                //let button = document.querySelector(".button" + i.toString());
                var input = document.getElementById("cantidad" + i.toString());
                input.max = result[i];
                $(".baseDatos"+i.toString()).text("");
                $(".baseDatos"+i.toString()).text(result[i]);
/*                 if (result[i] <= 0)
                {
                    button.disabled = true;
                }
                else
                {
                    button.disabled = false;
                } */
            }

        }
    )
    //setTimeout("location.reload(true);",15000); 
  
}

function irPaginaP() {

    var cantidadPizzas = [];
    var cantidaPizzasStr = '';
    for (var i = 0; i < pizza; i++)
    {
        var input = document.getElementById("cantidad" + i.toString());
        cantidadPizzas.push(input.value);
        if (pizza-1 == i){
            cantidaPizzasStr += input.value.toString()
        }
        else{
            cantidaPizzasStr += input.value.toString() + ','
        }

    }
    console.log(cantidaPizzasStr);
    if (acc == 0){
        alert('No escogio ninguna pizza!')
    }
    else{
        $.get( "/enviarPeticion/"+ cantidaPizzasStr + '/'  + acc );
        setTimeout(() => console.log("Esperando"), 500);
        window.location.href = "/mostarPagina";
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