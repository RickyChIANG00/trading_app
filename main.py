from re import template
import sqlite3, config
from fastapi import Request
from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

app = FastAPI() 
templates = Jinja2Templates(directory="templates")
 
@app.get('/')
def index(request: Request):
    connection = sqlite3.connect(config.DB_FILE_PATH)
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute("""
        SELECT id, symbol, name FROM stock
    """)
    rows = cursor.fetchall()
    
    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows}) 
