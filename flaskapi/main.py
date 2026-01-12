from flask import Flask
from src.api.routes import init_api_routes
from src.config import db
# Importamos el modelo para que SQLAlchemy sepa que existe y cree la tabla
import src.models.student 

app = Flask(__name__)

# Crea las tablas en la base de datos (si no existen)
db.Base.metadata.create_all(db.engine)

# Inicializa las rutas que acabamos de crear
init_api_routes(app)

if __name__ == '__main__':
    # Arranca la aplicación en modo debug
    app.run(debug=True)