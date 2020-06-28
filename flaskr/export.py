import json
import tempfile
import os
import bibtexparser
from bibtexparser.bibdatabase import BibDatabase


def export(data, file_bool):
    data_ = [k for i, j in data.items() if j for k in j]
    try:
        for i in data_:
            if 'timestamp' in i:
                i['timestamp'] = i['timestamp'].strftime('%Y/%m/%d')
            for k in i:
                i[k] = str(i[k])
    except AttributeError:
        pass
    path = os.path.abspath(os.path.dirname(__file__))
    if file_bool:
        mimetype = 'application/json'
        with tempfile.NamedTemporaryFile(dir=path, delete=False, suffix='.json') as temp:
            temp.write(bytes(json.dumps(data_), encoding='utf-8'))
    else:
        mimetype = 'application/x-bibtex'
        bib_db = BibDatabase()
        bib_db.entries = data_
        bibtex_str = bibtexparser.dumps(bib_db)
        with tempfile.NamedTemporaryFile(dir=path, delete=False, suffix='.bib') as temp:
            temp.write(bytes(bibtex_str, encoding='utf-8'))

    return temp.name.split('\\')[-1], mimetype
