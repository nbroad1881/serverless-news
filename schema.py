from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema


Base = declarative_base()


class Article(Base):
    """
    Article contains [source_id, source_name, author, title, content, url, published_at]
    """
    __tablename__ = 'news_articles'

    source_id = Column(String(50))
    source_name = Column(String(100))
    author = Column(String(50))
    title = Column(String(200))
    url = Column(String(250), primary_key=True)
    published_at = Column(DateTime)


class ArticleSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Article
        load_instance = True