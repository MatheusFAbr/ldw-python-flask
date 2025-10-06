from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importar os modelos DEPOIS que db for definido
from .anime_model import AnimeFavorite
from .user_model import User
