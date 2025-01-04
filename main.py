from fastapi import FastAPI, Request, Form
from starlette.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')


@app.get('/', response_class=HTMLResponse)
async def main(request: Request):
    return templates.TemplateResponse(
        request=request, name='main.html'
    )

@app.post('/result')
async def result(request: str = Form(...)):
    return {'message': f'Your enter: {request}'}