from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

DATABASE_URL = "postgresql://almaz:1@localhost/books"
'postgresql://username:password@host/db_name'

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    author = Column(String)
    genre = Column(String)
    created_at = Column(Integer)

Base.metadata.create_all(bind=engine)

ItemPydantic = sqlalchemy_to_pydantic(Book, exclude=['id'])

db_book = ItemPydantic(title='1984', author='George Orwell', genre='novel', created_at=1984-10-10)

def create_book(db_book: ItemPydantic):
    with SessionLocal() as db:
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    return db_book

def get_book():
    result = []
    with SessionLocal() as db:
        book = db.query(Book).all()
        for book in book:
            result.append({'title': book.title, 'author': book.author, 'genre': book.genre, 'created_at': book.created_at})
    return result

def retrieve(book_id):
    with SessionLocal() as db:
        db_book = db.query(Book).filter(Book.id==book_id).first()
        if db_book is None:
            return None
        return {
            'title': db_book.title,
            'author': db_book.author,
            'genre': db_book.genre,
            'created_at': db_book.created_at
        }

def update_book(book_id: int, book: ItemPydantic):
    with SessionLocal() as db:
        db_book = db.query(Book).filter(Book.id==book_id).first()
        if db_book is None:
            return None
        for field, value in book.dict().items():
            setattr(db_book, field, value)
        db.commit()
        db.refresh(db_book)
        return db_book

def delete_book(book_id: int):
    with SessionLocal() as db:
        db_book = db.query(Book).filter(Book.id==book_id).first()
        if not db_book:
            return None
        db.delete(db_book)
        db.commit()
        return db_book