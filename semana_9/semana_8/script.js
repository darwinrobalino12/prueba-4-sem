// Acción del botón de alerta
document.getElementById("btnAlerta").onclick = function() {
    alert("¡Bienvenido a Vitalfisio! Reserva tu paquete de 10 sesiones por solo $100.");
};

// Validación del formulario
document.getElementById("formulario").onsubmit = function(event) {
    event.preventDefault(); // Detiene el envío para validar

    let nombre = document.getElementById("nombre").value.trim();
    let email = document.getElementById("email").value.trim();
    let mensaje = document.getElementById("mensaje").value.trim();
    let respuesta = document.getElementById("respuesta");

    if (nombre === "" || email === "" || mensaje === "") {
        respuesta.innerHTML = `<div class="alert alert-danger">Error: Todos los campos son obligatorios.</div>`;
    } else {
        respuesta.innerHTML = `<div class="alert alert-success">¡Gracias ${nombre}! Vitalfisio se contactará contigo pronto.</div>`;
        document.getElementById("formulario").reset();
    }
};