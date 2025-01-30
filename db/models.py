from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped
from sqlalchemy.dialects.postgresql import ARRAY

class Base(DeclarativeBase):
    pass


# book model
class Book(Base):
    __tablename__ = 'Books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), unique=True)
    discription: Mapped[str] = mapped_column(String(10000))
    path: Mapped[str] = mapped_column(String(10000))
    preview_image: Mapped[str] = mapped_column(String(10000))
    author: Mapped[str] = mapped_column(String(10000))
    slug: Mapped[str] = mapped_column(String(10000000), nullable=False, default='unknown')

    ganres: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=True)

