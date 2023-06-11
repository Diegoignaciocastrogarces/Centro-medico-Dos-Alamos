(function () {
    'use strict'
    // Obtener todos los formularios a los que queremos aplicar estilos de validación de Bootstrap personalizados
    var forms = document.querySelectorAll('.needs-validation')
    //Recorremos los forms y evitamos en envío sin validacion
    Array.prototype.slice.call(forms)
      .forEach(function (form) {
        form.addEventListener('submit', function (event) {            
          if (!form.checkValidity()) {
            event.preventDefault()
            event.stopPropagation()
          }else{
            alert('FORM VALIDADO')
          }
          form.classList.add('was-validated')
        }, false)
      })
  })()