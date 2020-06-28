from scrapy.item import Item, Field
import re
from scrapy.loader.processors import MapCompose, Join, TakeFirst
import datetime


def filter_number(value):
    return re.search(r'\d+', value).group()


def date_convert(value):
    date_format = ["%Y/%m/%d", "%Y-%m-%d", "%Y/%m", "%Y", "%b. %Y"]
    for i in date_format:
        try:
            create_date = datetime.datetime.strptime(value, i).date()
            return create_date
        except ValueError:
            pass


class Document(Item):
    author = Field(
        input_processor=MapCompose(lambda v: v.replace(u'\xa0', u' ')),
        output_processor=Join(separator=',')
    )
    title = Field()
    doi = Field()
    url = Field()
    ENTRYTYPE = Field(
        input_processor=MapCompose(lambda v: v.lower())
    )
    ID = Field()


class Article(Document):
    journal = Field()
    publisher = Field(output_processor=Join(separator=','))
    year = Field(
        input_processor=MapCompose(lambda v: v.split('/')[0] or v.split('-')[0] or v[0], str),
    )
    abstract = Field()
    timestamp = Field(
        input_processor=MapCompose(date_convert),
        output_processor=TakeFirst()
    )


class Book(Document):
    publisher = Field(
        output_processor=Join(separator=',')
    )
    chapters = Field(
        input_processor=MapCompose(filter_number, int),
        output_processor=TakeFirst()
    )
    ISBN = Field()
    abstract = Field()


class ConferencePaper(Document):
    booktitle = Field()
    publisher = Field(output_processor=Join(separator=','))
    year = Field(
        input_processor=MapCompose(lambda v: v.split('/')[0] or v.split('-')[0] or v[0], str),
    )
    abstract = Field(input_processor=MapCompose(lambda v: v.rsplit(), str)
                     )
    timestamp = Field(
        input_processor=MapCompose(date_convert),
        output_processor=TakeFirst()
    )
