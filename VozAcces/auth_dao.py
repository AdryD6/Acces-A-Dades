import json
from datetime import datetime
from conexion_db import ConexionDB

class AuthDAO:
    """
    Data Access Object (DAO) para manejar el CRUD de usuarios y auditoría.
    Gestiona la columna JSONB 'resultado_json' para datos semi-estructurados.
    """
    def __init__(self):
        self.db = ConexionDB()
        self.conn = self.db.conectar()

    def registrar_usuario(self, username, passphrase):
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios_voz (username, passphrase_text) VALUES (%s, %s)",
                (username, passphrase)
            )
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            cursor.close()

    def obtener_usuario(self, username):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, passphrase_text FROM usuarios_voz WHERE username = %s", (username,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def registrar_log(self, usuario_id, detalles):
        """Inserta un registro en log_accesos_voz usando JSONB."""
        cursor = self.conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO log_accesos_voz (usuario_id, resultado_json) VALUES (%s, %s)",
                (usuario_id, json.dumps(detalles))
            )
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error al registrar log: {e}")
        finally:
            cursor.close()

    def login(self, username, voz_capturada, confianza):
        user = self.obtener_usuario(username)
        if not user:
            return False, "Usuario no encontrado"

        usuario_id, passphrase_correcta = user
        intentos_restantes = self._obtener_intentos_restantes(usuario_id)

        if intentos_restantes <= 0:
            return False, "Usuario bloqueado"

        # Comparación de voz (Lógica de negocio)
        if voz_capturada == passphrase_correcta.lower().strip():
            log_data = {
                "status": "SUCCESS",
                "confianza": confianza,
                "msg": "Acceso concedido"
            }
            self.registrar_log(usuario_id, log_data)
            return True, "Acceso concedido"
        else:
            intentos_restantes -= 1
            log_data = {
                "status": "FAIL",
                "confianza": confianza,
                "intentos_restantes": intentos_restantes,
                "msg": "Voz no coincide"
            }
            self.registrar_log(usuario_id, log_data)
            return False, f"Voz no coincide. Intentos restantes: {intentos_restantes}"

    def _obtener_intentos_restantes(self, usuario_id):
        """Consulta el último log para ver los intentos_restantes."""
        cursor = self.conn.cursor()
        cursor.execute(
            """SELECT resultado_json->>'intentos_restantes' 
               FROM log_accesos_voz 
               WHERE usuario_id = %s AND resultado_json->>'intentos_restantes' IS NOT NULL
               ORDER BY fecha DESC LIMIT 1""", 
            (usuario_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        return int(row[0]) if row and row[0] is not None else 3

    def consultar_fallos_criticos(self):
        """Consulta avanzada usando el operador ->> para filtrar JSONB."""
        cursor = self.conn.cursor()
        query = """
            SELECT u.username, l.fecha, l.resultado_json
            FROM log_accesos_voz l
            JOIN usuarios_voz u ON l.usuario_id = u.id
            WHERE l.resultado_json->>'status' = 'FAIL'
            OR (l.resultado_json->>'confianza')::float < 0.6
            ORDER BY l.fecha DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        return results
