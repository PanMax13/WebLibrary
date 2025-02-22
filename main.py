from http.client import responses
from logging import exception

from fastapi import FastAPI, Request, Form, UploadFile, File, Depends, Query
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List


from generate_slug import *


# import models
from db.models import Book
from BookReader import BookReader
from db.db_conn import connection, createSession


app = FastAPI()

# static file for css
app.mount('/static', StaticFiles(directory='static'), name='static')
#static files for images
app.mount('/preview_images', StaticFiles(directory='preview_images'), name='preview_images')
templates = Jinja2Templates(directory='templates')

@app.on_event("startup")
async def init():
    await connection()



# main page
@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(
        request=request, name='main.html'
    )

# show results of request from main page
@app.post('/result')
async def result(request: Request, search: str = Form(...)):
    return templates.TemplateResponse(request=request, name='view_models/bookItems.html', context={"search" : search})


# page for upload book
@app.get('/upload')
async def upload_form(request: Request):
    return templates.TemplateResponse(request=request, name='/upload.html')


# upload book to server
@app.post('/upload')
async def upload_file(
        request: Request,
        file: UploadFile = File(...),
        book_title: str = Form(...),
        book_author: str = Form(...),
        book_discription: str = Form(...),
        book_preview_image: UploadFile = File(...),
        ganre: list[str] = Form(...),
        session: AsyncSession = Depends(createSession)
    ):

    file_location = f'./books/{file.filename}'
    preview_image_location = f'{book_preview_image.filename}'
    bookTitle = book_title
    bookAuthor = book_author
    bookDiscription = book_discription
    slug = generate_slug(bookTitle)


    try:

        upload_book = Book(
            title=bookTitle,
            discription = bookDiscription,
            path=file_location,
            author=bookAuthor,
            preview_image=preview_image_location,
            slug=slug,
            ganres=ganre
        )

        session.add(upload_book)
        await session.commit()

        with open(file_location, 'wb') as file_path:
            file_path.write(file.file.read())

        with open('./preview_images/' + preview_image_location, 'wb') as preview_path:
            preview_path.write(book_preview_image.file.read())

        print(ganre)


        return RedirectResponse('/', status_code=303)

    except Exception as e:
        print(e)


# render the catalog of books
@app.get('/catalog')
async def catalog(
        request: Request,
        session: AsyncSession = Depends(createSession)
):
    catalog = select(Book)
    catalog = await session.execute(catalog)
    books = catalog.scalars().all()

    return templates.TemplateResponse(request=request, name='/catalog.html', context={'books': books})


# filter of books
@app.post('/catalog/filtered')
async def filter(
        request: Request,
        filters: List[str] | None = Form(default=None),
        session: AsyncSession = Depends(createSession)
):
    books = select(Book).where(Book.ganres.op('@>')(filters))
    books_ = await session.execute(books)
    books = books_.scalars().all()

    print(filters)
    if filters is None:
        books = select(Book)
        books = await session.execute(books)
        books = books.scalars().all()
        return templates.TemplateResponse(request=request, name='/catalog.html', context={'books': books})

    return templates.TemplateResponse(request=request, name='/catalog.html', context={'books': books, 'filters': filters})


# from for book data
@app.get('/catalog/book/{book_id}')
async def read_the_book(request: Request, book_id: int, session: AsyncSession = Depends(createSession)):
    book = await session.get(Book, book_id)
    book_preview = book.preview_image
    book_title = book.title
    book_author = book.author
    book_discription = book.discription
    ganres = book.ganres

    context = {
        'title': book_title,
        'preview_image': book_preview,
        'author': book_author,
        'discription': book_discription,
        'id': book_id,
        'ganres': ganres
    }

    return templates.TemplateResponse(request=request, name='/read_book.html', context=context)

@app.get('/catalog/book/read/{id}/{page}')
async def generate_page(reqeust: Request, id: int, page: int, session: AsyncSession = Depends(createSession)):
    book = await session.get(Book, id)

    book_ = BookReader(book.path)

    page_text = book_.page_reader(page)
    pages = book_.pagination(page)
    visible_left = page == 0
    visible_right = book_.get_last_page() == page

    context = {
        'title': book.title,
        'text': page_text,
        'pages': pages,
        'page': page,
        'id': id,
        'visible_left': visible_left,
        'visible_right': visible_right

    }

    return templates.TemplateResponse(request= reqeust, name='/reader.html', context=context)

@app.post('/test')
async def test(request: Request, ganre: List[str] | None = Form(default=None)):
    if ganre is None:
        return templates.TemplateResponse(request, '/test.html', context={"choosen": "it's empty"})
    return templates.TemplateResponse(request, '/test.html', context={"choosen": ganre})


@app.get('/test_')
async def test(request: Request):
    return templates.TemplateResponse(request, '/test.html', context={'choosen': []})

