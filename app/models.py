from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    author = db.Column(db.String(80))
    description = db.Column(db.Text)
    category = db.Column(db.String(80))

    def __repr__(self):
        return f'{self.id}: "{self.title}" by {self.author}'
