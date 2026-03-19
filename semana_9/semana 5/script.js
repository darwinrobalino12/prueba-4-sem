// 1. Referencias a los elementos del DOM
const urlInput = document.getElementById('urlImagen');
const btnAgregar = document.getElementById('btnAgregar');
const btnEliminar = document.getElementById('btnEliminar');
const galeria = document.getElementById('contenedorGaleria');

// Variable para rastrear cuál imagen está seleccionada actualmente
let imagenSeleccionada = null;

// --- FUNCIÓN PARA AGREGAR IMAGEN ---
btnAgregar.addEventListener('click', () => {
    const url = urlInput.value;

    if (url === "") {
        alert("Por favor, ingresa una URL válida.");
        return;
    }

    // Crear el elemento img dinámicamente
    const nuevaImg = document.createElement('img');
    nuevaImg.src = url;
    nuevaImg.alt = "Imagen de la galería";

    // Evento para SELECCIONAR la imagen al hacer clic
    nuevaImg.addEventListener('click', () => {
        // Si ya había una seleccionada, le quitamos el borde
        if (imagenSeleccionada) {
            imagenSeleccionada.classList.remove('seleccionada');
        }
        
        // Marcamos la nueva imagen como seleccionada
        nuevaImg.classList.add('seleccionada');
        imagenSeleccionada = nuevaImg;
    });

    // Agregar la imagen al contenedor
    galeria.appendChild(nuevaImg);

    // Limpiar el input después de agregar
    urlInput.value = "";
});

// --- FUNCIÓN PARA ELIMINAR IMAGEN ---
btnEliminar.addEventListener('click', () => {
    if (imagenSeleccionada) {
        // Eliminar del DOM el elemento seleccionado
        galeria.removeChild(imagenSeleccionada);
        imagenSeleccionada = null; // Reiniciar la variable
    } else {
        alert("Por favor, selecciona una imagen primero haciendo clic en ella.");
    }
});

// EXTRA: Atajo de teclado (tecla Delete para borrar)
document.addEventListener('keydown', (event) => {
    if (event.key === "Delete" || event.key === "Backspace") {
        btnEliminar.click();
    }
});