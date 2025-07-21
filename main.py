from fastapi import FastApi
from routes import book_routes

app = FastApi()

# Ruta de acceso a los libros
app.include_router(book_routes.router, prefix="/books", tags=['Books'])
