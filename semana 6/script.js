// Seleccionamos el formulario y los campos
const formulario = document.getElementById('registroForm');
const btnEnviar = document.getElementById('btnEnviar');

// Objeto para llevar el control de qué campos son válidos
const camposValidos = {
    nombre: false,
    correo: false,
    password: false,
    confirmar: false,
    edad: false
};

// --- FUNCIONES DE VALIDACIÓN ---

const validarFormulario = (e) => {
    switch (e.target.id) {
        case "nombre":
            // Validar mínimo 3 caracteres
            if (e.target.value.length >= 3) {
                marcarValido('nombre', e.target, 'errorNombre');
            } else {
                marcarInvalido('nombre', e.target, 'errorNombre', 'Mínimo 3 caracteres.');
            }
            break;

        case "correo":
            // Expresión regular para correo electrónico
            const regexCorreo = /^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$/;
            if (regexCorreo.test(e.target.value)) {
                marcarValido('correo', e.target, 'errorCorreo');
            } else {
                marcarInvalido('correo', e.target, 'errorCorreo', 'Formato de correo inválido.');
            }
            break;

        case "password":
            // Mínimo 8 caracteres, 1 número y 1 carácter especial
            const regexPassword = /^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{8,}$/;
            if (regexPassword.test(e.target.value)) {
                marcarValido('password', e.target, 'errorPassword');
            } else {
                marcarInvalido('password', e.target, 'errorPassword', 'Mín. 8 caracteres, 1 número y 1 símbolo.');
            }
            // También validar que coincidan si ya se escribió algo en confirmar
            validarCoincidenciaPas();
            break;

        case "confirmarPassword":
            validarCoincidenciaPas();
            break;

        case "edad":
            if (e.target.value >= 18) {
                marcarValido('edad', e.target, 'errorEdad');
            } else {
                marcarInvalido('edad', e.target, 'errorEdad', 'Debes ser mayor de 18 años.');
            }
            break;
    }
    
    // Al final de cada tecla, revisar si habilitamos el botón de enviar
    revisarTodo();
};

// Funciones auxiliares para no repetir código
function marcarValido(campo, input, errorId) {
    input.classList.remove('invalid');
    input.classList.add('valid');
    document.getElementById(errorId).textContent = "";
    camposValidos[campo] = true;
}

function marcarInvalido(campo, input, errorId, mensaje) {
    input.classList.remove('valid');
    input.classList.add('invalid');
    document.getElementById(errorId).textContent = mensaje;
    camposValidos[campo] = false;
}

function validarCoincidenciaPas() {
    const pass1 = document.getElementById('password');
    const pass2 = document.getElementById('confirmarPassword');
    if (pass1.value === pass2.value && pass1.value !== "") {
        marcarValido('confirmar', pass2, 'errorConfirmar');
    } else {
        marcarInvalido('confirmar', pass2, 'errorConfirmar', 'Las contraseñas no coinciden.');
    }
}

// Función para habilitar/deshabilitar botón
function revisarTodo() {
    const valores = Object.values(camposValidos);
    const todoCorrecto = valores.every(valor => valor === true);
    btnEnviar.disabled = !todoCorrecto;
}

// --- EVENTOS ---

// Escuchar cada vez que el usuario escribe (retroalimentación inmediata)
formulario.addEventListener('input', validarFormulario);

// Escuchar el envío final
formulario.addEventListener('submit', (e) => {
    e.preventDefault(); // Evita que la página se recargue
    alert("¡Registro exitoso! Todos los campos son válidos.");
});

// Limpiar estados al reiniciar
formulario.addEventListener('reset', () => {
    const inputs = formulario.querySelectorAll('input');
    inputs.forEach(input => input.classList.remove('valid', 'invalid'));
    const errores = formulario.querySelectorAll('.error-msg');
    errores.forEach(err => err.textContent = "");
    btnEnviar.disabled = true;
    // Resetear el objeto de control
    for (let key in camposValidos) camposValidos[key] = false;
});