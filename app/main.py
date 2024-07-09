from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from app.routers import book
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})

app.include_router(book.router)

