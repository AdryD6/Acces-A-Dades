import os

class Config:
    # Usamos SQLite por defecto. Creará un archivo 'mysqlite.db' en tu carpeta.
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///mysqlite.db')