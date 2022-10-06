var intervalID = setInterval(update_values,2000);
  function update_values()
   {
    console.log('hola');
    var data = $.get('/data');
    var tm = data.done(function(result){
      $(".pago").text("");
      $(".pago").text(`Monto Depositado: ${result[0]} MXN`);
      if (result[0] >= result[1]){
        window.location.href = "/mandarAlPLC";
        setTimeout("alert('Compra completada');",1000)
      } 
    })
    
    //setTimeout("location.reload(true);",2000);
   }

