import tkinter as tk
from tkinter import messagebox, scrolledtext
from voice_service import VoiceService
from auth_dao import AuthDAO

class VoiceAuditApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VoiceAudit - Sistema de Acceso por Voz")
        self.root.geometry("500x600")
        
        # Servicios
        try:
            self.voice_service = VoiceService()
            self.auth_dao = AuthDAO()
        except Exception as e:
            messagebox.showerror("Error de Inicio", f"No se pudo conectar a la base de datos o al micrófono: {e}")
            root.destroy()
            return

        # UI Components
        self.create_widgets()

    def create_widgets(self):
        # Frame Registro
        reg_frame = tk.LabelFrame(self.root, text="Registro de Usuario", padx=10, pady=10)
        reg_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(reg_frame, text="Username:").grid(row=0, column=0, sticky="w")
        self.entry_reg_user = tk.Entry(reg_frame)
        self.entry_reg_user.grid(row=0, column=1, padx=5, pady=5)

        # Variable para guardar la frase capturada sin mostrarla en un Entry
        self.passphrase_capturada = ""
        self.lbl_reg_status = tk.Label(reg_frame, text="Estado: Use el botón para grabar", fg="blue")
        self.lbl_reg_status.grid(row=1, columnspan=3, pady=5)

        self.btn_reg_voice = tk.Button(reg_frame, text="🎤 Grabar Frase (3s)", command=self.capturar_pass_voz, bg="#2196F3", fg="white")
        self.btn_reg_voice.grid(row=2, column=0, padx=5, pady=5)

        tk.Button(reg_frame, text="Registrar Usuario", command=self.registrar).grid(row=2, column=1, pady=10)

        # Frame Login
        login_frame = tk.LabelFrame(self.root, text="Autenticación (Voz)", padx=10, pady=10)
        login_frame.pack(fill="x", padx=20, pady=10)

        tk.Label(login_frame, text="Username:").grid(row=0, column=0, sticky="w")
        self.entry_login_user = tk.Entry(login_frame)
        self.entry_login_user.grid(row=0, column=1, padx=5, pady=5)

        self.lbl_login_status = tk.Label(login_frame, text="Estado: Listo", fg="#4CAF50")
        self.lbl_login_status.grid(row=1, columnspan=2)

        tk.Button(login_frame, text="🎤 Hable ahora (3s)", command=self.login, bg="#4CAF50", fg="white").grid(row=2, columnspan=2, pady=10)

        # Frame Auditoría
        audit_frame = tk.LabelFrame(self.root, text="Auditoría de Accesos (JSONB)", padx=10, pady=10)
        audit_frame.pack(fill="both", expand=True, padx=20, pady=10)

        tk.Button(audit_frame, text="Refrescar Fallos Críticos", command=self.mostrar_auditoria).pack(pady=5)
        self.txt_audit = scrolledtext.ScrolledText(audit_frame, height=10)
        self.txt_audit.pack(fill="both", expand=True)

    def capturar_pass_voz(self):
        self.lbl_reg_status.config(text="Hable ahora...", fg="red")
        self.root.update()
        
        texto, confianza = self.voice_service.capturar_voz(timeout=3, phrase_time_limit=3)
        
        if texto:
            self.passphrase_capturada = texto
            self.lbl_reg_status.config(text=f"Frase grabada: '{texto}'", fg="green")
            messagebox.showinfo("Éxito", f"Frase capturada correctamente")
        else:
            self.lbl_reg_status.config(text="Error: No se detectó voz", fg="red")
            messagebox.showerror("Error", "Tiempo agotado o voz no reconocida")

    def registrar(self):
        user = self.entry_reg_user.get()
        pas = self.passphrase_capturada
        if user and pas:
            if self.auth_dao.registrar_usuario(user, pas):
                messagebox.showinfo("Éxito", f"Usuario '{user}' registrado.")
                self.entry_reg_user.delete(0, tk.END)
                self.passphrase_capturada = ""
                self.lbl_reg_status.config(text="Estado: Registrado con éxito", fg="blue")
            else:
                messagebox.showerror("Error", "No se pudo registrar (¿usuario duplicado?)")
        else:
            messagebox.showwarning("Aviso", "Rellene el username y grabe su frase")

    def login(self):
        user = self.entry_login_user.get()
        if not user:
            messagebox.showwarning("Aviso", "Ingrese su username")
            return

        self.lbl_login_status.config(text="Hable ahora...", fg="red")
        self.root.update()

        texto, confianza = self.voice_service.capturar_voz(timeout=3, phrase_time_limit=3)
        
        if texto is None or texto == "":
            self.lbl_login_status.config(text="Error en captura", fg="red")
            db_user = self.auth_dao.obtener_usuario(user)
            if db_user:
                self.auth_dao.registrar_log(db_user[0], {"status": "ERROR", "msg": "Fallo reconocimiento audio"})
            messagebox.showerror("Error", "No se pudo reconocer la voz")
            return

        self.lbl_login_status.config(text="Procesando...", fg="blue")
        self.root.update()

        exito, msg = self.auth_dao.login(user, texto, confianza)
        if exito:
            self.lbl_login_status.config(text="Acceso concedido", fg="green")
            messagebox.showinfo("Bienvenido", msg)
        else:
            self.lbl_login_status.config(text="Denegado", fg="red")
            messagebox.showerror("Acceso Denegado", msg)

    def mostrar_auditoria(self):
        self.txt_audit.delete('1.0', tk.END)
        fallos = self.auth_dao.consultar_fallos_criticos()
        for f in fallos:
            user, fecha, json_data = f
            linea = f"[{fecha.strftime('%Y-%m-%d %H:%M')}] {user}: {json_data}\n"
            self.txt_audit.insert(tk.END, linea)

if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceAuditApp(root)
    root.mainloop()
