from http.client import responses

from fastapi import FastAPI, Request, Form, UploadFile, File, Depends
from starlette.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fileReader import page_reader

# import models
from db.models import Book
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
        session: AsyncSession = Depends(createSession)
    ):

    file_location = f'./books/{file.filename}'
    preview_image_location = f'{book_preview_image.filename}'
    bookTitle = book_title
    bookAuthor = book_author
    bookDiscription = book_discription


    try:

        upload_book = Book(
            title=bookTitle,
            discription = bookDiscription,
            path=file_location,
            author=bookAuthor,
            preview_image=preview_image_location
        )

        session.add(upload_book)
        await session.commit()

        with open(file_location, 'wb') as file_path:
            file_path.write(file.file.read())

        with open('./preview_images/' + preview_image_location, 'wb') as preview_path:
            preview_path.write(book_preview_image.file.read())


        return RedirectResponse('/', status_code=303)

    except Exception as e:
        print(e)


# render the catalog of books
@app.get('/catalog')
async def catalog(request: Request, session: AsyncSession = Depends(createSession)):
    catalog = select(Book)
    catalog = await session.execute(catalog)
    books = catalog.scalars().all()

    return templates.TemplateResponse(request=request, name='/catalog.html', context={'books': books})


@app.get('/catalog/book/{book_id}')
async def read_the_book(request: Request, book_id: int, session: AsyncSession = Depends(createSession)):
    book = await session.get(Book, book_id)
    book_preview = book.preview_image
    book_title = book.title
    book_author = book.author
    book_discription = book.discription

    context = {
        'title': book_title,
        'preview_image': book_preview,
        'author': book_author,
        'discription': book_discription
    }

    return templates.TemplateResponse(request=request, name='/read_book.html', context=context)

@app.get('/catalog/book/read/{id}/{page}')
async def generate_page(reqeust: Request, id: int, page: int, session: AsyncSession = Depends(createSession)):
    book = await session.get(Book, id)

    page_text = page_reader(book.path, page)

    context = {
        'title': book.title,
        'text': page_text
    }
    return templates.TemplateResponse(request= reqeust, name='/reader.html', context=context)