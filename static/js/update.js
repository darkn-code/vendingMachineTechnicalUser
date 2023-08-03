var script = document.querySelector('script[src="../static/js/update.js"]');
var metodoPago = JSON.parse(script.getAttribute('metodoPago'));
var monto = 0;
let indiceColor = 0;


function update_values(){
  modalInicio.showModal();
  modalEfectivo.show();
  document.addEventListener('gesturestart', function (e) {
    e.preventDefault();
});
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
      if (result[0] >= result[1]){ 
        compraCompletada.showModal();
        if ((result[0]-result[1]) > 0){
          $(".cambio").text(`Recoja su cambio ${result[0]-result[1]} MXN`); 
        }  
        setTimeout(() => window.location.href = "/mandarAlPLC", 4000);
      }
      if (result[0]==-1){
        window.location.href = "/compraCancelada/0";
      } 
    })
  var intervalID = setInterval(cambiarEstilo,1000);
     function cambiarEstilo()
   	{
	const colores =["red","#F9C85A"];
	$(".centrado").each(function(index){
		const color = colores[index + indiceColor % colores.length];
		$(this).css("color",color);
	});
	indiceColor = (indiceColor + 1) % colores.length;
   	}
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
  if (monto == 0){
    window.location.href = "/";
  }
  else{
    compraCancelada.showModal();
  }
  
 }


 


