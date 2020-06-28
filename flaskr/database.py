from models import Article, Book, ConferencePaper, Document
from sqlalchemy import inspection
from sqlalchemy.exc import OperationalError
from app import db

try:
    db.create_all()
except OperationalError:
    pass


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspection.inspect(obj).mapper.column_attrs}


def check(dois):
    out = {'data': []}
    doi_temp = []
    for i in dois:
        data = Document.query.filter_by(doi=i).first()
        if data:
            out['data'].append(object_as_dict(data))
        else:
            doi_temp.append(i)
    return doi_temp


def read(dois):
    out_db = {'book': [],
              'article': [],
              'paper': [],
              }
    out = {'data': []}
    doi_temp = []
    for i in dois:
        data = Document.query.filter_by(doi=i).first()
        if data:
            out['data'].append(object_as_dict(data))
        else:
            doi_temp.append(i)
    for i, j in out.items():
        for k in j:
            if k['ENTRYTYPE'] == 'book':
                out_db['book'].append(object_as_dict(Book.query.filter_by(doi=k['doi']).first()))
            elif k['ENTRYTYPE'] == 'paper' or k['ENTRYTYPE'] == 'chapter':
                out_db['paper'].append(object_as_dict(ConferencePaper.query.filter_by(doi=k['doi']).first()))
            else:
                out_db['article'].append(object_as_dict(Article.query.filter_by(doi=k['doi']).first()))
    return out_db


def read_all():
    out_db = {'book': [object_as_dict(book) for book in Book.query.all()],
              'article': [object_as_dict(article) for article in Article.query.all()],
              'paper': [object_as_dict(paper) for paper in ConferencePaper.query.all()],
              }

    return out_db


def save(item):
    if item:
        if item['ENTRYTYPE'] == 'book':
            def book(author, title, doi, url, ENTRYTYPE, ID, publisher, chapters, ISBN, abstract):
                return Book(author=author, title=title, doi=doi,
                            url=url, ENTRYTYPE=ENTRYTYPE, ID=ID,
                            publisher=publisher, chapters=chapters,
                            isbn=ISBN, abstract=abstract
                            )

            book = book(**item)
            db.session.add(book)
        elif item['ENTRYTYPE'] == 'paper' or item['ENTRYTYPE'] == 'chapter':
            def paper(author, title, doi, url, ENTRYTYPE, ID,
                      booktitle, publisher, year, abstract, timestamp):
                return ConferencePaper(author=author, title=title, doi=doi,
                                       url=url, ENTRYTYPE=ENTRYTYPE, ID=ID,
                                       booktitle=booktitle, publisher=publisher,
                                       year=year, abstract=abstract, timestamp=timestamp
                                       )

            paper = paper(**item)
            db.session.add(paper)
        else:
            def article(author, title, doi, url, ENTRYTYPE, ID,
                        journal, year, publisher, abstract, timestamp):
                return Article(author=author, title=title, doi=doi,
                               url=url, ENTRYTYPE=ENTRYTYPE, ID=ID, abstract=abstract,
                               journal=journal, year=year, publisher=publisher, timestamp=timestamp)

            article = article(**item)
            db.session.add(article)
        db.session.commit()
