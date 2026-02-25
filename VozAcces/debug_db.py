from conexion_db import ConexionDB
import sys

def check_db():
    try:
        db = ConexionDB()
        # El Singleton ya tiene cargados los datos del usuario (host, dbname, user, password)
        # si es que el usuario los cambió en el archivo conexion_db.py
        conn = db.conectar(database="voice_audit", password="123")
        cursor = conn.cursor()
        
        # Verificar si la tabla existe
        cursor.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'usuarios_voz');")
        table_exists = cursor.fetchone()[0]
        print(f"La tabla 'usuarios_voz' existe: {table_exists}")
        
        if table_exists:
            cursor.execute("SELECT username FROM usuarios_voz;")
            usuarios = cursor.fetchall()
            print("Usuarios en la base de datos:")
            for u in usuarios:
                print(f"- {u[0]}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al verificar la base de datos: {e}")

if __name__ == "__main__":
    check_db()
