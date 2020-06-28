from app import db


class Document(db.Model):
    author = db.Column(db.String(256))
    title = db.Column(db.String(256))
    doi = db.Column(db.String(128), primary_key=True)
    url = db.Column(db.String(128))
    ENTRYTYPE = db.Column(db.String(128))
    ID = db.Column(db.String(128))

    article = db.relationship('Article', lazy='select',
                              backref=db.backref('document', lazy='joined'))
    book = db.relationship('Book', lazy='select',
                           backref=db.backref('document', lazy='joined'))
    conferencepaper = db.relationship('ConferencePaper', lazy='select',
                                      backref=db.backref('document', lazy='joined'))


class Article(Document):
    journal = db.Column(db.String(128))
    publisher = db.Column(db.String(128))
    year = db.Column(db.String(32))
    abstract = db.Column(db.String(256))
    timestamp = db.Column(db.Date())
    __tablename__ = 'Article'
    doi = db.Column(None, db.ForeignKey('document.doi'), primary_key=True)


class Book(Document):
    publisher = db.Column(db.String(128))
    chapters = db.Column(db.String(32))
    isbn = db.Column(db.String(128))
    abstract = db.Column(db.String(256))
    __tablename__ = 'Book'
    doi = db.Column(None, db.ForeignKey('document.doi'), primary_key=True)


class ConferencePaper(Document):
    booktitle = db.Column(db.String(256))
    publisher = db.Column(db.String(128))
    year = db.Column(db.String(32))
    abstract = db.Column(db.String(2048))
    timestamp = db.Column(db.Date())
    __tablename__ = 'ConferencePaper'
    doi = db.Column(None, db.ForeignKey('document.doi'), primary_key=True)
