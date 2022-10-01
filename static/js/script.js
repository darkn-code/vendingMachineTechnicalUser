function irPagina(number)
{
    window.location.href="/opcion"+number.toString()+"/"; 
}
function verificarBotones(pizza)
{
    for (var i = 1; i < 9; i++) 
    {
        let button = document.querySelector(".button" + i.toString());
        if (pizza[i - 1] <= 0)
        {
            button.disabled = true;
        }
    }
}