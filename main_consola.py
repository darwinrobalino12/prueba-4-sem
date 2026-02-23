from database import GestionFisio, Paciente

def menu():
    gestion = GestionFisio()
    
    while True:
        print("\n--- SISTEMA VITALFISIO (CONTROL DE PACIENTES) ---")
        print("1. Registrar nuevo paciente")
        print("2. Mostrar todos los pacientes")
        print("3. Buscar paciente por nombre")
        print("4. Salir")
        
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            id_p = int(input("Cédula/ID: "))
            nom = input("Nombre completo: ")
            eda = int(input("Edad: "))
            tel = input("Teléfono: ")
            mot = input("Motivo de consulta: ")
            
            nuevo = Paciente(id_p, nom, eda, tel, mot)
            gestion.registrar_paciente(nuevo)
            print("¡Paciente registrado con éxito!")

        elif opcion == "2":
            pacientes = gestion.obtener_lista_pacientes()
            print("\n--- LISTA DE PACIENTES EN SISTEMA ---")
            for p in pacientes:
                print(f"ID: {p.id} | Nombre: {p.nombre} | Motivo: {p.motivo}")

        elif opcion == "3":
            nom = input("Nombre a buscar: ")
            resultados = gestion.buscar_por_nombre(nom)
            for r in resultados:
                print(f"Encontrado: {r.nombre} - Tel: {r.telefono}")

        elif opcion == "4":
            break

if __name__ == "__main__":
    menu()