from . import db

class AnimeFavorite(db.Model):
    __tablename__ = 'anime_favorites'
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(250), nullable=False)
    genero = db.Column(db.String(120))
    nota = db.Column(db.Float)
    image = db.Column(db.String(500))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'genero': self.genero,
            'nota': self.nota,
            'image': self.image,
            'user_id': self.user_id
        }

    def __repr__(self):
        return f"<AnimeFavorite {self.titulo}>"
