import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.ext.declarative import declarative_base
from src.config.config import Config

# 1. Crear el motor de la base de datos
engine = sa.create_engine(Config.DATABASE_URI)

# 2. Crear la sesión (que usaremos para guardar/leer datos)
Session = orm.sessionmaker(bind=engine)
session = Session()

# 3. Crear la base para los modelos
Base = declarative_base()