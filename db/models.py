from sqlalchemy import String
from sqlalchemy.orm import mapped_column, DeclarativeBase, Mapped

class Base(DeclarativeBase):
    pass


# book model
class Book(Base):
    __tablename__ = 'Books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    discription: Mapped[str] = mapped_column(String(10000))
    path: Mapped[str] = mapped_column(String(10000))
    preview_image: Mapped[str] = mapped_column(String(10000))
    author: Mapped[str] = mapped_column(String(10000))