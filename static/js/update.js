var script = document.querySelector('script[src="../static/js/update.js"]');
var metodoPago = JSON.parse(script.getAttribute('metodoPago'));
var monto = 0;


function update_values(){
  modalInicio.showModal();
  modalEfectivo.show();
  var intervalID = setInterval(cargarDatos,2000);
  function cargarDatos()
   {
    console.log(metodoPago);
    var data = $.get('/data');
    var tm = data.done(function(result){
      monto = result[0];
      $(".pago").text("");
      $(".pago").text(`Monto Depositado: ${result[0]} MXN`);
      $(".falta_pago").text(`Falta depositar: ${result[1]-result[0]} MXN`);
      if ((result[0]-result[1])!=0){
        $(".cambio").text(`Recoja su cambio ${result[0]-result[1]} MXN`); 
      }
      if (result[0] >= result[1]){ 
        compraCompletada.showModal();  
        setTimeout(() => window.location.href = "/mandarAlPLC", 2000);
      } 
    })
   }
}
function cerrarModal(){
  modalInicio.close();
 }
 function cerrarModalCompra(){
  compraCompletada.close();
  window.location.href = "/mandarAlPLC";
 }
 function cerrarModalCancelado(){
  compraCancelada.close();
 }
 function ModalCancelado(){
  compraCancelada.close();
  console.log(monto);
  window.location.href = "/compraCancelada/"+monto.toString();
 }
 function ModalCanceladoInit(){
  compraCancelada.showModal();
 }


 


