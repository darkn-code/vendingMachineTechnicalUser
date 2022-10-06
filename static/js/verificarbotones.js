var intervalID = setInterval(verificarBotones,5000);
function verificarBotones(lenPizza)
{
    var data = $.get('/comprobarBotones');
    var tm = data.done
    (
        function(result)
        {
            for (var i = 0; i < parseInt(lenPizza); i++) 
            {
                let button = document.querySelector(".button" + i.toString());
                $(".baseDatos"+i.toString()).text("");
                $(".baseDatos"+i.toString()).text(result[i]);
                if (result[i] <= 0)
                {
                    button.disabled = true;
                }
                else
                {
                    button.disabled = false;
                }
            }
        }
    )
    
  
}