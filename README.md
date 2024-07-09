# Book Management System

### This system should allow users to perform CRUD (Create, Read, Update, Delete) operations on books.

### To create table in db:
alembic upgrade head

### To set up project 
pip install -m requirements.txt
uvicorn app.main:app --reload
