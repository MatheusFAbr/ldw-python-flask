from . import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    favorites = db.relationship('AnimeFavorite', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.name}>"
