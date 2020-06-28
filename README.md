# Project_DOI_
## Search with DOIs and extract the bibliographical details.

### requirements
1. crochet==1.12.0
2. Flask==1.1.2
3. Scrapy==2.1.0
4. SQLAlchemy==1.3.17
5. python-doi==0.2.0
6. flask-sqlalchemy==2.4.1
7. flask_migrate==2.5.3
### crawling springer.com;

## For journal articles:

1. Author name
2. journal title
3. Publisher
4. Article title (if using a journal)
5. Date of publication
6. language of publication
7. Volume number of a journal, magazine or encyclopedia
8. DOI
9. title of article

## For Books:

1. Author and/or editor name
2. Title of the website
3. publisher
4. isbn
5. doi
6. type_of_article 

## please run run.py

### Created basic layout in flask for searching a doi and can view the biblographical data.

Currently one can search for bibliographical data which belongs to journal articles or
books published in Springer.com .It will display the data of books and articles separately.

First the dois are searched in database from main.py if the dois are not present in the database 
dispatcher will connect it to the respected spider.

The data is stored to db by scrapy.

Pending:
1. Add upload dois as csvs etc (can still search if dois are provided as comma separated strings )
2. Add download button for json and bibtex.
3. spiders for different websites
4. add item for journals




