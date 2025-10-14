from dominio.alumno import Alumno
from servicio.alumnos_matriculados import AlumnosMatriculados

def menu():
    while True:
        print("\n--- MENÚ ---")
        print("1. Matricular alumno")
        print("2. Listar alumnos")
        print("3. Eliminar archivo de alumnos")
        print("4. Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            nombre = input("Nombre del alumno: ")
            alumno = Alumno(nombre)
            AlumnosMatriculados.matricular_alumno(alumno)
            print("Alumno matriculado correctamente.")
        elif opcion == "2":
            AlumnosMatriculados.listar_alumnos()
        elif opcion == "3":
            AlumnosMatriculados.eliminar_alumnos()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()
