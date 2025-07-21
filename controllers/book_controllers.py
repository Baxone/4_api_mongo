from fastapi import HTTPException
# como vamos conectaros con BBDD mongo tengo importar la conexion
from db.mongo import book_collection
from models.book_models import Book, BookCreate
from bson import ObjectId


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

# controlador para obtener la lista de libros


async def get_book_list():
    try:
        books = []
        # find no puede ser asincrono por que si saltariamos al for sin tener el array cargado.
        result = book_collection.find({})
        async for item in result:
            books.append(book_helper(item))
        return books
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# controlador para obtener un libro por id

async def get_book_by_id(book_id: str):
    try:
        if not ObjectId.is_valid(book_id):
            raise HTTPException(
                status_code=400, detail="Id del libro no es valido")
        book = await book_collection.find_one({'_id': ObjectId(book_id)})
        if book:
            return book_helper(book)
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


# controlador actualizar un libro por id
async def update_book(book_id: str, book_data: BookCreate):
    try:
        if not ObjectId.is_valid(book_id):
            raise HTTPException(
                status_code=400, detail="Id del libro no es valido")
        result = await book_collection.update_one(
            {"_id": ObjectId(book_id)},
            {"$set": book_data.model_dump()}
        )
        if result.modified_count == 0:
            return None
        update = await book_collection.find_one({"_id": ObjectId(book_id)})
        return book_helper(update)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


async def delete_one_book_by_id(book_id: str):
    try:
        if not ObjectId.is_valid(book_id):
            raise HTTPException(status_code=400, detail='Id no valido')
        result = await book_collection.delete_one({"_id": ObjectId(book_id)})
        if not result.deleted_count == 1:
            raise HTTPException(
                status_code=409, detail="No se ha borrado el libro, intentalo de nuevo")
        return {'msg': f"El libro con id {book_id} se ha borrado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
