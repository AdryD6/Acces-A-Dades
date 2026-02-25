from conexion_db import ConexionDB
import sys

def apply_schema():
    try:
        db = ConexionDB()
        conn = db.conectar(database="voice_audit", password="123")
        cursor = conn.cursor()
        
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
            
        cursor.execute(schema_sql)
        conn.commit()
        print("Esquema aplicado exitosamente.")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error al aplicar el esquema: {e}")

if __name__ == "__main__":
    apply_schema()
