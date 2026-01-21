// 1. Nuestro "arreglo" de datos iniciales
const productos = [
    { nombre: "Laptop", precio: 800, descripcion: "Potente para programar." },
    { nombre: "Mouse", precio: 20, descripcion: "Ergonómico y veloz." },
    { nombre: "Teclado", precio: 50, descripcion: "Mecánico con luces RGB." }
];

// 2. Referencias a los elementos del HTML
const listaUl = document.getElementById("lista-productos");
const botonAgregar = document.getElementById("btn-agregar");

// 3. Función para renderizar (dibujar) la lista
function mostrarProductos() {
    // Limpiamos la lista para no duplicar contenido
    listaUl.innerHTML = "";

    // Recorremos el arreglo
    productos.forEach((producto) => {
        // Creamos la "plantilla" usando Backticks (``)
        const plantilla = `
            <li>
                <strong>${producto.nombre}</strong> - $${producto.precio}
                <p>${producto.descripcion}</p>
            </li>
        `;
        // Agregamos la plantilla al HTML del <ul>
        listaUl.innerHTML += plantilla;
    });
}

// 4. Función para agregar un producto nuevo
function agregarProducto() {
    const nuevo = {
        nombre: "Producto Nuevo",
        precio: 100,
        descripcion: "Este producto se agregó al hacer clic."
    };

    // Empujamos el nuevo objeto al arreglo
    productos.push(nuevo);

    // Volvemos a llamar a la función para que se vea en pantalla
    mostrarProductos();
}

// 5. Eventos: Ejecutar funciones
// Al cargar la página, mostramos los productos iniciales
document.addEventListener("DOMContentLoaded", mostrarProductos);

// Al hacer clic en el botón, agregamos uno nuevo
botonAgregar.addEventListener("click", agregarProducto);