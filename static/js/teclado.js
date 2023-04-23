let Keyboard = window.SimpleKeyboard.default;

let keyboard = new Keyboard({
    onChange: inputTeclado => onChange(inputTeclado),
    onKeyPress: button => onKeyPress(button),
    theme: "hg-theme-default myTheme1"
  });
  keyboard.setOptions({
    layout: {
      'default': [
        '` 1 2 3 4 5 6 7 8 9 0 - = {bksp}',
        '{tab} q w e r t y u i o p [ ] {cancel}',
        '{lock} a s d f g h j k l ñ ; \' {enter}',
        '{shift} z x c v b n m , . / {clear}',
        '.com @ {space}'
      ],
      'shift': [
        '~ ! @ # $ % ^ &amp; * ( ) _ + {bksp}',
        '{tab} Q W E R T Y U I O P { } |',
        '{lock} A S D F G H J K L Ñ : " {enter}',
        '{shift} Z X C V B N M &lt; &gt; ? {shift}',
        '.com @ {space}'
      ]
    },
    display: {
      '{bksp}': 'backspace',
      '{enter}': '< enter',
      '{tab}': 'tab',
      '{lock}': 'Caps',
      '{shift}': 'shift',
      '{space}' : 'space',
      '{cancel}': 'cancel',
      '{clear}' : 'clear'
    }
  });
  document.querySelector(".inputTeclado").addEventListener("inputTeclado", event => {
    keyboard.setInput(event.target.value);
  });

  function tecladoModal(){
    teclado.showModal();
    if (inputTeclado =! ""){
      var tel = document.getElementById("inputTeclado");
      tel.selectionStart = tel.selectionEnd = tel.value.length;
      tel.focus();
    } 
  }  

function onChange(inputTeclado) {
  document.querySelector(".inputTeclado").value = inputTeclado;
  codigo = document.querySelector(".codigo").value = inputTeclado;
  console.log("Input changed", inputTeclado);
}

function onKeyPress(button) {
  console.log("Button pressed", button);
  if (button == '{enter}'){
    codigo = document.querySelector(".codigo").value;
    console.log("Codigo ingresao fue:", codigo);
    var data = $.get('/verificarCodigo/'+codigo.toString());
    var tm = data.done
    (
        function(result)
        {
        console.log(result);
        if (result[0] == 1){
          $(".codigoLabel").text("Codigo Ingresado Correctamente");
          document.getElementById("codigoLabel").style.color = "#008F39" 
        }
        else{
          $(".codigoLabel").text("Codigo Incorrecto");
          document.getElementById("codigoLabel").style.color = "red" 
        }
        }
    )
    teclado.close();
  }
  if (button == '{clear}'){
    keyboard.clearInput();
  }
  if (button == '{cancel}'){
    keyboard.clearInput();
    teclado.close();
  }
  if (button === "{shift}" || button === "{lock}") handleShift();
}

function handleShift() {
  let currentLayout = keyboard.options.layoutName;
  let shiftToggle = currentLayout === "default" ? "shift" : "default";

  keyboard.setOptions({
    layoutName: shiftToggle
  });
}

