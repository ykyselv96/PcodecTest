from typing import List

from fastapi import Depends, HTTPException, status
from sqlalchemy import select, update, delete

from app.core.get_db_session import get_session
from app.models.models import Book
from app.schemas.book_schema import BookBase
from loguru import logger


class BookCrud:

    def __init__(self, db):
        self.db = db

    async def if_book_in_db(self, title: str, author: str):
        try:
            statement = select(Book).where(Book.title == title and Book.author == author)
            result = await self.db.execute(statement)
            return result.scalars().first()
        except Exception as e:
            logger.error(f"Error via check if book exists in db {e}")


    async def add_a_new_book(self, payload: BookBase) -> BookBase:

        book_in_db = await self.if_book_in_db(title=payload.title, author=payload.author)

        if book_in_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='This book already exists',
            )

        try:
            db_book = Book(**dict(payload))
            self.db.add(db_book)
            await self.db.commit()
            await self.db.refresh(db_book)
            return [db_book]

        except Exception as e:
            logger.error(f"Error adding book {e}")


    async def retrieve_a_list_of_all_books(self) -> List[BookBase]:
        try:
            statement = select(Book)
            result = await self.db.execute(statement)
            books = result.scalars().all()
            return books

        except Exception as e:
            logger.error("Error getting list of books {e}")


    async def retrieve_details_of_a_specific_book_by_id(self, book_id: int):
        try:
            statement = select(Book).where(Book.id == book_id)
            result = await self.db.execute(statement)
            book = result.scalars().all()

            if not book:
                raise HTTPException(status_code=404, detail="Book_not_found")
            return book

        except Exception as e:
            logger.error(f"Error getting book {e}")


    async def update_an_existing_book_by_id(self, book_id: int, payload: BookBase) -> BookBase:
        try:
            breakpoint()
            statement = update(Book).where(Book.id == book_id)

            if payload.title:
                statement = statement.values(title=payload.title)

            if payload.author:
                statement = statement.values(author=payload.author)

            if payload.published_date:
                statement = statement.values(author=payload.published_date)

            if payload.isbn:
                statement = statement.values(author=payload.isbn)

            if payload.pages:
                statement = statement.values(author=payload.pages)

            await self.db.execute(statement)
            await self.db.commit()

            updated_book = await self.retrieve_details_of_a_specific_book_by_id(book_id=book_id)
            return updated_book

        except Exception as e:
            logger.error(f"Error updating book {e}")


    async def delete_a_book_by_id(self, book_id: int) -> BookBase:

        book_object = await self.retrieve_details_of_a_specific_book_by_id(book_id=book_id)

        try:
            statement = delete(Book).where(Book.id == book_id)
            await self.db.execute(statement)
            await self.db.commit()
            return book_object

        except Exception as e:
            logger.error(f"Error book deletion: {e}")

def get_book_crud(db=Depends(get_session)) -> BookCrud:
    return BookCrud(db=db)
