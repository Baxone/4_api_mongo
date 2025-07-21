from fastapi import HTTPException
# como vamos conectaros con BBDD mongo tengo importar la conexion
from db.mongo import book_collection
from models.book_models import Book, BookCreate


# vamos a crear una funcion que nos permita convertir el tipo de mongo (objecto) en una class Book de python. Vamos crear una funcion boolk_helper que transforma los datos de python => mongo. Nuestra propia funcion de parseo.

def book_helper(book: dict) -> Book:
    return Book(
        id=str(book["_id"]),
        title=book["title"],
        author=book["author"],
        year=book["year"],
        pages=book.get("pages"),
    )


# controlador post para crear un libro en mongo.
async def create_book(book_data: BookCreate):
    try:
        # model_dump() convierte un modelo un dict
        new_book = book_data.model_dump()
        result = await book_collection.insert_one(new_book)
        created = await book_collection.find_one({"_id": result.inserted_id})
        return book_helper(created)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
