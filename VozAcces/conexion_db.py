import psycopg2
import sys

class ConexionDB:
    """
    Patrón Singleton para gestionar la conexión a PostgreSQL.
    Asegura que solo exista una instancia de conexión en toda la aplicación.
    """
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super(ConexionDB, cls).__new__(cls)
            cls._instancia._conexion = None
        return cls._instancia

    def conectar(self, host="localhost", database="voice_audit", user="postgres", password="123"):
        """Establece la conexión si no existe."""
        if self._conexion is None or self._conexion.closed != 0:
            try:
                self._conexion = psycopg2.connect(
                    host=host,
                    database=database,
                    user=user,
                    password=password
                )
                print("Conexión exitosa a la base de datos.")
            except Exception as e:
                print(f"Error al conectar a PostgreSQL: {e}")
                sys.exit(1)
        return self._conexion

    def obtener_cursor(self):
        """Devuelve un cursor para ejecutar consultas."""
        if self._conexion:
            return self._conexion.cursor()
        return None

    def cerrar(self):
        """Cierra la conexión."""
        if self._conexion:
            self._conexion.close()
            print("Conexión cerrada.")
