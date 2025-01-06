from typing import List
from sqlalchemy import String, Integer,ForeignKey
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped, relationship

class Base(DeclarativeBase):
    pass

# author model
class Author(Base):
    __tablename__ = 'Authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(500))
    books: Mapped[List['Book']] = relationship('Book', back_populates='author')




# book model
class Book(Base):
    __tablename__ = 'Books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    discription: Mapped[str] = mapped_column(String(10000))
    pages: Mapped[int] = mapped_column(Integer)
    path: Mapped[str] = mapped_column(String(10000))
    author_id: Mapped[int] = mapped_column(ForeignKey('Authors.id'))
    author: Mapped['Author'] = relationship('Author', back_populates='books')