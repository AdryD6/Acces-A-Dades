import os
from dominio.alumno import Alumno

class AlumnosMatriculados:
    ruta_archivo = "alumnos.txt"

    @staticmethod
    def matricular_alumno(alumno):
        with open(AlumnosMatriculados.ruta_archivo, "a") as archivo:
            archivo.write(alumno.nombre + "\n")

    @staticmethod
    def listar_alumnos():
        if not os.path.exists(AlumnosMatriculados.ruta_archivo):
            print("No hay alumnos matriculados.")
            return
        with open(AlumnosMatriculados.ruta_archivo, "r") as archivo:
            print("Lista de alumnos:")
            for linea in archivo:
                print("-", linea.strip())

    @staticmethod
    def eliminar_alumnos():
        if os.path.exists(AlumnosMatriculados.ruta_archivo):
            os.remove(AlumnosMatriculados.ruta_archivo)
            print("Archivo de alumnos eliminado.")
        else:
            print("No hay archivo para eliminar.")
