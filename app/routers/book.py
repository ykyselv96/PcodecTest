import json
from datetime import date

from fastapi import APIRouter, Depends, status, Form
from app.schemas.book_schema import BookBase, BookUpdate
from fastapi.responses import HTMLResponse
from app.crud.book_crud import BookCrud, get_book_crud
from fastapi_pagination import Page, Params, paginate
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import RedirectResponse



router = APIRouter(tags=["books"], prefix="/books")

templates = Jinja2Templates(directory="templates")



# CREATE BOOK
@router.get("/create_form", response_model=BookBase, response_class=HTMLResponse)
async def book_creation_form(request: Request) -> BookBase:
    return templates.TemplateResponse("add_book_form.html", {"request": request})


@router.post("/", response_model=BookBase, response_class=HTMLResponse)
async def add_a_new_book(request: Request,
                         title: str = Form(str),
                         author: str = Form(str),
                         isbn: str = Form(str),
                         published_date: date = Form(date),
                         pages: str = Form(str),
                         book_crud: BookCrud = Depends(get_book_crud)) -> BookBase:

    payload = BookBase(title=title, author=author, published_date=published_date, isbn=isbn, pages=pages)
    res = await book_crud.add_a_new_book(payload)
    return templates.TemplateResponse("get_all_books.html", {"request": request, "books": res})


# GET LIST OF BOOKS
@router.get("/", status_code=status.HTTP_200_OK, response_model = Page[BookBase])
async def retrieve_a_list_of_all_books(request: Request, book_crud: BookCrud = Depends(get_book_crud)) -> Page[BookBase]:
    res = await book_crud.retrieve_a_list_of_all_books()
    return templates.TemplateResponse("get_all_books.html", {"request": request, "books": res})


@router.get("/id_for_book_update", status_code=status.HTTP_200_OK, response_model = BookBase)
async def retrieve_id_delete_form(request: Request) -> BookBase:
    return templates.TemplateResponse("get_id_for_book_upd_form.html", {"request": request})


@router.get("/update_form/{book_id}", response_model=BookUpdate, response_class=HTMLResponse)
async def book_update_form(book_id: int, request: Request, book_crud: BookCrud = Depends(get_book_crud)) -> BookUpdate:
    book = await book_crud.retrieve_details_of_a_specific_book_by_id(book_id=book_id)
    if not book:
        return templates.TemplateResponse("get_all_books.html", {"request": request, "books": book})

    return templates.TemplateResponse("update_book_form.html", {"request": request, "book": book, "book_id": book_id})


@router.put("/{book_id}", status_code=status.HTTP_200_OK, response_model=BookBase)
async def update_an_existing_book_by_id(
                                        book_id: int,
                                        request: Request,
                                        book_crud: BookCrud = Depends(get_book_crud)) -> BookBase:

    request_body = await request.body()
    body_decoded = request_body.decode('utf-8')
    data_dict = json.loads(body_decoded)
    payload = BookUpdate(title=data_dict.get('title') if data_dict.get('title') != '' else None,
                         author=data_dict.get('author') if data_dict.get('author') != '' else None,
                         isbn=data_dict.get('isbn') if data_dict.get('isbn') != '' else None,
                         published_date=data_dict.get('published_date')
                                    if data_dict.get('published_date') else None,
                         pages=data_dict.get('pages') if data_dict.get('pages') != '' else None)


    res = await book_crud.update_an_existing_book_by_id(book_id=book_id, payload=payload)

    return templates.TemplateResponse("get_all_books.html", {"request": request, "books": res})

# DELETE BY ID
@router.get("/id_for_book_delete", status_code=status.HTTP_200_OK, response_model = BookBase)
async def retrieve_id_delete_form(request: Request) -> BookBase:
    return templates.TemplateResponse("get_id_for_book_del_form.html", {"request": request})


@router.delete("/{book_id}",  status_code=status.HTTP_200_OK, response_model=BookBase)
async def delete_a_book_by_id(book_id: int, request: Request, book_crud: BookCrud = Depends(get_book_crud)) -> BookBase:
    res = await book_crud.delete_a_book_by_id(book_id=book_id)
    return templates.TemplateResponse("get_all_books.html", {"request": request, "books": res})

# GET BOOK BY ID
@router.get("/id_for_book_details", status_code=status.HTTP_200_OK, response_model = BookBase)
async def retrieve_id_form(request: Request) -> BookBase:
    return templates.TemplateResponse("get_id_for_book_details_form.html", {"request": request})


@router.get("/{book_id}", status_code=status.HTTP_200_OK, response_model = BookBase)
async def retrieve_details_of_a_specific_book_by_id(book_id: int, request: Request, book_crud: BookCrud = Depends(get_book_crud)) -> BookBase:
    res = await book_crud.retrieve_details_of_a_specific_book_by_id(book_id=book_id)
    return templates.TemplateResponse("get_all_books.html", {"request": request, "books": res})





