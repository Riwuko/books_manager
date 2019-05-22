from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    author = db.Column(db.String())
    description = db.Column(db.Text)
    category = db.Column(db.String())

    def __repr__(self):
        return f'{self.id}: "{self.title}" by {self.author}'
